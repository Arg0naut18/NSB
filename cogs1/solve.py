import discord
import matplotlib.pyplot as plt
import os
import numpy as np
from sympy import *
# from __future__ import division
from sympy.solvers import solve
from discord.ext import commands


class solve(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def sol(self, ctx, eq1, eq2 = None, eq3 = None):
        if eq2 is None and eq3 is None:
            x = symbols('x')
            k, m, n = symbols('k m n', integer=True)
            f, g, h = symbols('f g h', cls=Function)
            if "^" in eq1:    
                eq1 = eq1.replace("^", "**")
            try:
                equ1 = solveset(eq1,x)
                # res = str(equ1)
                await ctx.send(f'`{equ1}`')
                # print(res)
            except Exception as e:
                print(e)
                await ctx.send("Can't solve this question!")
        elif eq3 is None:
            x, y = symbols('x y')
            if "^" in eq1:    
                eq1 = eq1.replace("^", "**")
            if "^" in eq2:    
                eq2 = eq2.replace("^", "**")
            try:
                # exp1 = Eq(e1, 0)
                # exp2 = Eq(e2, 0)
                sol = linsolve((eq1, eq2), (x, y))
                await ctx.send(f'`{sol}`')
            except Exception as e:
                print(e)
                await ctx.send("Can't solve this question!")
        else:
            x, y, z = symbols('x y z')
            if "^" in eq1:
                eq1 = eq1.replace("^", "**")
            if "^" in eq2:
                eq2 = eq2.replace("^", "**")
            if "^" in eq3:
                eq3 = eq3.replace("^", "**")
            try:
                sol = linsolve((eq1, eq2, eq3), (x, y, z))
                await ctx.send(f'`{sol}`')
            except Exception as e:
                print(e)
                await ctx.send("Can't solve this question!")

def setup(bot):
    bot.add_cog(solve(bot))
