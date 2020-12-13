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
        botn = await self.bot.fetch_user("763700343137239070")
        owner = await self.bot.fetch_user("436844058217021441")
        if isinstance(channel, discord.channel.DMChannel):
            if msg.author != botn and msg.author != owner:
                await self.bot.process_commands(msg)
                # print(msg)
                emb = discord.Embed(title="Message recieved!", color = color_main)
                emb.add_field(name="Message:", value=msg.content, inline=False)
                emb.add_field(name="Member ID:", value=msg.author.id, inline=False)
                emb.set_footer(text=f"Message by {msg.author}",icon_url=msg.author.avatar_url)
                try:
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
            await asyncio.sleep(2)
            await ctx.channel.purge(limit=2)
        except:
            await ctx.send("Failed to send mssg!")

    @commands.command()
    async def reply(self, ctx, memberid, *, mssg):
        color_main = color[random.randint(0, len(color)-1)]
        try:
            member = await self.bot.fetch_user(memberid)
            # emb = discord.Embed(title=mssg, color=color_main)
            # emb.add_field(name="Message:", value=mssg, inline=False)
            await member.send(f"{member.name}: {mssg}")
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
