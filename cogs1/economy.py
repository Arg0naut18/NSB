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
        emb.set_footer(text=f"Invoked by: {ctx.author.name}", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=emb)

    @commands.command()
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def beg(self, ctx):
        await open_account(ctx.author)
        users = await get_account_data()
        money = random.randrange(500)
        if money != 0 and random.randrange(0,2)==1:
            users[str(ctx.author.id)]["wallet"] += money
            with open(r'./bank/bank.json', 'w') as f:
                json.dump(users, f, indent=4)
            await ctx.send(f"Someone just gave you :coin:`{money}`! Congrats <a:partygif:855108791532388422>!")
        else:
            await ctx.send(f"Better luck next time. <a:sadcrypeace:855109649962369054>")

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
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def rob(self, ctx, member: discord.Member=None):
        if member is None:
            await ctx.send("You need to mention whom you wanna give the money to.")
            return
        await open_account(ctx.author)
        await open_account(member)
        bal = await update_bank_data(ctx.author)
        membal = await update_bank_data(member)
        if bal[0]<50:
            await ctx.send("You need to have :coin:50 in your wallet to rob.")
            return
        if membal[0]<100:
            await ctx.send("It's not worth it man.")
            return
        chance = random.randrange(0,2)
        if chance==1:
            amount = random.randrange(0, membal[0])
            await update_bank_data(member, -1*int(amount))
            await update_bank_data(ctx.author, int(amount))
            await ctx.send(f"You just robbed :coin:{amount} from {member.mention}! Poor lad.")
        else:
            await update_bank_data(ctx.author, -50)
            await ctx.send(f"Failed to rob {member.mention}. You lost :coin:50!")

def setup(bot):
    bot.add_cog(economy(bot))