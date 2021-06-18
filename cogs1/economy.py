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

async def update_bank_data(user,amount=0,mode="wallet"):
    users = await get_account_data()
    users[str(user.id)][mode] += amount
    with open(r'./bank/bank.json', 'w') as j:
        json.dump(users, j)
    bal = [users[str(user.id)]["wallet"], users[str(user.id)]["bank"]]
    return bal

class economy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
     
    @commands.command(aliases = ['bal'])
    async def balance(self, ctx, member: discord.Member = None):
        member = ctx.author if not member else member
        await open_account(member)
        users = await get_account_data()
        wallet_money = users[str(member.id)]["wallet"]
        bank_money = users[str(member.id)]["bank"]
        emb = discord.Embed(title=f"{member.name}'s Balance", color=0x00FF00)
        emb.add_field(name=":money_with_wings: Wallet balance", value=f"`{wallet_money}`", inline=False)
        emb.add_field(name=":bank: Bank balance", value=f"`{bank_money}`", inline=False)
        await ctx.send(embed=emb)

    @commands.command()
    async def beg(self, ctx):
        await open_account(ctx.author)
        users = await get_account_data()
        money = random.randrange(100)
        if money != 0:
            users[str(ctx.author.id)]["wallet"] += money
            with open(r'./bank/bank.json', 'w') as f:
                json.dump(users, f, indent=4)
            await ctx.send(f"Someone just gave you :coin:`{money}`! Congrats :tada:!")
        else:
            await ctx.send(f"Better luck next time. <:sadcrypeace:855109459852656690>")

    @commands.command()
    async def deposit(self, ctx, amount=None):
        if amount is None:
            await ctx.send("You need to mention the amount you wanna deposit.")
            return
        await open_account(ctx.author)
        bal = await update_bank_data(ctx.author)
        if amount == "all" or amount == "max":
            amount = bal[0]
        if int(amount)>bal[0]:
            await ctx.send("You don't have enough money.")
            return
        if int(amount)<0:
            await ctx.send("The amount can't be negative.")
            return
        await update_bank_data(ctx.author, int(amount), "bank")
        await update_bank_data(ctx.author, -1*int(amount))
        await ctx.send(f"You just deposited :coin:{amount}!")
    
    @commands.command()
    async def give(self, ctx, member: discord.Member=None, amount=None):
        if amount is None:
            await ctx.send("You need to mention the amount you wanna deposit.")
            return
        if member is None:
            await ctx.send("You need to mention whom you wanna give the money to.")
            return
        await open_account(ctx.author)
        await open_account(member)
        bal = await update_bank_data(ctx.author)
        if amount == "all" or amount == "max":
            amount = bal[0]
        if int(amount)>bal[0]:
            await ctx.send("You don't have enough money.")
            return
        if int(amount)<0:
            await ctx.send("The amount can't be negative.")
            return
        await update_bank_data(member, int(amount))
        await update_bank_data(ctx.author, -1*int(amount))
        await ctx.send(f"You just gave :coin:{amount} to {member.mention}! What a generous lad.")

    @commands.command()
    async def withdraw(self, ctx, amount=None):
        if amount is None:
            await ctx.send("You need to mention the amount you wanna deposit.")
            return
        await open_account(ctx.author)
        bal = await update_bank_data(ctx.author)
        if amount == "all" or amount == "max":
            amount = bal[1]
        if int(amount)>bal[1]:
            await ctx.send("You don't have enough money.")
            return
        if int(amount)<0:
            await ctx.send("The amount can't be negative.")
            return
        await update_bank_data(ctx.author, int(amount))
        await update_bank_data(ctx.author, -1*int(amount), "bank")
        await ctx.send(f"You just withdrew :coin:{amount}!")

    @commands.command()
    async def rob(self, ctx, member: discord.Member=None):
        if member is None:
            await ctx.send("You need to mention the person you wanna rob lmao.")
            return
        users = await get_account_data()
        if ctx.author.id not in users:
            await ctx.send("You need to create your own account first!")

def setup(bot):
    bot.add_cog(economy(bot))