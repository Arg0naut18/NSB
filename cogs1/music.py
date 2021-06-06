import discord
from discord.ext import commands
import random
import DiscordUtils
from youtube_title_parse import get_artist_title
import asyncio
import requests
import json
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from pytube import Playlist

m = DiscordUtils.Music()

j_file = open("divinesecrets.txt")
vari = json.load(j_file)
j_file.close()
cid = vari['spotipyid']
ctoken = vari['spotipytoken']
client_cred = SpotifyClientCredentials(client_id=cid, client_secret=ctoken)

class music(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def join(self, ctx):
        try:
            await ctx.author.voice.channel.connect()
        except:
            await ctx.send("`You need to be connected to the vc!`")
        await ctx.guild.change_voice_state(channel=ctx.author.voice.channel, self_deaf=True)

    @commands.command(aliases=['dc', 'disconnect'])
    async def leave(self, ctx):
        try:
            vc = ctx.author.voice.channel
        except:
            return
        await ctx.message.add_reaction("👋")
        await ctx.voice_client.disconnect()

    @commands.command(aliases=['p'])
    async def play(self, ctx, *, url=None):
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
        sp = spotipy.Spotify(client_credentials_manager=client_cred)
        if 'spotify.com/track' in url:
            # sp = spotipy.Spotify(client_credentials_manager=client_cred)
            urn, idextra = url.split('track/')
            id, extra = idextra.split('?')
            newurn = f'spotify:track:{id}'
            song = sp.track(newurn)
            name = song['name']
            artist = song['album']['artists'][0]['name']
            url = f"{name} lyrics {artist}"
        if 'youtube.com/playlist?' in url:
            play_list = Playlist(url)
            for video in play_list.videos:
                name = video.title
                artist = video.author
                newtitle = f"{name} {artist}"
                await player.queue(newtitle, search=True)
            await ctx.send(f"Added `{len(play_list.videos)}` songs to the queue!")
        if 'spotify.com/album' in url:
            urn, idextra = url.split('album/')
            id, extra = idextra.split('?')
            newurn = f'spotify:album:{id}'
            # sp = spotipy.Spotify(client_credentials_manager=client_cred)
            album = sp.album(newurn)
            for i in range(len(album['tracks']['items'])):
                name = album['tracks']['items'][i]['name']
                artist = album['artists'][0]['name']
                url = f"{name} lyrics {artist}"
                await player.queue(url, search=True)
            await ctx.send(f"Added `{len(album['tracks']['items'])}` songs to the queue!")
        if 'spotify.com/playlist' in url:
            urn, idextra = url.split('playlist/')
            id, extra = idextra.split('?')
            newurn = f'spotify:playlist:{id}'
            # sp = spotipy.Spotify(client_credentials_manager=client_cred)
            playlist = sp.playlist(newurn)
            for i in range(len(playlist['tracks']['items'])):
                name = playlist['tracks']['items'][i]['track']['name']
                artist = playlist['tracks']['items'][i]['track']['artists'][0]['name']
                url = f"{name} lyrics {artist}"
                await player.queue(url, search=True)
            await ctx.send(f"Added `{len(playlist['tracks']['items'])}` songs to the queue!")
        if ctx.voice_client.is_paused() and url==None:
            try:
                player = m.get_player(guild_id=ctx.guild.id)
                await player.resume()
                await ctx.message.add_reaction("👍")
            except:
                pass
        if not ctx.voice_client.is_playing() and not ctx.voice_client.is_paused():
            await player.queue(url, search=True)
            song = await player.play()
            try:
                artist, title = get_artist_title(f"{song.name}")
            except:
                title = song.name
                artist = song.channel
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
            await ctx.send(embed=emb)

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
            emb.set_footer(text=f"Song added at index position {len(player.current_queue())}")
            await ctx.send(embed=emb)

    @commands.command()
    async def pause(self, ctx):
        try:
            vc = ctx.author.voice.channel
        except:
            await ctx.send("`You need to be connected to the vc!`")
            return
        player = m.get_player(guild_id=ctx.guild.id)
        await player.pause()
        await ctx.message.add_reaction("⏸️")

    @commands.command()
    async def resume(self, ctx):
        try:
            vc = ctx.author.voice.channel
        except:
            await ctx.send("`You need to be connected to the vc!`")
            return
        player = m.get_player(guild_id=ctx.guild.id)
        song = await player.resume()
        await ctx.message.add_reaction("👍")

    @commands.command()
    async def stop(self, ctx):
        try:
            vc = ctx.author.voice.channel
        except:
            await ctx.send("`You need to be connected to the vc!`")
            return
        player = m.get_player(guild_id=ctx.guild.id)
        await player.stop()
        await ctx.message.add_reaction("🛑")

    @commands.command()
    async def loop(self, ctx):
        try:
            vc = ctx.author.voice.channel
        except:
            await ctx.send("`You need to be connected to the vc!`")
            return
        player = m.get_player(guild_id=ctx.guild.id)
        song = await player.toggle_song_loop()
        if song.is_looping:
            await ctx.send(f"Enabled loop for `{song.name}`")
        else:
            await ctx.send(f"Disabled loop for `{song.name}`")

    @commands.command(aliases = ['q'])
    async def queue(self, ctx):
        player = m.get_player(guild_id=ctx.guild.id)
        duralist = []
        total_duration = 0
        if(len(player.current_queue))<0:
            emptymessg = discord.Embed(title="Queue", description="Queue is empty! Add some songs.", color=0x00FF00)
            await ctx.send(embed=emptymessg)
        else:    
            for song in player.current_queue():
                total_duration += song.duration
                if song.duration % 60 >= 10:
                    dura = f"{song.duration//60}:{song.duration%60}"
                else:
                    secs = '0' + str(song.duration%60)
                    dura = f"{song.duration//60}:{secs}"
                duralist.append(dura)
            if total_duration % 60 >= 10:
                if total_duration >= 3600:
                    hours=total_duration//3600
                    mins = (total_duration//60) - 60
                    if mins<10:
                        minu = '0'+str(mins)
                        durafoot = f"{hours}:{minu}:{secs}"
                    else:
                        durafoot = f"{hours}:{mins}:{secs}"
                else:
                    durafoot = f"{total_duration//60}:{secs}"
            else:
                secs = '0' + str(total_duration%60)
                if total_duration >= 3600:
                    hours=total_duration//3600
                    mins = (total_duration//60) - 60
                    if mins<10:
                        minu = '0'+str(mins)
                        durafoot = f"{hours}:{minu}:{secs}"
                    else:
                        durafoot = f"{hours}:{mins}:{secs}"
                else:
                    durafoot = f"{total_duration//60}:{secs}"
            noofsongs = len(player.current_queue())
            if noofsongs<15:
                msg1 = ''.join([f"```yaml\n{player.current_queue().index(song) + 1}) {song.name} -> ({duralist[player.current_queue().index(song)]})```" for song in player.current_queue()])
            else:    
                msg1 = ''.join([f"```yaml\n{player.current_queue().index(song) + 1}) {song.name} -> ({duralist[player.current_queue().index(song)]})```" for song in player.current_queue()[:15]])
                n = noofsongs//15
                paginator = DiscordUtils.Pagination.CustomEmbedPaginator(ctx)
                if n==2:
                    msg2 = ''.join([f"```yaml\n{player.current_queue().index(song) + 1}) {song.name} -> ({duralist[player.current_queue().index(song)]})```" for song in player.current_queue()[15:]])
                    msg3=''
                if n==3:
                    msg2 = ''.join([f"```yaml\n{player.current_queue().index(song) + 1}) {song.name} -> ({duralist[player.current_queue().index(song)]})```" for song in player.current_queue()[15:30]])
                    msg3 = ''.join([f"```yaml\n{player.current_queue().index(song) + 1}) {song.name} -> ({duralist[player.current_queue().index(song)]})```" for song in player.current_queue()[30:]])
                    msg4=''
                if n==4:
                    msg2 = ''.join([f"```yaml\n{player.current_queue().index(song) + 1}) {song.name} -> ({duralist[player.current_queue().index(song)]})```" for song in player.current_queue()[15:30]])
                    msg3 = ''.join([f"```yaml\n{player.current_queue().index(song) + 1}) {song.name} -> ({duralist[player.current_queue().index(song)]})```" for song in player.current_queue()[30:45]])
                    msg4 = ''.join([f"```yaml\n{player.current_queue().index(song) + 1}) {song.name} -> ({duralist[player.current_queue().index(song)]})```" for song in player.current_queue()[45:]])
                q1 = discord.Embed(title="Queue", description=msg1, color=0x00FF00)
                q1.set_footer(text=f"{len(player.current_queue())} songs -> ({durafoot}) duration")
                if msg2!='':
                    q2 = discord.Embed(title="Queue", description=msg2, color=0x00FF00)
                    embeds = [q1,q2]
                    #q2.set_footer(text=f"{len(player.current_queue())} songs -> ({durafoot}) duration")
                else:
                    await ctx.send(embed=q1)
                if msg3!='':
                    q3 = discord.Embed(title="Queue", description=msg3, color=0x00FF00)
                    embeds = [q1,q2,q3]
                    paginator.add_reaction('⏮️', "first")
                    paginator.add_reaction('⏪', "back")
                    paginator.add_reaction('⏩', "next")
                    paginator.add_reaction('⏭️', "last")
                    #q3.set_footer(text=f"{len(player.current_queue())} songs -> ({durafoot}) duration")
                else:
                    paginator.add_reaction('⏪', "back")
                    paginator.add_reaction('⏩', "next")
                if msg4!='':
                    q4 = discord.Embed(title="Queue", description=msg4, color=0x00FF00)
                    #q4.set_footer(text=f"{len(player.current_queue())} songs -> ({durafoot}) duration")
                    embeds = [q1,q2,q3,q4]
                    paginator.add_reaction('⏮️', "first")
                    paginator.add_reaction('⏪', "back")
                    paginator.add_reaction('⏩', "next")
                    paginator.add_reaction('⏭️', "last")
                else:
                    pass
                await paginator.run(embeds)
                await ctx.send(embed=q1)
        # try:
        #     msg2 = ''.join([f"```yaml\n{player.current_queue().index(song) + 1}) {song.name} -> ({duralist[player.current_queue().index(song)]})```" for song in player.current_queue()[15:]])
        # except:
        #     pass
        # if msg1 == '':
        #     q = discord.Embed(title="Queue", description="The queue is empty! Add some songs.", color=0x00FF00)
        # else:
        #     q = discord.Embed(title="Queue", description=msg1, color=0x00FF00)
        #     if msg2!='':
        #         q2 = discord.Embed(title="Queue", description=msg2, color=0x00FF00)
        #         paginator.add_reaction('⏪', "back")
        #         paginator.add_reaction('⏩', "next")
        #         embeds = [q, q2]
        #         await paginator.run(embeds)
        #     q.set_footer(text=f"{len(player.current_queue())} songs -> ({durafoot}) duration")
        #     await ctx.send(embed=q)

    @commands.command()
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

    @commands.command()
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

    @commands.command()
    async def volume(self, ctx, vol):
        try:
            vc = ctx.author.voice.channel
        except:
            await ctx.send("`You need to be connected to the vc!`")
            return
        player = m.get_player(guild_id=ctx.guild.id)
        song, volume = await player.change_volume(float(vol) / 100) # volume should be a float between 0 to 1
        await ctx.send(f"Changed volume for {song.name} to {volume*100}%")

    @commands.command()
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
    
    @skip.error
    async def noSkipleft(self, ctx, error):
        if isinstance(error, commands.CommandInvokeError):
            msg = await ctx.send(f"`Queue is empty! Add more songs.`")
            await asyncio.sleep(5)
            await msg.delete()
    
    @play.error
    async def songcouldntbeplayed(self, ctx, error):
        if isinstance(error, commands.CommandInvokeError):
            msg = await ctx.send(f"Check your arguments. Currently only youtube and spotify urls are supported. Sorry for the inconvenience.\nUse **resume** command instead of this to resume paused song.\nIf you think you didn't do any of these errors, disconnect the bot and use **r music** command to refresh the music commands.")
            print(error)
            await asyncio.sleep(15)
            await msg.delete()
    
def setup(bot):
    bot.add_cog(music(bot))


    # @commands.command()
    # async def lyrics(self,ctx, *, songname=None):
    #     if songname is None:
    #         player = m.get_player(guild_id=ctx.guild.id)
    #         song = player.now_playing()
    #         artistname, titlename = get_artist_title(f"{song.name}")
    #     else:
    #         artistname, titlename = get_artist_title(f"{songname}")
    #     artist = ''
    #     title = ''
    #     for char in artistname:
    #         if char.isalpha():
    #             artist += char
    #     for char in titlename:
    #         if char.isalpha():
    #             title += char
    #     r = requests.get('https://api.lyrics.ovh/v1/{}/{}'.format(artist, title))
    #     if r.status_code == 200:
    #         l_response = json.loads(r.content)
    #         try:
    #             async with ctx.typing():
    #                 lyric = l_response["lyrics"]
    #                 lyr = discord.Embed(title=f"{title}".title(), description=lyric.replace("\n\n", "\n"), color=0x00FF00)
    #                 await ctx.send(embed=lyr)
    #         except:
    #             await ctx.send(f'`Lyrics not found.`')