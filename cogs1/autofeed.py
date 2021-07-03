import discord
from discord.ext import commands, tasks
import asyncio
from datetime import datetime, timedelta
from pytz import timezone

class autofeed(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.my_task.start()

    @tasks.loop(hours=24)
    async def my_task(self):
        channel = self.bot.get_channel(764169003051778058)
        await channel.send("@everyone Get ready.")

    @my_task.before_loop
    async def before_my_task(self):
        hour = 13
        minute = 45
        await self.bot.wait_until_ready()
        now = datetime.now(timezone('Asia/Kolkata'))
        future = datetime(now.year, now.month, now.day, hour, minute)
        if now.hour >= hour and now.minute > minute:
            future += timedelta(days=1)
        await asyncio.sleep((future-now).seconds)

    

def setup(bot):
    bot.add_cog(autofeed(bot))