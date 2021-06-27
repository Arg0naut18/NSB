import discord
from discord.ext import commands
import random
import requests 
from bs4 import BeautifulSoup 
    
def getdata(url): 
    r = requests.get(url) 
    return r.text 

async def get_fox_image(url):   
    htmldata = getdata(url) 
    soup = BeautifulSoup(htmldata, 'html.parser') 
    # for item in soup.find_all('img'):
    #     return item['src']
    return soup.find_all('img')[1]['src']

async def get_image(url):   
    htmldata = getdata(url) 
    soup = BeautifulSoup(htmldata, 'html.parser') 
    for item in soup.find_all('img'):
        return item['src']

class animals(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def fox(self, ctx):
        q = random.randint(1,123)
        foxembed = discord.Embed(title="Here is a foxie for you!", color=0x00FF00)
        url = await get_fox_image(f"https://randomfox.ca/?i={q}")
        foxembed.set_image(url=url)
        foxembed.set_footer(text=f"Invoked by {ctx.author}", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=foxembed)
    
    @commands.command()
    async def wolf(self, ctx):
        q = random.randint(1,123)
        foxembed = discord.Embed(title="Here is a wolf for you!", color=0x00FF00)
        url = await get_image(f"https://source.unsplash.com/800x450/?wolf")
        foxembed.set_image(url=url)
        foxembed.set_footer(text=f"Invoked by {ctx.author}", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=foxembed)
    
def setup(bot):
    bot.add_cog(animals(bot))