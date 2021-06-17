import discord
from discord.ext import commands
import json
from datetime import date
import calendar

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
        json.dump(users, f)
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
        await open_account(ctx.author)
        users = await get_account_data()
        wallet_money = users[str(ctx.author.id)]["wallet"]
        bank_money = users[str(ctx.author.id)]["bank"]
        emb = discord.Embed(title=f"{ctx.author.name}'s Balance", color=0x00FF00)
        emb.add_field(name="Wallet balance", value=f"{wallet_money}", inline=True)
        emb.add_field(name="Bank balance", value=f"{bank_money}", inline=True)

def setup(bot):
    bot.add_cog(bday(bot))