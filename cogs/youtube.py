import discord
from discord.ext import commands
import random
import os
from pyyoutube import Api
import json
import urllib
import re

j_file = open("secrets.txt")
vari = json.load(j_file)
j_file.close()
ytKey = vari["ytKey"]
api = Api(api_key = ytKey)
color = [15158332, 3066993, 10181046, 3447003, 1752220, 15844367]

class youtube(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['ytsubs'])
    async def subs(self, ctx, *, channelName = None):
        color_main = color[random.randint(0,5)]
        if channelName is None:
            await ctx.send("Please enter the name or channel id of the channel u want to see the subscribers of.")
        else:
            try:
                channel_by_name = api.get_channel_info(channel_name=channelName)
                channel_by_id = api.get_channel_info(channel_id=channelName)
                try:
                    data = channel_by_name.items[0].to_dict()
                except Exception:
                    data = channel_by_id.items[0].to_dict()
                subs = data["statistics"]["subscriberCount"]
                thum = data["snippet"]["thumbnails"]["default"]["url"]
                embed = discord.Embed(title=f'{channelName}', description = f'The current subscribers of {channelName} are `{subs}`', color=color_main)
                embed.set_thumbnail(url = thum)
                await ctx.send(embed=embed)
            except Exception as e:
                print(e)
                await ctx.send("Channel not found!")

    @commands.command(aliases = ['ytc'])
    async def subscomp(self, ctx, channel1, channel2 = None):
        color_main = color[random.randint(0,5)]
        if channel2 is None:
            try:
                channel_by_name = api.get_channel_info(channel_name=channel1)
                channel_by_id = api.get_channel_info(channel_id=channel1)
                try:
                    data = channel_by_name.items[0].to_dict()
                except Exception:
                    data = channel_by_id.items[0].to_dict()
                subs = data["statistics"]["subscriberCount"]
                embed = discord.Embed(title=f'{channel1}', description = f'The current subscribers of {channel1} are `{subs}`', color=color_main)
                await ctx.send(embed=embed)
            except Exception as e:
                print(e)
                await ctx.send("Channel not found!")
        else:
            try:
                channel_by_name1 = api.get_channel_info(channel_name=channel1)
                channel_by_id1 = api.get_channel_info(channel_id=channel1)
                try:
                    data1 = channel_by_name1.items[0].to_dict()
                except Exception:
                    data1 = channel_by_id1.items[0].to_dict()
                channel_by_name2 = api.get_channel_info(channel_name=channel2)
                channel_by_id2 = api.get_channel_info(channel_id=channel2)
                try:
                    data2 = channel_by_name2.items[0].to_dict()
                except Exception:
                    data2 = channel_by_id2.items[0].to_dict()
                subs1 = data1["statistics"]["subscriberCount"]
                subs2 = data2["statistics"]["subscriberCount"]
                if subs1 > subs2:
                    res = int(subs1) - int(subs2)
                    embed = discord.Embed(title=f'Subscriber Comparison of {channel1} and {channel2}', description = f'The result is: {channel1} has `{res}` subscribers more \
                    than {channel2}', color=color_main)
                    await ctx.send(embed=embed)
                else:
                    res = int(subs2) - int(subs1)
                    embed = discord.Embed(title=f'Subscriber Comparison of {channel1} and {channel2}', description = f'The result is: {channel2} has `{res}` subscribers more \
                    than {channel1}', color=color_main)
                    await ctx.send(embed=embed)
            except Exception as e:
                print(e)
                await ctx.send("Channel not found!")
                
    @commands.command(aliases = ['yts'])
    async def ytsearch(self, ctx, *, search):

        query_string = urllib.parse.urlencode({'search_query': search})
        htm_content = urllib.request.urlopen(
            'http://www.youtube.com/results?' + query_string)
        search_results = re.findall(r'/watch\?v=(.{11})',
                                    htm_content.read().decode())
        await ctx.send('http://www.youtube.com/watch?v=' + search_results[0])      

async def setup(bot):
    await bot.add_cog(youtube(bot))
