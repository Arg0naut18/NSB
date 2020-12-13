import discord
import periodic
from periodic.table import element
import random
from discord.ext import commands
import json
import wikipedia

color = [15158332, 3066993, 10181046, 3447003, 1752220, 15844367]

# attributes = ['atomic', 'symbol', 'name', 'mass']


class atom(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
     
    @commands.command(aliases = ["pt"])
    async def atom(self, ctx, elem1):
        color_main = color[random.randint(0, 5)]
        try:
            elem = element(elem1.lower())
            res = wikipedia.page(title = elem, auto_suggest=True)
            embed = discord.Embed(title=f'__{elem1.title()}__', color=color_main)
            embed.add_field(name="Symbol", value=f'`{elem.symbol}`', inline=True)
            embed.add_field(name="Element", value=f'`{elem1.title()}`', inline=True)
            embed.add_field(name="Atomic no.", value=f'`{elem.atomic}`', inline=True)
            embed.add_field(name="Atomic mass", value=f'`{elem.mass}`', inline=True)
            embed.add_field(name="Wikipedia Link", value=f'{res.url}', inline = False)
            await ctx.send(embed=embed)
        except Exception as e:
            await ctx.send("Error loading database! Please check the element.")

def setup(bot):
    bot.add_cog(atom(bot))
