import discord
from discord.ext import commands
import random
import asyncio


class errors(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            respo = await ctx.reply("You do not have the permission to execute this command.")
            await asyncio.sleep(10)
            await ctx.message.delete()
            await respo.delete()
        elif isinstance(error, commands.MissingRequiredArgument):
            respo = await ctx.reply("Please enter all the required arguments.")
            await asyncio.sleep(10)
            await ctx.message.delete()
            await respo.delete()
        elif isinstance(error, commands.CommandNotFound):
            # respo = await ctx.reply("Are you sure that is the right command?")
            # await asyncio.sleep(10)
            # await respo.delete()
            pass
        elif isinstance(error, commands.MissingRole):
            respo = await ctx.reply("You do not have the role to execute this command.")
            await asyncio.sleep(10)
            await respo.delete()
        elif isinstance(error, commands.CommandInvokeError):
            respo = await ctx.reply("Something went wrong! Are you sure all your arguments ||(inputs)|| are correct?")
            await asyncio.sleep(10)
            await respo.delete()
            raise error
        else:
            raise error


def setup(bot):
    bot.add_cog(errors(bot))