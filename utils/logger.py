from discord.ext import commands
import logging 


class LoggerClass:
	logging.basicConfig(filename="./std.log", 
						format='%(asctime)s %(message)s', 
						filemode='w')
	logger=logging.getLogger()
	logger.setLevel(logging.DEBUG)

logger_instance = LoggerClass()

async def send_error_message(ctx: commands.Context, message, ephemeral=True, error=None) -> bool:
    await ctx.reply(message, ephemeral=ephemeral)
    logger_instance.logger.debug(message)
    if error:
          raise error
    return False
