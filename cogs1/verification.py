import discord
from discord.ext import commands
import random
import asyncio
from discord.utils import get

color = [15158332, 3066993, 10181046, 3447003, 1752220, 15844367]

class verification(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context = True)
    async def verify(self, ctx):
        if ctx.message.channel.id == 764073807627157515:
            member = ctx.message.author
            role = get(ctx.guild.roles, name = "members")
            await member.add_roles(role)
            msg = await ctx.send(f"Congratulations! {member.mention} is now verified :thumbup:")
            await asyncio.sleep(4)
            await msg.delete()
            await ctx.channel.purge(limit=1)
        else:
            msg = await ctx.send("Can't verify here! please type in #verification")
            await asyncio.sleep(4)
            await msg.delete()

def setup(bot):
    bot.add_cog(verification(bot))
