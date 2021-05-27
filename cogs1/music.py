import discord
from discord import FFmpegPCMAudio
from discord.ext import commands
import random
import os
from pyyoutube import Api
import json
import urllib
import pafy
import re
from youtube_title_parse import get_artist_title
from PyLyrics import *
import lyricsgenius as lg

j_file = open("secrets.txt")
vari = json.load(j_file)
j_file.close()
ytKey = vari["ytKey"]
gid = vari["geniusid"]
gsecret = vari["geniussecret"]
gtoken = vari["geniustoken"]
api = Api(api_key=ytKey)
queue = []

class music(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['p'])
    async def play(self, ctx, *, song_name=None):
        playing = False
        try:
            vc = ctx.author.voice.channel
            if song_name is None:
                paused = ctx.voice_client.is_paused()
                if paused == True:
                    await ctx.message.add_reaction("⏯️")
                    ctx.voice_client.resume()
            elif playing == False:
                req = song_name
                FFMPEG_OPTS = {
                    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
                query_string = urllib.parse.urlencode(
                    {'search_query': song_name})
                htm_content = urllib.request.urlopen(
                    'http://www.youtube.com/results?' + query_string)
                search_results = re.findall(r'/watch\?v=(.{11})',
                                            htm_content.read().decode())
                url = 'http://www.youtube.com/watch?v=' + search_results[0]
                vidfile = pafy.new(url)
                try:
                    artist, title = get_artist_title(f"{vidfile.title}")
                except:
                    pass
                audiofiles = vidfile.audiostreams
                audiofile = audiofiles[1]
                name = audiofile.title
                try:
                    paused = ctx.voice_client.is_paused()
                    state = ctx.voice_client.is_playing()
                    if state == True and paused == False:
                        queue.append(audiofile.title)
                except:
                    pass
                async with ctx.typing():
                    emb = discord.Embed(title="Now playing:",
                                        # description=f"Song: [{title}]({url})\nArtist: **{artist}**",
                                        color=random.randint(0x000000, 0xFFFFFF))
                    try:
                        emb.add_field(
                            name="Title", value=f"[{title}]({url})", inline=False)
                    except:
                        emb.add_field(
                            name="Title", value=f"[{vidfile.title}]({url})", inline=False)
                    try:
                        emb.add_field(
                            name="Artist", value=f"{artist}", inline=False)
                    except:
                        pass
                    playing = await ctx.send(embed=emb)
                try:
                    await vc.connect()
                except:
                    pass
            else:
                await ctx.send("`Current song didn't finish yet!`")
        except Exception as e:
            await ctx.send("`U need to be connected in a vc!`")
            print(e)
            return
        else:
            playing = True
            ctx.voice_client.play(FFmpegPCMAudio(
                audiofile.url, **FFMPEG_OPTS))

    @commands.command(aliases=['dc'])
    async def leave(self, ctx):
        if ctx.author.voice.channel:
            try:
                await ctx.message.add_reaction("👋")
                await ctx.voice_client.disconnect()
            except:
                pass

    @commands.command()
    async def pause(self, ctx):
        stat = ctx.voice_client.is_playing()
        paused = ctx.voice_client.is_paused()
        if paused != True:
            await ctx.message.add_reaction("⏸️")
            ctx.voice_client.pause()
        else:
            if stat == True:
                await ctx.send("`Song is already paused!`")
            else:
                await ctx.send("`No song is playing!`")

    @commands.command()
    async def stop(self, ctx):
        stat = ctx.voice_client.is_playing()
        paused = ctx.voice_client.is_paused()
        if paused != True:
            await ctx.message.add_reaction("🛑")
            ctx.voice_client.stop()
        else:
            if stat == True:
                await ctx.send("`Song is already paused!`")
            else:
                await ctx.send("`No song is playing!`")

def setup(bot):
    bot.add_cog(music(bot))
