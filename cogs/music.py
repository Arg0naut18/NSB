import discord
from discord import app_commands
from discord.ext import commands
from .MusicUtils.MusicPlayer import Music
import DiscordUtils
from youtube_title_parse import get_artist_title
import asyncio
import requests
import json
from pytube import Playlist
import datetime
from SpotifyUtil import SpotifyUtil

m = Music()

j_file = open("secrets.txt")
vari = json.load(j_file)
j_file.close()
spotify_id = vari["spotipyid"]
spotify_token = vari["spotipytoken"]
spotify_redirect_uri = vari["spotipyredirecturi"]
apikey = vari['musixmatchkey']
redis_host = vari['redis_host']
redis_pass = vari['redis_pass']
redis_port = vari['redis_port']
queue_looping = False


class Queue:
    def __init__(self):
        with open("./music/queue.json", 'r') as f:
            self.past_queue = json.load(f)

    async def get_queue(self, user):
        return self.past_queue[str(user.guild.id)]

    async def make_queue(self, user):
        if user.guild.id in self.past_queue:
            return False
        self.past_queue[str(user.guild.id)] = []
        with open("./music/queue.json", 'w') as f:
            json.dump(self.past_queue, f, indent=4)
        return True

    async def add_queue(self, user, name):
        await self.make_queue(user)
        self.past_queue[str(user.guild.id)].append(name)
        with open("./music/queue.json", 'w') as f:
            json.dump(self.past_queue, f, indent=4)

    async def clear_queue(self, user):
        await self.make_queue(user)
        self.past_queue[str(user.guild.id)] = []
        with open("./music/queue.json", 'w') as f:
            json.dump(self.past_queue, f, indent=4)


class music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.queueObj = Queue()
        try:
            self.spotify = SpotifyUtil(spotify_client_id=spotify_id, spotify_client_secret=spotify_token, spotify_redirect_uri=spotify_redirect_uri, redis_pass=redis_pass, host=redis_host, port=redis_port, use_redis=True)
        except Exception as e:
            print(e)

    async def send_and_delete_msg(self, ctx, mssg, time=5, is_embed=False):
        if is_embed: msg = await ctx.send(embed=mssg)
        else: msg = await ctx.send(mssg)
        await asyncio.sleep(time)
        await msg.delete()

    @commands.command()
    async def join(self, ctx):
        try:
            await ctx.author.voice.channel.connect()
        except:
            await self.send_and_delete_msg(ctx, "You need to be connected to the vc!")
        await ctx.guild.change_voice_state(channel=ctx.author.voice.channel, self_deaf=True)

    @commands.hybrid_command(description="Bot leaves the vc", aliases=['dc', 'disconnect'])
    async def leave(self, ctx):
        try:
            vc = ctx.author.voice.channel
            player = m.get_player(guild_id=ctx.guild.id)
        except:
            await self.send_and_delete_msg(ctx, "`You must be in the vc for this command to work!`")
            return
        if player is None:
            await self.send_and_delete_msg(ctx, "`The bot must be in the vc for this command to work!`")
            return
        try:
            await ctx.message.add_reaction("👋")
        except: pass
        await player.stop()
        await ctx.voice_client.disconnect()
        await self.queueObj.clear_queue(ctx.author)

    @commands.hybrid_command(description="Play songs", aliases=['p'])
    @app_commands.rename(url="name-or-url")
    async def play(self, ctx, *, url):
        await ctx.defer()
        try:
            vc = ctx.author.voice.channel
        except:
            await ctx.send("`You need to be connected to the vc!`")
            return
        try:
            await vc.connect()
            await ctx.guild.change_voice_state(channel=ctx.author.voice.channel, self_deaf=True)
        except:
            pass
        player = m.get_player(guild_id=ctx.guild.id)
        if not player:
            player = m.create_player(ctx, ffmpeg_error_betterfix=True)
        if 'spotify.com' in url:
            type = url.split('spotify.com/')[1].split('/')[0]
            if type=='track':
                result = self.spotify.get_track_details(url)
                name, artist, url = result['name'], result['artist'], f"{result['name']} official {result['artist']}"
            else:
                tracks = self.spotify.get_tracks(url, type=type, verbose=True)
                for track in tracks.detailed_list:
                    name = track['name']
                    artist = track['artist']
                    url = f"{name} official {artist}"
                    try:
                        await player.queue(url, search=True)
                    except:
                        pass
                await player.remove_from_queue(len(player.current_queue())-1)
                await ctx.send(f"Added `{tracks.total_size}` songs to the queue!")
        if 'youtube.com/playlist?' in url:
            play_list = Playlist(url)
            for video in play_list.videos:
                name = video.title
                artist = video.author
                newtitle = f"{name} {artist}"
                try:
                    await player.queue(newtitle, search=True)
                except:
                    pass
            await player.remove_from_queue(len(player.current_queue())-1)   
            await ctx.send(f"Added `{len(play_list.videos)}` songs to the queue!")
        @player.on_play
        async def on_play(ctx, song):
            # emb = discord.Embed(title="Now Playing!", description=f"[{song.name}]({song.url})", color=0x00FF00)
            try:
                artist, title = get_artist_title(f"{song.name}")
            except:
                title = song.name
                artist = song.channel
            sname = title + " " + artist
            await self.queueObj.add_queue(ctx.author, sname)
            if song.duration % 60 >= 10:
                dura = f"{song.duration//60}:{song.duration%60}"
            else:
                secs = '0' + str(song.duration%60)
                dura = f"{song.duration//60}:{secs}"
            emb = discord.Embed(title="Now Playing!",color=0x00FF00)
            emb.add_field(name="Title", value=f"[{title}]({song.url})", inline=True)
            emb.add_field(name="Duration", value=f"`{dura}`", inline=True)
            try:
                emb.add_field(name="Artist", value=f"`{artist}`", inline=False)
            except:
                pass
            await self.send_and_delete_msg(ctx, emb, time=song.duration, is_embed=True)
        if ctx.voice_client.is_paused() and url==None:
            try:
                await player.resume()
                await ctx.message.add_reaction("👍")
            except:
                pass
        if not ctx.voice_client.is_playing() and not ctx.voice_client.is_paused():
            await player.queue(url, search=True)
            song = await player.play()
        else:
            song = await player.queue(url, search=True)
            try:
                artist, title = get_artist_title(f"{song.name}")
            except:
                title = song.name
            if song.duration % 60 >= 10:
                dura = f"{song.duration//60}:{song.duration%60}"
            else:
                secs = '0' + str(song.duration%60)
                dura = f"{song.duration//60}:{secs}"
            emb = discord.Embed(title="Queued!",color=0x00FF00)
            emb.add_field(name="Title", value=f"[{title}]({song.url})", inline=True)
            emb.add_field(name="Duration", value=f"`{dura}`", inline=True)
            try:
                emb.add_field(name="Artist", value=f"`{artist}`", inline=False)
            except:
                pass
            emb.set_footer(text=f"Position: {len(player.current_queue())}")
            await ctx.send(embed=emb)

    @commands.hybrid_command()
    async def pause(self, ctx):
        try:
            vc = ctx.author.voice.channel
        except:
            await ctx.send("`You need to be connected to the vc!`")
            return
        player = m.get_player(guild_id=ctx.guild.id)
        await player.pause()
        await ctx.message.add_reaction("⏸️")

    @commands.hybrid_command()
    async def resume(self, ctx):
        try:
            vc = ctx.author.voice.channel
        except:
            await ctx.send("`You need to be connected to the vc!`")
            return
        player = m.get_player(guild_id=ctx.guild.id)
        song = await player.resume()
        try:
            await ctx.message.add_reaction("👍")
        except:
            pass

    @commands.hybrid_command()
    async def stop(self, ctx):
        try:
            vc = ctx.author.voice.channel
        except:
            await ctx.send("`You need to be connected to the vc!`")
            return
        player = m.get_player(guild_id=ctx.guild.id)
        await player.stop()
        try:
            await ctx.message.add_reaction("🛑")
        except:
            pass
        await self.queueObj.clear_queue(ctx.author)

    @commands.hybrid_command()
    async def loop(self, ctx, term=None):
        try:
            vc = ctx.author.voice.channel
        except:
            await ctx.send("`You need to be connected to the vc!`")
            return
        player = m.get_player(guild_id=ctx.guild.id)
        if term != "queue":
            song = await player.toggle_song_loop()
            if song.is_looping:
                await ctx.send(f"Enabled loop for `{song.name}`")
            else:
                await ctx.send(f"Disabled loop for `{song.name}`")
        elif term == "queue":
            past_q = await self.queueObj.get_queue(ctx.author)
            total_queue = list(set(past_q))[:-1] + [songs.name+" "+songs.channel for songs in player.current_queue()]
            for song in total_queue:
                await player.queue(song, search=True)
            await ctx.send("Now the Queue is looping. It will loop only once.")

    @commands.hybrid_command(aliases = ['q'])
    async def queue(self, ctx):
        await ctx.defer()
        player = m.get_player(guild_id=ctx.guild.id)
        duralist = []
        duras = [str(datetime.timedelta(seconds = song.duration)) for song in player.current_queue()]
        for durationosong in duras:
            if durationosong.startswith("0:"):
                durationosong = durationosong.replace("0:", "", 1)
                duralist.append(durationosong)
        durationsofsongs = [song.duration for song in player.current_queue()]
        total_duration = sum(durationsofsongs)
        durafoot = str(datetime.timedelta(seconds = total_duration))
        if durafoot.startswith("0:"):
            durafoot = durafoot.replace("0:", "", 1)
        paginator = DiscordUtils.Pagination.CustomEmbedPaginator(ctx, remove_reactions=True)
        total_queue_list = list(dict.fromkeys(player.current_queue()))
        msg1=''
        try:
            msg1 = ''.join([f"```yaml\n{player.current_queue().index(song) + 1}) {song.name} -> ({duralist[player.current_queue().index(song)]})```" for song in total_queue_list[:15]])
        except:
            pass
        if msg1 == '':
            emptymessg = discord.Embed(title="Queue", description="Queue is empty! Add some songs.", color=0x00FF00)
            await ctx.send(embed=emptymessg)
        else:
            msg1 = ''.join([f"```yaml\n{player.current_queue().index(song) + 1}) {song.name} -> ({duralist[player.current_queue().index(song)]})```" for song in total_queue_list[1:15]])
            mainmsg = f"**Now Playing**:\n```yaml\n1) {player.now_playing().name} -> ({duralist[player.current_queue().index(player.current_queue()[0])]})\n```\n**Queue**:\n{msg1}"
        msg2 = ''.join([f"```yaml\n{player.current_queue().index(song) + 1}) {song.name} -> ({duralist[player.current_queue().index(song)]})```" for song in total_queue_list[15:30]])
        msg3 = ''.join([f"```yaml\n{player.current_queue().index(song) + 1}) {song.name} -> ({duralist[player.current_queue().index(song)]})```" for song in total_queue_list[30:45]])
        msg4 = ''.join([f"```yaml\n{player.current_queue().index(song) + 1}) {song.name} -> ({duralist[player.current_queue().index(song)]})```" for song in total_queue_list[45:60]])
        q1 = discord.Embed(title="Queue", description=mainmsg, color=0x00FF00)
        q1.set_footer(text=f"{len(player.current_queue())} songs -> ({durafoot}) duration")
        if msg2!='':
            q2 = discord.Embed(title="Queue", description=msg2, color=0x00FF00)
            embeds = [q1,q2]
            q2.set_footer(text=f"{len(player.current_queue())} songs -> ({durafoot}) duration")
        else:
            await ctx.send(embed=q1)
            return
        if msg3!='':
            q3 = discord.Embed(title="Queue", description=msg3, color=0x00FF00)
            embeds = [q1,q2,q3]
            paginator.add_reaction('⏮️', "first")
            paginator.add_reaction('⏪', "back")
            paginator.add_reaction('⏩', "next")
            paginator.add_reaction('⏭️', "last")
            q3.set_footer(text=f"{len(player.current_queue())} songs -> ({durafoot}) duration")
        else:
            paginator.add_reaction('⏪', "back")
            paginator.add_reaction('⏩', "next")
        if msg4!='':
            q4 = discord.Embed(title="Queue", description=msg4, color=0x00FF00)
            if len(player.current_queue())>60:
                q4.set_footer(text=f"{len(player.current_queue())} songs -> ({durafoot}) duration, more {len(player.current_queue())-60} songs r there.")
            else:    
                q4.set_footer(text=f"{len(player.current_queue())} songs -> ({durafoot}) duration")
            embeds = [q1,q2,q3,q4]
            paginator.add_reaction('⏮️', "first")
            paginator.add_reaction('⏪', "back")
            paginator.add_reaction('⏩', "next")
            paginator.add_reaction('⏭️', "last")
        else:
            pass
        await paginator.run(embeds)

    @commands.hybrid_command(description="Shows the song playing right now")
    async def np(self, ctx):
        player = m.get_player(guild_id=ctx.guild.id)
        song = player.now_playing()
        if song.duration % 60 >= 10:
            dura = f"{song.duration//60}:{song.duration%60}"
        else:
            secs = '0' + str(song.duration%60)
            dura = f"{song.duration//60}:{secs}"
        emb = discord.Embed(title="Now Playing!", description=f"[{song.name}]({song.url})"+f" - ({dura})", color=0x00FF00)
        await ctx.send(embed=emb)

    @commands.hybrid_command(aliases = ['next'])
    async def skip(self, ctx):
        try:
            vc = ctx.author.voice.channel
        except:
            await ctx.send("`You need to be connected to the vc!`")
            return
        player = m.get_player(guild_id=ctx.guild.id)
        data = await player.skip(force=True)
        await ctx.message.add_reaction("⏩")
        song = player.now_playing()
        emb = discord.Embed(title="Now Playing!", description=f"[{song.name}]({song.url})", color=0x00FF00)
        await ctx.send(embed=emb)
        # await ctx.send(f"Skipped from `{data[0].name}` to `{data[1].name}`")
        #else:
        # await ctx.send(f"Skipped `{data[0].name}`")

    @commands.hybrid_command()
    async def volume(self, ctx, vol):
        try:
            vc = ctx.author.voice.channel
        except:
            await ctx.send("`You need to be connected to the vc!`")
            return
        player = m.get_player(guild_id=ctx.guild.id)
        song, volume = await player.change_volume(float(vol) / 100) # volume should be a float between 0 to 1
        await ctx.send(f"Changed volume for {song.name} to {volume*100}%")

    @commands.hybrid_command()
    async def remove(self, ctx, index):
        try:
            vc = ctx.author.voice.channel
        except:
            await ctx.send("`You need to be connected to the vc!`")
            return
        player = m.get_player(guild_id=ctx.guild.id)
        if index=="last":
            ind = len(player.current_queue())
            song = await player.remove_from_queue(int(ind-1))
        else:
            song = await player.remove_from_queue(int(index)-1)
        await ctx.send(f"Removed `{song.name}` from queue")
    
    @commands.hybrid_command()
    async def lyrics(self,ctx, *, songname=None):
        api = "&apikey="+apikey
        lyrics_matcher = "matcher.lyrics.get"
        base_url = "https://api.musixmatch.com/ws/1.1/"
        format_url = "?format=json&callback=callback"
        track_search_parameter = "&q_track="
        artist_search_parameter = "&q_artist="
        if songname is None:
            player = m.get_player(guild_id=ctx.guild.id)
            song = player.now_playing()
            artistname, titlename = get_artist_title(f"{song.name}")
        elif 'by' in songname:
            titlename, artistname = songname.split('by')
        else:
            artistname, titlename = get_artist_title(f"{songname}")
        artist = ''
        title = ''
        for char in artistname:
            if char.isalpha() or char==' ':
                artist += char
        for char in titlename:
            if char.isalpha() or char==' ':
                title += char
        try:
            api_call = base_url + lyrics_matcher + format_url + artist_search_parameter + artist + track_search_parameter + title + api
            request = requests.get(api_call)
            data = request.json()
            data = data['message']['body']
            lyrics = data['lyrics']['lyrics_body']
        except:
            api_call = base_url + lyrics_matcher + format_url + track_search_parameter + title + api
            request = requests.get(api_call)
            data = request.json()
            data = data['message']['body']
            lyrics = data['lyrics']['lyrics_body']
        try:
            lyric = lyrics
            lyr = discord.Embed(title=f"{title}".title(), description=lyric, color=0x00FF00)
            await ctx.send(embed=lyr)
        except:
            await ctx.send(f'`Lyrics not found.`')
    
    @skip.error
    async def noSkipleft(self, ctx, error):
        if isinstance(error, commands.CommandInvokeError):
            await self.send_and_delete_msg(ctx, f"`Queue is empty! Add more songs.`")
    
    @play.error
    async def songcouldntbeplayed(self, ctx, error):
        if isinstance(error, commands.CommandInvokeError):
            await self.send_and_delete_msg(ctx, f"Check your arguments. Currently only youtube and spotify urls are supported. Sorry for the inconvenience.\nUse **resume** command instead of this to resume paused song.\nError:\n`{error}`")
            raise(error)
    
    @queue.error
    async def emptyqueue(self, ctx, error):
        if isinstance(error, commands.CommandInvokeError):
            print(error)
    
    @lyrics.error
    async def nolyricsfound(self, ctx, error):
        if isinstance(error, commands.CommandInvokeError):
            print(error)
            await self.send_and_delete_msg(ctx, "`Lyrics not found!`", time=7)
            return
    
async def setup(bot):
    await bot.add_cog(music(bot))