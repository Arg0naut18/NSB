import discord
from discord.ext import commands
import asyncio


class errors(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if hasattr(ctx.command, 'on_error'):
            return
        if isinstance(error, commands.MissingPermissions):
            respo = await ctx.reply("You do not have the permission to execute this command.")
            await asyncio.sleep(10)
            await ctx.message.delete()
            await respo.delete()
        elif isinstance(error, commands.MissingRequiredArgument):
            respo = await ctx.reply("Please enter all the required arguments.")
            print(error)
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
            respo = await ctx.reply("Something went wrong <a:hmmm:858583304021868554>! Are you sure all your arguments ||(inputs)|| are correct?")
            await asyncio.sleep(10)
            await respo.delete()
            raise error
        elif isinstance(error, commands.NotOwner):
            respo = await ctx.reply("You do not have the permission to execute this command.")
            await asyncio.sleep(10)
            await ctx.message.delete()
            await respo.delete()
        elif isinstance(error, discord.errors.Forbidden):
            respo = await ctx.reply("Please check that the role of the bot has to be higher than the role it's alloting.")
            await asyncio.sleep(10)
            await ctx.message.delete()
            await respo.delete()
        elif isinstance(error, commands.CommandOnCooldown):
            trash, time = str(error).split("Try again in ")
            respo = await ctx.reply(f"Chill dude. You can use this command again in `{time}`.")
            await asyncio.sleep(10)
            await respo.delete()
        elif isinstance(error, commands.NSFWChannelRequired):
            respo = await ctx.reply(f"This command is NSFW. Try it in an NSFW marked channel.")
            await asyncio.sleep(10)
            await respo.delete()    
        else:
            raise error


async def setup(bot):
    await bot.add_cog(errors(bot))