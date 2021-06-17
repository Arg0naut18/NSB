import discord
from discord.ext import commands
import json
from datetime import date
import calendar
import random

async def open_account(user):
    with open(r'./bank/bank.json', 'r') as f:
        users = json.load(f)
    if str(user.id) in users:
        return False
    else:
        users[str(user.id)] = {}
        users[str(user.id)]["wallet"] = 0
        users[str(user.id)]["bank"] = 0
    with open(r'./bank/bank.json', 'w') as f:
        json.dump(users, f, indent=4)
    return True

async def get_account_data():
    with open(r'./bank/bank.json', 'r') as j:
        users = json.load(j)
    return users

class bday(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
     
    @commands.command()
    async def balance(self, ctx, member: discord.Member = None):
        member = ctx.author if not member else member
        await open_account(member)
        users = await get_account_data()
        wallet_money = users[str(member.id)]["wallet"]
        bank_money = users[str(member.id)]["bank"]
        emb = discord.Embed(title=f"{member.name}'s Balance", color=0x00FF00)
        emb.add_field(name="Wallet balance", value=f"{wallet_money}", inline=True)
        emb.add_field(name="Bank balance", value=f"{bank_money}", inline=True)
        await ctx.send(embed=emb)

    @commands.command()
    async def beg(self, ctx):
        await open_account(ctx.author)
        users = await get_account_data()
        money = random.randrange(1000)
        if money != 0:
            users[str(ctx.author.id)]["wallet"] += money
            with open(r'./bank/bank.json', 'w') as f:
                json.dump(users, f, indent=4)
            await ctx.send(f"Someone just gave you :coin:{money}! Congrats <:party:855108695192895498>!")
        else:
            await ctx.send(f"Better luck next time. <:sadcrypeace:855109459852656690>")

    @commands.command()
    async def deposit(self, ctx, amount=None):
        await open_account(ctx.author)
        users = await get_account_data()
        if amount == None:
            amount = users[str(ctx.author.id)]["wallet"]
            users[str(ctx.author.id)]["bank"] += users[str(ctx.author.id)]["wallet"]
            users[str(ctx.author.id)]["wallet"] = 0
            await ctx.send(f"You successfully deposited :coin:{amount}!")
        else:
            users[str(ctx.author.id)]["bank"] += int(amount)
            users[str(ctx.author.id)]["wallet"] -= int(amount)
            await ctx.send(f"You successfully deposited :coin:{amount}!")
        with open(r'./bank/bank.json', 'w') as f:
            json.dump(users, f, indent=4)

    @commands.command()
    async def withdraw(self, ctx, amount=None):
        await open_account(ctx.author)
        users = await get_account_data()
        if amount == None:
            await ctx.send("You need to mention the amount you wanna withdraw!")
        else:
            users[str(ctx.author.id)]["wallet"] += int(amount)
            users[str(ctx.author.id)]["bank"] -= int(amount)
            with open(r'./bank/bank.json', 'w') as f:
                json.dump(users, f, indent=4)
            await ctx.send(f"You successfully withdrew :coin:{amount}!")

def setup(bot):
    bot.add_cog(bday(bot))