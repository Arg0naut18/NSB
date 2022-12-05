import discord
from discord.ext import commands
import json
import csv

async def get_transactions(user):
    with open(r'./bank/transactions.json', 'r') as f:
        trans = json.load(f)
    return trans[str(user.id)]

class translog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def passbook(self,ctx, member: discord.Member=None):
        member = ctx.author if not member else member
        transactions = await get_transactions(member)
        data_file = open('./bank/transactions.csv', 'w', newline='')
        item_data = transactions
        csv_columns = ["amount", "description", "total"]
        csv_writer = csv.DictWriter(data_file, fieldnames=csv_columns, extrasaction='ignore')
        csv_writer.writeheader()
        for itm in item_data:
            csv_writer.writerow(itm)
        data_file.close()
        file=discord.File(r"./bank/transactions.csv", filename=f"{member.display_name}'s passbook.csv")
        await ctx.send(f"{member.display_name}'s Passbook", file=file)

async def setup(bot):
    await bot.add_cog(translog(bot))