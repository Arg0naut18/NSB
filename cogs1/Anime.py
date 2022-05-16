import discord
from discord.ext import commands
import random
from Main.__init__ import Anilist
import asyncio

color = [15158332, 3066993, 10181046, 3447003, 1752220, 15844367]

async def listToStr(l):
    str1 = ','.join([str(elem) for elem in l])
    return str1

async def toReadableTime(seconds):
    '''
    Converts seconds to a readable time.

    :param seconds: The number of seconds to be converted
    :return: The converted time
    :rtype: str
    '''
    seconds = int(seconds)
    days = seconds // 86400
    hours = (seconds // 3600)%24
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60
    return f'{days}d {hours}h {minutes}m {seconds}s'

class trans(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["tr"])
    async def anime(self, ctx, *, name):
        anilist = Anilist()
        anime = anilist.get_anime(name)
        color_main = color[random.randint(0, len(color)-1)]
        embed = discord.Embed(title=f"{anime['name_english']}", color=color_main, description=f"{anime['desc']}")
        embed.set_thumbnail(url=anime['cover_image'])
        embed.add_field(name="Score", value=anime['average_score'], inline=False)
        embed.add_field(name="Genre", value=listToStr(anime['genres']), inline=True)
        embed.add_field(name="Started Airing", value=anime['starting_time'], inline=False)
        embed.add_field(name="Last Airing", value=anime['ending_time'], inline=True)
        embed.add_field(name="Episodes", value = anime['airing_episodes'], inline=False)
        embed.add_field(name="Status", value = anime['airing_status'], inline=True)
        if(anime['airing_status']=="RELEASING"):
            embed.add_field(name="Aired Episodes", value = anime['next_airing_ep']['episode'], inline=False)
            embed.add_field(name="Next Episode airing in", value = toReadableTime(anime['next_airing_ep']['time_until_airing']), inline=True)
        embed.set_image(url=anime['banner_image'])
        await ctx.reply(embed=embed)

def setup(bot):
    bot.add_cog(trans(bot))