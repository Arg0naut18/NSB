import discord
from discord.ext import commands
import random
from sympy import *

class calculus(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def derivate(self, ctx, expr, variable = "X"):
        y = symbols('x')
        if "^" in expr:
            expr = expr.replace("^", "**")
        d = Derivative(expr, y)
        res = d.doit()
        await ctx.send(f'`{res}`')

    @commands.command()
    async def integrate(self, ctx, expr, variable = "X"):
        y = symbols('x')
        if "^" in expr:
            expr = expr.replace("^", "**")
        d = integrate(expr, y)
        res = str(d).replace("**", "^")
        await ctx.send(f'`{res}+c`')

def setup(bot):
    bot.add_cog(calculus(bot))
