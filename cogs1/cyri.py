import discord
from discord.ext import commands, tasks
import requests
from bs4 import BeautifulSoup
import re


class cyri(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['canyourunit', 'canirunit', 'ciri'])
    async def cyri(self, ctx, *, game_name):
        game_name = game_name.lower().strip()
# game_name = ''.join(char for char in game_name if char.isalnum())
        game_name = re.sub(r'[^a-zA-Z0-9 ]+', '', game_name)
        if(game_name == ''): 
            await ctx.send("Please enter a game name!")
            return
        game_name = game_name.replace('gta', 'grand theft auto ')
        actual_name = game_name.title()
        game_name = game_name.replace(" ", "-")
        req = requests.get(f"https://www.pcgamebenchmark.com/{game_name}-system-requirements").content.decode("utf-8")
        soup = BeautifulSoup(req, "html.parser")
        contents = soup.find_all("ul", class_ = "bb_ul")
        titles = soup.find_all("h2", class_ = "requirement-title")
        # recC = contents[0].get_text()
        # minC = contents[1].get_text()
        embed = discord.Embed(title=f"{actual_name.title()} System Requirements", color=0x00ff00)
        for i in range(2):
            embed.add_field(name=titles[i].get_text().title(), value="```"+contents[i].get_text()+"```", inline=False)
        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(cyri(bot))