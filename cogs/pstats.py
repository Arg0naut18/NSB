import discord
from discord import app_commands
from discord.ext import commands
import random
import json
import sys
import psutil
import os
from pytz import timezone


class pterostats(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        
    @commands.hybrid_command(name="pstats", description='Shows the server status', with_app_commands=True)
    @commands.is_owner()
    @app_commands.guilds(discord.Object(id=743741348578066442))
    async def pstats(self, ctx):
        member_count = len(self.bot.users)
        emb = discord.Embed(title="Panel Status", color=random.randint(0x000000, 0xFFFFFF))
        emb.add_field(name="Memory Usage", value=f"`{psutil.Process(os.getpid()).memory_info().rss / 1024 ** 2} MB`", inline=True)
        emb.add_field(name="CPU Usage", value=f"`{psutil.cpu_percent(interval=0.5)}%`", inline=True)
        emb.add_field(name="Ping / Latency", value=f"`{round(self.bot.latency*1000)} ms`", inline=True)
        emb.add_field(name="Python Version", value=f"`{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}`", inline=True)
        emb.add_field(name="Discord.py Version", value=f"`{discord.__version__}`", inline=True)
        emb.add_field(name="Servers", value=f"`{len(self.bot.guilds)}`", inline=True)
        emb.add_field(name="Members", value=f"`{member_count}`", inline=True)
        emb.add_field(name="VCs connected", value=f"`{len(self.bot.voice_clients)}`", inline=True)
        await ctx.send(embed=emb)
    
    @commands.command(aliases=['gstats', 'guild'])
    @commands.has_permissions(administrator=True)
    async def guildstats(self, ctx, guildid=None):
        if guildid is None:
            guild = ctx.guild
        else:
            guild = self.bot.get_guild(guildid)
        creationdate = guild.created_at
        creation = creationdate.replace(tzinfo=timezone('UTC')).astimezone(timezone('Asia/Kolkata'))
        online = 0
        offline = 0
        away = 0
        dnd = 0
        for member in guild.members:
            if str(member.status)=="online":
                online += 1
            elif str(member.status)=="dnd":
                dnd += 1
            elif member.status=="idle":
                away += 1
            else:
                offline += 1
        banned_users = await guild.bans()
        emb = discord.Embed(title=f"{guild.name}'s Status", color=0x00FF00)
        emb.add_field(name="Name", value=f"{guild.name}", inline=False)
        emb.add_field(name="Members", value=f"`{len([m for m in guild.members if not m.bot])}`", inline=True)
        emb.add_field(name="Bots", value=f"`{len([m for m in guild.members if m.bot])}`", inline=True)
        emb.add_field(name="Region", value=f"{guild.region}".title(), inline=True)
        emb.add_field(name="Banned Members", value=f"`{len(banned_users)}`", inline=True)
        emb.add_field(name="Member Status", value=f":green_circle:`{online}` :red_circle:`{dnd}` :orange_circle:`{away}` :white_circle:`{offline}`", inline=False)
        emb.add_field(name="Created At", value=f'{creation.strftime("%a, %b %d, %Y, %I:%M%p IST")}', inline=False)
        emb.add_field(name="Guild ID", value=f"`{guild.id}`", inline=False)
        emb.set_thumbnail(url=guild.icon_url)
        emb.set_footer(text=f"Invoked by {ctx.author}", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=emb)

    @commands.command()
    async def testcustom(self, ctx, emoji: discord.Emoji=None):
        try:
            await ctx.send(f"{emoji.id}")
        except Exception:
            pass
        
    @commands.command()
    async def testname(self, ctx, member_id):
        try:
            member = discord.utils.get(self.bot.textchannels, id=member_id)
            await ctx.send(f"{member.name}")
        except Exception:
            pass
        
    @commands.command()
    async def testgroup(self, ctx, group: discord.GroupChannel):
        await ctx.send(f"You are in {group.name}. This group has {len(group.recipients)}")
        
async def setup(bot):
    await bot.add_cog(pterostats(bot))