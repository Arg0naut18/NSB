#import gevent.monkey
#gevent.monkey.patch_all()
import discord
from discord.ext import commands
import urllib.request
from bs4 import BeautifulSoup
from python_aternos import Client

class mcraft(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['tame', 'iaf', 'fireandice'])
    async def iceandfire(self, ctx, *, query=None):
        if query is None:
            return
        try:
            if " " in query:
                q = query.replace(" ", "_")
            else:
                q = query
            link = f"https://ice-and-fire-mod.fandom.com/wiki/{q.title()}"    
            r = urllib.request.urlopen(link)
        except Exception as e:
            await ctx.send("`Entity not found!`")
            print(e)
            return
        soup = BeautifulSoup(r, "lxml")
        description = soup.find(property="og:description")
        desc = description.prettify()[15:-29]
        Description = desc.split(".")[0]+"."
        tameembed = discord.Embed(title=f"__**{query.title()}**__", color=0x00ff00)
        imageurl = soup.find("a", class_="image image-thumbnail").img['src']
        tameembed.set_image(url=imageurl)
        tameembed.add_field(name="Description", value=Description, inline=False)
        try:
            #text2 = "spawn"
            spawn = soup.find_all(lambda tag: tag.name == "p" and "spawn" in tag.text.lower())[1].text
            tameembed.add_field(name="Spawning", value=spawn, inline=False)
        except:
            tameembed.add_field(name="Spawning", value="This entity cannot be spawned.", inline=False)
        try:
            #text1 = "tame"
            tame = soup.find_all(lambda tag: tag.name == "p" and ("tame" in tag.text.lower() or "befriend" in tag.text.lower()))[0].text
            tameembed.add_field(name="Taming", value=tame, inline=False)
        except:
            tameembed.add_field(name="Taming", value="This entity cannot be tamed.", inline=False)
        try:
            breed = soup.find_all(lambda tag: tag.name == "p" and "breed" in tag.text.lower())[0].text
            tameembed.add_field(name="Breeding", value=breed, inline=False)
        except:
            tameembed.add_field(name="Breeding", value="This entity cannot be bred.", inline=False)
        tameembed.add_field(name="Further Info", value=link, inline=False)    
        await ctx.send(embed=tameembed)
    
    @commands.command()
    async def startserver(self, ctx, username, passd, server_number=0):
        if passd.startswith("md5"):
            passd = passd[4:]
            aternos = Client(username, md5=passd)
        else:
            aternos = Client(username, password=passd)
        servers = aternos.servers
        main_server = servers[server_number]
        main_server.start()
        await ctx.send(f"Starting `{main_server.address}`! Keep an eye out on the server as it might ask for confirmation during startup sometimes.")
        
    @commands.command(aliases=['closeserver'])
    async def stopserver(self, ctx, username, passd, server_number=0):
        if passd.startswith("md5"):
            passd = passd[4:]
            aternos = Client(username, md5=passd)
        else:
            aternos = Client(username, password=passd)
        servers = aternos.servers
        main_server = servers[server_number]
        main_server.stop()
        await ctx.send(f"Stoping `{main_server.address}`")
        
    @commands.command(aliases=['minecraftwiki', 'mcraftwiki'])
    async def mcraft(self, ctx, *, query=None):
        if query is None:
            return
        try:
            if " " in query:
                q = query.replace(" ", "_")
            else:
                q = query
            link = f"https://minecraft.fandom.com/wiki/{q.title()}"    
            r = urllib.request.urlopen(link)
        except Exception as e:
            await ctx.send("`Entity not found!`")
            print(e)
            return
        soup = BeautifulSoup(r, "lxml")
        description = soup.find(property="og:description")
        desc = description.prettify()[15:-29]
        Description = desc.split(".")[0]+"."
        tameembed = discord.Embed(title=f"__**{query.title()}**__", color=0x00ff00)
        try:
            imageurl = soup.find("a", class_="image").img['data-src']
        except:
            imageurl = soup.find("a", class_="image").img['src']
        tameembed.set_image(url=imageurl)
        tameembed.add_field(name="Description", value=Description, inline=False)
        try:
            #text2 = "spawn"
            spawn = soup.find_all(lambda tag: tag.name == "p" and "spawn" in tag.text.lower())[1].text
            tameembed.add_field(name="Spawning", value=spawn, inline=False)
        except:
            tameembed.add_field(name="Spawning", value="This entity cannot be spawned.", inline=False)
        try:
            #text1 = "tame"
            tame = soup.find_all(lambda tag: tag.name == "p" and ("tame" in tag.text.lower() or "befriend" in tag.text.lower()))[0].text
            tameembed.add_field(name="Taming", value=tame, inline=False)
        except:
            tameembed.add_field(name="Taming", value="This entity cannot be tamed.", inline=False)
        try:
            breed = soup.find_all(lambda tag: tag.name == "p" and "breed" in tag.text.lower())[0].text
            tameembed.add_field(name="Breeding", value=breed, inline=False)
        except:
            tameembed.add_field(name="Breeding", value="This entity cannot be bred.", inline=False)
        tameembed.add_field(name="Further Info", value=link, inline=False)
        await ctx.send(embed=tameembed)
    
    @startserver.error
    async def serverNotFound(self, ctx, error):
        if isinstance(error, commands.CommandInvokeError):
            await ctx.send(f"I guess the server wasn't found. Please make sure you input the right username and password.\nError:\n`{error}`")
            
    @stopserver.error
    async def serverNotRunning(self, ctx, error):
        if isinstance(error, commands.CommandInvokeError):
            await ctx.send(f"I guess the server isn't ON at the moment.\nError:\n`{error}`")        
    
async def setup(bot):
    await bot.add_cog(mcraft(bot))