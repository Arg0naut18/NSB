#import gevent.monkey
#gevent.monkey.patch_all()
import discord
from discord.ext import commands
import urllib.request
from bs4 import BeautifulSoup

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
            r = urllib.request.urlopen(f"https://ice-and-fire-mod.fandom.com/wiki/{q.title()}")
        except Exception as e:
            await ctx.send("`Entity not found!`")
            print(e)
            return
        soup = BeautifulSoup(r, "html.parser")
        description = soup.find(property="og:description")
        desc = description.prettify()[15:-29]
        Description = desc.split(".")[0]+"."
        tameembed = discord.Embed(title=f"{query.title()}", color=0x00ff00)
        tameembed.add_field(name="Description", value=Description, inline=False)
        try:
            taming = soup.find_all("p", string=lambda text: text and ("tamed" in text.lower() or "befriended" in text.lower()))
            tame = str(taming[0])[3:-4]
            tameembed.add_field(name="Taming", value=tame, inline=False)
        except:
            pass
        imagethumb = soup.find("a", class_="image image-thumbnail")
        imageurlstart = str(imagethumb).find("href=")
        imageurlend = str(imagethumb).find(" title")
        imageurl = str(imagethumb)[imageurlstart+6:imageurlend-1]
        tameembed.set_image(url=imageurl)
        await ctx.send(embed=tameembed)
        
    @commands.command(aliases=['minecraftwiki', 'mcraftwiki'])
    async def mcraft(self, ctx, *, query=None):
        if query is None:
            return
        try:
            if " " in query:
                q = query.replace(" ", "_")
            else:
                q = query
            r = urllib.request.urlopen(f"https://minecraft.fandom.com/wiki/{q.title()}")
        except Exception as e:
            await ctx.send("`Entity not found!`")
            print(e)
            return
        soup = BeautifulSoup(r, "html.parser")
        description = soup.find(property="og:description")
        desc = description.prettify()[15:-29]
        Description = desc.split(".")[0]+"."
        tameembed = discord.Embed(title=f"{query.title()}", color=0x00ff00)
        tameembed.add_field(name="Description", value=Description, inline=False)
        try:
            taming = soup.find_all("p", string=lambda text: text and ("tamed" in text.lower() or "befriended" in text.lower()))
            tame = str(taming[0])[3:-4]
            tameembed.add_field(name="Taming", value=tame, inline=False)
        except:
            pass
        imagethumb = soup.find("a", class_="image")
        imageurlstart = str(imagethumb).find("href=")
        imageurlend = str(imagethumb).find(" title")
        imageurl = str(imagethumb)[imageurlstart+6:imageurlend-1]
        tameembed.set_image(url=imageurl)
        await ctx.send(embed=tameembed)
            
def setup(bot):
    bot.add_cog(mcraft(bot))