import discord
from discord.ext import commands
import random
import asyncio
import time
import json
import requests

color = [15158332, 3066993, 10181046, 3447003, 1752220, 15844367]

j_file = open("divinesecrets.txt")
vari = json.load(j_file)
j_file.close()
fillerApi = vari["fillerApi"]

class Currency_convertor:
    rates = 0
    def __init__(self, url):
        data = requests.request("GET", url, headers={"apikey":fillerApi}, data = {}).json()
        self.rates = data['info']['rate']

    def convert(self, from_currency, to_currency, amount):
        initial_amount = amount
        amount = round(amount * self.rates, 2)
        return ('{} {} = {} {}'.format(initial_amount, from_currency, amount, to_currency))

class splEmotes(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(description="Shows the bot latency", with_app_command=True)
    async def latency(self, ctx: commands.Context):
        time_1 = time.perf_counter()
        await ctx.trigger_typing()
        time_2 = time.perf_counter()
        ping = round((time_2-time_1)*1000)
        await ctx.send(f"ping : {ping}ms")
        await ctx.send(f"bot latency: {round(self.bot.latency*1000)}ms")

    @commands.hybrid_command(description="Converts currency", with_app_command=True)
    async def convert(self, ctx: commands.Context, money: int, CurrFrom: str, CurrTo: str):
        CurrFrom = CurrFrom.upper()
        CurrTo = CurrTo.upper()
        url = f"https://api.apilayer.com/fixer/convert?to={CurrTo}&from={CurrFrom}&amount={money}"
        c = Currency_convertor(url)
        await ctx.reply(c.convert(CurrFrom, CurrTo, money))

    @commands.hybrid_command(description="Converts INR to USD", with_app_command=True)
    async def convertToUSDFromINR(self, ctx: commands.Context, money: int):
        CurrTo = "INR"
        CurrFrom = "USD"
        url = f"https://api.apilayer.com/fixer/convert?to={CurrTo}&from={CurrFrom}&amount={money}"
        c = Currency_convertor(url)
        await ctx.reply(c.convert(CurrFrom, CurrTo, money))

    @commands.hybrid_command(description="Converts USD to INR", with_app_command=True)
    async def convertToINRFromUSD(self, ctx: commands.Context, money: int):
        CurrTo = "USD"
        CurrFrom = "INR"
        url = f"https://api.apilayer.com/fixer/convert?to={CurrTo}&from={CurrFrom}&amount={money}"
        c = Currency_convertor(url)
        money = int(money)
        await ctx.reply(c.convert(CurrFrom, CurrTo, money))

    @commands.command()
    @commands.is_owner()
    async def getmsg(self, ctx, msgid: int):
        for guild in self.bot.guilds:
            for channel in guild.channels:
                try:
                    msg = await channel.fetch_message(msgid)
                    break
                except:
                    pass
        await ctx.send(msg.content)
        
    @commands.command(aliases = ['cpres'])
    @commands.is_owner()
    async def changepresence(self, ctx, *, mssg=None):
        if mssg is None:
            await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"Prefix: nsb | {len(self.bot.guilds)} guilds and {len(self.bot.users)} members."))
        else:
            await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"{mssg}"))    
        await ctx.send("Status updated!")
    
async def setup(bot):
    await bot.add_cog(splEmotes(bot))