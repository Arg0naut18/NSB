import discord
from discord.ext import commands
import random
import DiscordUtils
from youtube_title_parse import get_artist_title
import asyncio
import requests
import json

m = DiscordUtils.Music()

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
        if ctx.voice_client.is_paused() and url==None:
            try:
                await player.resume()
                await ctx.message.add_reaction("👍")
            except:
                pass
        if not ctx.voice_client.is_playing():
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
        for song in player.current_queue():
            if song.duration % 60 >= 10:
                dura = f"{song.duration//60}:{song.duration%60}"
            else:
                secs = '0' + str(song.duration%60)
                dura = f"{song.duration//60}:{secs}"
            duralist.append(dura)
        msg = ''.join([f"```yaml\n{player.current_queue().index(song) + 1}) {song.name} -> ({duralist[player.current_queue().index(song)]})```" for song in player.current_queue()])
        if msg != '':
            q = discord.Embed(title="Queue", description=msg, color=0x00FF00)
        else:
            q = discord.Embed(title="Queue", description="The queue is empty! Add some songs.", color=0x00FF00)
        await ctx.send(embed=q)

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
            msg = await ctx.send(f"`If the song didn't play, it's either cause you played a non-youtube url or a youtube playlist. These formats are not supported yet. Sorry for the inconvenience.\nAnd if you used this to resume a song, I'd recommend to use resume command instead of this to avoid getting this message.`")
            print(error)
            await asyncio.sleep(10)
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