import discord
from discord.ext import commands
import random
# from pydactyl import PterodactylClient
import json
import sys
import psutil
import os
from pytz import timezone

j_file = open("divinesecrets.txt")
vari = json.load(j_file)
j_file.close()
serverapikey = vari["serverapikey"]


class pterostats(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['pterostats', 'status', 'server'])
    @commands.is_owner()
    async def pstats(self, ctx):
        # client = PterodactylClient('https://panel.chaoticdestiny.host', serverapikey)
        # my_servers = client.client.list_servers()
        # srv_id = my_servers[0]['identifier']
        # srv_utilization = client.client.get_server_utilization(srv_id)
        member_count = len(self.bot.users)
        # member_count = len([m for m in self.bot.users if not m.bot])
        emb = discord.Embed(title="Panel Status", color=random.randint(0x000000, 0xFFFFFF))
        # emb.add_field(name="Uptime", value="` `", inline=True)
        emb.add_field(name="Memory Usage", value=f"`{psutil.Process(os.getpid()).memory_info().rss / 1024 ** 2} MB`", inline=True)
        emb.add_field(name="CPU Usage", value=f"`{psutil.cpu_percent(interval=0.5)}%`", inline=True)
        emb.add_field(name="Ping / Latency", value=f"`{round(self.bot.latency*1000)} ms`", inline=True)
        emb.add_field(name="Python Version", value=f"`{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}`", inline=True)
        emb.add_field(name="Discord.py Version", value=f"`{discord.__version__}`", inline=True)
        emb.add_field(name="Servers", value=f"`{len(self.bot.guilds)}`", inline=True)
        emb.add_field(name="Members", value=f"`{member_count}`", inline=True)
        await ctx.send(embed=emb)

    @commands.command(aliases=['gstats', 'guild'])
    @commands.has_permissions(administrator=True)
    async def guildstats(self, ctx):
        creationdate = ctx.guild.created_at
        creation = creationdate.replace(tzinfo=timezone('UTC')).astimezone(timezone('Asia/Kolkata'))
        online = 0
        offline = 0
        away = 0
        dnd = 0
        for member in ctx.guild.members:
            if str(member.status)=="online":
                online += 1
            elif str(member.status)=="dnd":
                dnd += 1
            elif member.status=="idle":
                away += 1
            else:
                offline += 1
        banned_users = await ctx.guild.bans()
        emb = discord.Embed(title=f"{ctx.guild.name}'s Status", color=0x00FF00)
        emb.add_field(name="Name", value=f"{ctx.guild.name}", inline=False)
        emb.add_field(name="Members", value=f"`{len([m for m in ctx.guild.members if not m.bot])}`", inline=True)
        emb.add_field(name="Bots", value=f"`{len([m for m in ctx.guild.members if m.bot])}`", inline=True)
        emb.add_field(name="Region", value=f"{ctx.guild.region}".title(), inline=True)
        emb.add_field(name="Banned Members", value=f"`{len(banned_users)}`", inline=True)
        emb.add_field(name="Member Status", value=f":green_circle:`{online}` :red_circle:`{dnd}` :orange_circle:`{away}` :white_circle:`{offline}`", inline=False)
        emb.add_field(name="Created At", value=f'{creation.strftime("%a, %b %d, %Y, %I:%M%p IST")}', inline=False)
        emb.add_field(name="Guild ID", value=f"`{ctx.guild.id}`", inline=False)
        emb.set_thumbnail(url=ctx.guild.icon_url)
        emb.set_footer(text=f"Invoked by {ctx.author}", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=emb)

def setup(bot):
    bot.add_cog(pterostats(bot))