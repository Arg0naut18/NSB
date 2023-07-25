import discord
import math
import matplotlib.pyplot as plt
import os
import numpy as np
from sympy import *
from discord.ext import commands


class graph(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases = ["graph"])
    async def draw(self, ctx, xvals, yvals):
        xList = []
        yList = []
        for varx in xvals:
            xList.append(varx)
        for vary in yvals:
            yList.append(vary)
        # xList.sort()
        # yList.sort()
        x = np.array(xList)
        y = np.array(yList)
        arr = np.stack((x, y))
        # xdata = np.arange(0, 10, 1)
        # ydata = np.arange(0, 10, 1)
        y = int(y)
        for i in range(0, 2, 1):
            plt.plot(x, y)
        plt.title(f'{ctx.message.author}\'s Graph')
        plt.savefig(fname='plot')
        await ctx.send(file=discord.File('plot.png'))
        os.remove('plot.png')
        plt.clf()

    @commands.command()
    async def plot(self, ctx, expr):
        x1 = np.arange(-10, 10, 1)
        x = symbols('x')
        y=symbols('y')
        if "^" in expr:
            expr = expr.replace("^", "**")
        expr = solveset(expr, x)
        plt.plot(x1, expr)
        plt.title(f'{ctx.message.author}\'s Graph')
        plt.savefig(fname='plot')
        await ctx.send(file=discord.File('plot.png'))
        os.remove('plot.png')
        plt.clf()

def setup(bot):
    bot.add_cog(graph(bot))
