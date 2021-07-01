import discord
from discord import channel
from discord.abc import PrivateChannel
from discord.channel import DMChannel
# from discord import channel
# from discord.embeds import Embed
from discord.ext import commands
from discord import TextChannel
import random
from discord.ext.commands import has_permissions, MissingPermissions
from discord.utils import get
import asyncio

color = [15158332, 3066993, 10181046, 3447003, 1752220, 15844367]


class dm(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, msg):
        color_main = color[random.randint(0, len(color)-1)]
        channel = msg.channel
        botn = await self.bot.fetch_user("743741872039657492")
        owners = ["436844058217021441"]
        owner = await self.bot.fetch_user(owners[0])
        if isinstance(channel, discord.channel.DMChannel):
            if msg.author != botn and msg.author != owner and not msg.content.startswith('nsb'):
                await self.bot.process_commands(msg)
                # print(msg)
                emb = discord.Embed(title="Message recieved!", color = color_main)
                emb.add_field(name="Message:", value=msg.content, inline=False)
                emb.add_field(name="Member ID:", value=msg.author.id, inline=False)
                emb.set_footer(text=f"Message by {msg.author}",icon_url=msg.author.avatar_url)
                try:
                    for memid in owners:
                        owner = await self.bot.fetch_user(memid)
                        await owner.send(embed=emb)
                except:
                    pass

    @commands.command()
    async def dm(self, ctx, member: discord.Member, *, mssg):
        color_main = color[random.randint(0, len(color)-1)]
        try:
            emb = discord.Embed(title="Bot DM", color=color_main)
            emb.add_field(name="Message:", value=mssg, inline=False)
            emb.set_footer(
                text=f"Message by {ctx.author}", icon_url=ctx.author.avatar_url)
            await member.send(embed=emb)
            await ctx.send("Message has been sent!")
        except:
            await ctx.send("Failed to send mssg!")
        try:
            await asyncio.sleep(2)
            await ctx.channel.purge(limit=2)
        except:
            pass

    @commands.command()
    @commands.is_owner()
    async def reply(self, ctx, memberid: discord.Member, *, mssg):
        try:
            member = await self.bot.fetch_user(memberid)
            emb = discord.Embed(title=mssg, color=0x00FF00)
            # emb.add_field(name="Message:", value=mssg, inline=False)
            await member.send(embed=emb)
            await ctx.send("Message has been sent!")
            await asyncio.sleep(2)
            dmchannel = await ctx.author.create_dm()
            async for message in dmchannel.history(limit=1):
    		        if message.author == self.bot.user:
        			    await message.delete()
        except Exception as e:
            await ctx.send("Failed to send mssg!")
            print(e)

def setup(bot):
    bot.add_cog(dm(bot))