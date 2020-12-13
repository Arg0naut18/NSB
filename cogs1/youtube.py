import discord
from discord.ext import commands
import random
import os
from pyyoutube import Api
import json
import zulu
from datetime import datetime
import urllib.request

j_file = open("secrets.txt")
vari = json.load(j_file)
j_file.close()
ytKey = vari["ytKey"]
api = Api(api_key = ytKey)
channelId = "UCgAbQLdWSQiJkivZ6_YDn8w" #for JasJ
# channelId = "UCiadaFEhLevKjf6xyXePSAA"
# channelId = "UC9tUVrIU8IKzB4alGP3wp5w"
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

    @commands.command(aliases=['latvid'])
    async def vid(self, ctx, ytchannel = None):
        color_main = color[random.randint(0, 5)]
        ytchannel = "UCgAbQLdWSQiJkivZ6_YDn8w" if not ytchannel else ytchannel
        member = ctx.author
        try:
            channel_by_name = api.get_channel_info(channel_name=ytchannel)
            channel_by_id = api.get_channel_info(channel_id=ytchannel)
            try:
                data = channel_by_name.items[0].to_dict()
            except Exception:
                data = channel_by_id.items[0].to_dict()
        except Exception as e:
            print(e)
            await ctx.send("Channel not found!")
        try:
            Url = f'https://www.googleapis.com/youtube/v3/search?part=snippet&channelId={ytchannel}&maxResults=1&order=date&type=video&key={ytKey}'
            inp = urllib.request.urlopen(Url)
        except:
            ytchannel = data["id"]
            Url = f'https://www.googleapis.com/youtube/v3/search?part=snippet&channelId={ytchannel}&maxResults=1&order=date&type=video&key={ytKey}'
            inp = urllib.request.urlopen(Url)
            
        resp = json.load(inp)
        inp.close()
        # time = zulu.now()
        # time = time.strftime(r"%Y-%m-%dT%I:%M:%SZ")
        first = resp['items'][0]
        # pubTime = first["snippet"]["publishedAt"]
        vidId = "https://www.youtube.com/watch?v=" + first["id"]["videoId"]
        # title = first["snippet"]["title"]
        # desc = first["snippet"]["description"]
        name = first["snippet"]["channelTitle"]
        # channel_by_id = api.get_channel_info(channel_id=ytchannel)
        # data = channel_by_id.items[0].to_dict()
        # thumbnail = first["snippet"]["thumbnails"]["high"]["url"]
        # icon = data["snippet"]["thumbnails"]["default"]["url"]

        # e = discord.Embed(color = color_main, description = desc)
        # e.add_field(name="Link", value=vidId, inline=False)
        # e.set_author(name = title, icon_url = icon)
        # e.set_thumbnail(url = thumbnail)
        # e.set_footer(text=f"id: {member.id}", icon_url=member.avatar_url)
        await ctx.send(f"Waddap {member.mention}! This is **{name}**'s latest video! Go check it out!")
        await ctx.send(vidId)
        # await ctx.send(embed = e)
        # await ctx.send(str(time) + " " + str(pubTime))

def setup(bot):
    bot.add_cog(youtube(bot))
