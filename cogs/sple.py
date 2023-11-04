import discord
from discord.ext import commands
import time
import json
import requests
from configs import FILLER_API

color = [15158332, 3066993, 10181046, 3447003, 1752220, 15844367]

class CurrencyConvertor:
    rates = 0
    def __init__(self, url):
        data = requests.request("GET", url, headers={"apikey":FILLER_API}, data = {}).json()
        self.rates = data['info']['rate']

    def convert(self, from_currency, to_currency, amount):
        initial_amount = amount
        amount = round(amount * self.rates, 2)
        return ('{} {} = {} {}'.format(initial_amount, from_currency, amount, to_currency))

class SplEmotes(commands.Cog):

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
    async def convert(self, ctx: commands.Context, money: int, curr_from: str, curr_to: str):
        curr_from = curr_from.upper()
        curr_to = curr_to.upper()
        url = f"https://api.apilayer.com/fixer/convert?to={curr_to}&from={curr_from}&amount={money}"
        c = CurrencyConvertor(url)
        await ctx.reply(c.convert(curr_from, curr_to, money))

    @commands.hybrid_command(name="convert-to-usd-from-inr", description="Converts INR to USD", with_app_command=True)
    async def convertToUSDFromINR(self, ctx: commands.Context, money: int):
        curr_to = "INR"
        curr_from = "USD"
        url = f"https://api.apilayer.com/fixer/convert?to={curr_to}&from={curr_from}&amount={money}"
        c = CurrencyConvertor(url)
        await ctx.reply(c.convert(curr_from, curr_to, money))

    @commands.hybrid_command(name="convert-to-inr-from-usd", description="Converts USD to INR", with_app_command=True)
    async def convertToINRFromUSD(self, ctx: commands.Context, money: int):
        curr_to = "USD"
        curr_from = "INR"
        url = f"https://api.apilayer.com/fixer/convert?to={curr_to}&from={curr_from}&amount={money}"
        c = CurrencyConvertor(url)
        money = int(money)
        await ctx.reply(c.convert(curr_from, curr_to, money))

    @commands.command()
    @commands.is_owner()
    async def getmsg(self, ctx, msgid: int):
        for guild in self.bot.guilds:
            for channel in guild.channels:
                try:
                    msg = await channel.fetch_message(msgid)
                    break
                except Exception:
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
    await bot.add_cog(SplEmotes(bot))