import discord
from discord.ext import commands
import asyncio
from utils.logger import send_error_message


class errors(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if hasattr(ctx.command, 'on_error'):
            return
        if isinstance(error, commands.MissingPermissions) or isinstance(error, commands.NotOwner):
            await send_error_message(ctx, "You do not have the permission to execute this command.")
        elif isinstance(error, commands.MissingRequiredArgument):
            await send_error_message(ctx, "Please enter all the required arguments.")
        elif isinstance(error, commands.MissingRole):
            await send_error_message(ctx, "You do not have the role to execute this command.")
        elif isinstance(error, commands.CommandInvokeError):
            await send_error_message(ctx, "Something went wrong <a:hmmm:858583304021868554>! Are you sure all your arguments ||(inputs)|| are correct?", error=error)
        elif isinstance(error, discord.errors.Forbidden):
            await send_error_message(ctx, "Please check that the role of the bot has to be higher than the role it's alloting.")
        elif isinstance(error, commands.CommandOnCooldown):
            await send_error_message(ctx, f"Chill dude. You can use this command again in `{str(error).split('Try again in ')[1]}`.")
        elif isinstance(error, commands.NSFWChannelRequired):
            await send_error_message(ctx, "This command is NSFW. Try it in an NSFW marked channel.")  
        else:
            raise error


async def setup(bot):
    await bot.add_cog(errors(bot))