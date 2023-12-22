from discord.ext import commands
import logging 


class LoggerClass:
	logging.basicConfig(filename="./std.log", 
						format='%(asctime)s %(message)s', 
						filemode='w')
	logger=logging.getLogger() 
	logger.setLevel(logging.DEBUG)

logger_instance = LoggerClass()

async def send_error_message(ctx: commands.Context, message, ephemeral=True) -> bool:
    logger_instance.logger.debug(message)
    xd = await ctx.reply(message, ephemeral=ephemeral)
    return False
