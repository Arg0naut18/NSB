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
        dict = soup.find_all('a', class_="title", limit=10)
        embed = discord.Embed(title=f"Top 10 Trending Anime", color=color_main)
        #l = []
        i=0
        digemoji = {
            '1':"<:digital1:975657333646561300>",
            '2':"<:digital2:975657333541707807>",
            '3':"<:digital3:975657333558501396>",
            '4':"<:digital4:975657333642371082>",
            '5':"<:digital5:975657333524938764>",
            '6':"<:digital6:975657333650751508>",
            '7':"<:digital7:975657333298458655>",
            '8':"<:digital8:975657333671751700>",
            '9':"<:digital9:975657333772410881>",
            '10':"<:digital1:975657333646561300><:digital0:975661653913911317>",
        }
        purpemoji={
            '1' : "<:purple1:975657279653306409>",
            '2' : "<:purple2:975657279674261605>",
            '3' : "<:purple3:975657279783317534>",
            '4' : "<:purple4:975657279904940113>",
            '5' : "<:purple5:975657280156598273>",
            '6' : "<:purple6:975657280013996143>",
            '7' : "<:purple7:975657280219541587>",
            '8' : "<:purple8:975657280240504832>",
            '9' : "<:purple9:975657280597024828>",
            '10' : "<:purple1:975657279653306409><:purple0:975657279858806784>"
        }
        for link in dict:
            name = link.text
            name = name.replace("\n", "")
            embed.add_field(name='\u200b', value=f"{purpemoji[str(i+1)]} -> [{name}](https://anilist.co/anime/{anilist.get_anime_id(name)})", inline=False)
            i+=1
        embed.add_field(name="\u200b", value=f"Data from [anilist.co]({url})", inline=False)
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(trans(bot))