import discord
from discord.ext import commands
import random
from .Main.__init__ import Anilist
anilist = Anilist()
import re
import requests
from bs4 import BeautifulSoup

CLEANR = re.compile('<.*?>') 

color = [15158332, 3066993, 10181046, 3447003, 1752220, 15844367]

async def listToStr(l):
    str1 = ', '.join([str(elem) for elem in l])
    return "`"+str1+"`"

async def cleanText(s):
    clear = re.sub(CLEANR, '', s)
    return clear

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
    return f'`{days}d {hours}h {minutes}m {seconds}s`'

async def toCorrectDateFormat(date):
    month, day, year = date.split('/')
    return f'`{day}/{month}/{year}`'

class trans(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["animename"])
    async def anime(self, ctx, *, name):
        anime = anilist.get_anime(name)
        if(anime==None):
            await ctx.reply("Anime not found!")
            return
        color_main = color[random.randint(0, len(color)-1)]
        embed = discord.Embed(title=f"{anime['name_english']}", color=color_main, description=f"{(await cleanText(anime['desc']))[:500]+'...'}", url=f'https://anilist.co/anime/{anilist.get_anime_id(anime["name_romaji"])}')
        embed.set_thumbnail(url=anime['cover_image'])
        embed.add_field(name="Original/Japanese Name", value="`"+anime["name_romaji"]+"`", inline = False)
        embed.add_field(name="Score", value="`"+str(anime['average_score'])+"`", inline=True)
        embed.add_field(name="Genre", value=await listToStr(anime['genres']), inline=True)
        embed.add_field(name="Started Airing", value = await toCorrectDateFormat(anime['starting_time']), inline=False)
        embed.add_field(name="Last Airing", value = await toCorrectDateFormat(anime['ending_time']), inline=False)
        embed.add_field(name="Episodes", value = "`"+str(anime['airing_episodes'])+"`", inline=False)
        embed.add_field(name="Status", value = "`"+str(anime['airing_status'])+"`", inline=True)
        if(anime['airing_status']=="RELEASING"):
            embed.add_field(name="Aired Episodes", value = "`"+str(anime['next_airing_ep']['episode'])+"`", inline=True)
            embed.add_field(name="Next Episode airing in", value = await toReadableTime(anime['next_airing_ep']['timeUntilAiring']), inline=True)
        try:
            embed.set_image(url=anime['banner_image'])
        except:
            pass
        await ctx.reply(embed=embed)

    @commands.command(aliases=["manganame"])
    async def manga(self, ctx, *, name):
        anime = anilist.get_manga(name)
        if(anime==None):
            await ctx.reply("Manga not found!")
            return
        color_main = color[random.randint(0, len(color)-1)]
        embed = discord.Embed(title=f"{anime['name_english']}", color=color_main, description=f"{(await cleanText(anime['desc']))[:500]+'...'}", url=f'https://anilist.co/manga/{anilist.get_manga_id(anime["name_romaji"])}')
        embed.set_thumbnail(url=anime['cover_image'])
        embed.add_field(name="Original/Japanese Name", value="`"+anime["name_romaji"]+"`", inline = False)
        embed.add_field(name="Score", value="`"+str(anime['average_score'])+"`", inline=True)
        embed.add_field(name="Genre", value=await listToStr(anime['genres']), inline=True)
        embed.add_field(name="Started Publishing", value = await toCorrectDateFormat(anime['starting_time']), inline=False)
        embed.add_field(name="Last Publishing", value = await toCorrectDateFormat(anime['ending_time']), inline=False)
        embed.add_field(name="Chapters", value = "`"+str(anime['chapters'])+"`", inline=False)
        embed.add_field(name="Volumes", value = "`"+str(anime['volumes'])+"`", inline=False)
        embed.add_field(name="Status", value = "`"+str(anime['release_status'])+"`", inline=True)
        try:
            embed.set_image(url=anime['banner_image'])
        except:
            pass
        await ctx.reply(embed=embed)

    @commands.command(aliases=["animeranks"])
    async def anime_rank(self, ctx):
        url = 'https://anilist.co/search/anime/trending'
        site = requests.get(url)
        color_main = color[random.randint(0, len(color)-1)]
        soup = BeautifulSoup(site.content, "html.parser")
        dict = soup.find_all('a', class_="title")
        embed = discord.Embed(title=f"Top 10 Trending Anime", color=color_main, url=url)
        l = []
        for link in dict:
            name = link.text
            name = name.replace("\n", "")
            l.append(name)
        for i in range(min(10, len(l))):
            embed.add_field(name='\u200b', value=f"[{str(i+1)} -> {l[i]}](https://anilist.co/anime/{anilist.get_anime_id(l[i])})", inline=False)

def setup(bot):
    bot.add_cog(trans(bot))