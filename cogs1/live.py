import discord
from discord.ext import commands, tasks
import grequests
import time

class checklive(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.is_live.start()

    @tasks.loop(seconds=120)
    async def is_live(self):
        channel = self.bot.get_channel(865131861179891732)
        channelName = 'kiash_d'
        channelstats = grequests.get('https://www.twitch.tv/'+channelName).content.decode('utf-8')
        if 'isLiveBroadcast' in channelstats:
            await channel.send(channelName + ' is live!\nhttps://www.twitch.tv/'+channelName)

def setup(bot):
    bot.add_cog(checklive(bot))