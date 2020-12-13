import discord
import urbandict
from discord.ext import commands
import random

color = [15158332, 3066993, 10181046, 3447003, 1752220, 15844367]


class dict(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases = ["ud", "dictionary"])
    async def dict(self, ctx, word):
        color_main = color[random.randint(0, 5)]
        query = urbandict.define(word)
        res = query[0]
        embed = discord.Embed(title=f"{res['word']}", color=color_main)
        embed.add_field(name="Definition", value=str(res["def"]), inline=False)
        embed.add_field(name="Example", value=str(res["example"]), inline=False)
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(dict(bot))
