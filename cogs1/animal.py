import discord
from discord.ext import commands
import random
import httpx
from bs4 import BeautifulSoup
import asyncio

async def getdata(url):
    client = httpx.AsyncClient()
    reqs=await asyncio.gather(*[client.get(url)])
    await client.aclose()
    for req in reqs:
        return req.text

async def get_fox_image(url):   
    htmldata = await getdata(url) 
    soup = BeautifulSoup(htmldata, 'html.parser') 
    # for item in soup.find_all('img'):
    #     return item['src']
    return soup.find_all('img')[1]['src']

async def get_image(url):   
    htmldata = await getdata(url) 
    soup = BeautifulSoup(htmldata, 'html.parser') 
    image_srcs = []
    for item in soup.find_all('img'):
        image_srcs.append(item['src'])
    return random.choice(image_srcs)

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
        url = await get_image(f"https://source.unsplash.com/1600x900/?wolf")
        foxembed.set_image(url=url)
        foxembed.set_footer(text=f"Invoked by {ctx.author}", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=foxembed)
    
def setup(bot):
    bot.add_cog(animals(bot))