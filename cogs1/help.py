import discord
from discord.ext import commands
import random

color = [15158332, 3066993, 10181046, 3447003, 1752220, 15844367]


class help(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def help(self, ctx):
        msg = "·sol (solve equations upto 3 variables)\n`sci sol x+y-3 x-y-1`\n\n·differentiate\n`sci derivate x^2+2x+1`\n\n·integrate\n`sci integrate x^2+2x+1`\n\n·atom\n`sci atom Uranium`\n\n·wiki\n`sci wiki Uranium`\n\nType `sci dc` to join our official discord server if you have any suggestions or need further help.\nThank You!"
        color_main = color[random.randint(0, 5)]
        embed = discord.Embed(
            title="__**Scicord command list:**__", description=msg, color=color_main)
        await ctx.send(embed=embed)

    @commands.command(aliases=['discord'])
    async def dc(self, ctx):
        await ctx.send(f"{ctx.author.mention} Thanks for your concern! Please join our discord server.\nhttps://discord.gg/yDjSeEj")


def setup(bot):
    bot.add_cog(help(bot))
