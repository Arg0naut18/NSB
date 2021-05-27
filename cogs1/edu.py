import discord
from discord.ext import commands
import random
from sympy import *
import math
import os
import numpy as np
# from __future__ import division
from sympy.solvers import solve

prev = 0

class edu(commands.Cog):

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

    @commands.command()
    async def sol(self, ctx, eq1, eq2=None, eq3=None):
        if eq2 is None and eq3 is None:
            x = symbols('x')
            k, m, n = symbols('k m n', integer=True)
            f, g, h = symbols('f g h', cls=Function)
            if "^" in eq1:
                eq1 = eq1.replace("^", "**")
            try:
                equ1 = solveset(eq1, x)
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
    
    @commands.command()
    async def calc(self, ctx, term1, op, term2=None):
        if term1 != "sqrt" and term1 != "log":
            term1 = int(term1)
        if term2 is not None and term2 is not "e":
            term2 = int(term2)
        if term2 == None:
            base = math.e
        else:
            base = term2
        if op == '+':
            result = term1 + term2
            await ctx.send(f"`{result}`")
        if op == '-':
            result = term1 - term2
            await ctx.send(f"`{result}`")
        if op == '*':
            result = term1 + term2
            await ctx.send(f"`{result}`")
        if op == '/':
            result = term1 / term2
            await ctx.send(f"`{result}`")
        if op == '^':
            result = term1 ** term2
            await ctx.send(f"`{result}`")
        if term1 == "sqrt":
            result = math.sqrt(int(op))
            await ctx.send(f"`{result}`")
        if term1 == "log":
            op = int(op)
            result = math.log(op, base)
            await ctx.send(f"`{result}`")

def setup(bot):
    bot.add_cog(edu(bot))