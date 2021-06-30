import discord
from discord.ext import commands
import json
import csv
import ast

async def get_bank_data():
    with open(r"./bank/bank.json", 'r') as f:
        bank = json.load(f)
    return bank

class csvbank(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def bank(self, ctx):
        bank_data = await get_bank_data()
        # bank_data = ast.literal_eval(bank_data)
        data_file = open('./bank/bankdata.csv', 'w', newline='')
        csv_writer = csv.writer(data_file)
        count = 1
        for data_id in bank_data:
            print(data_id)
            data = bank_data[str(data_id)]
            csv_writer.writerow(["ID"])
            csv_writer.writerow([str(data_id)])
            if not isinstance(data, list):
                if count == 1:
                    header=data.keys()
                    csv_writer.writerow(header)
                    count += 1
                values=data.values()
                csv_writer.writerow(values)
            else:
                item_data = data["bag"]
                count=1
                for itm in item_data:
                    if count==1:
                        header=itm.keys()
                        csv_writer.writerow(header)
                        count+=1
                csv_writer.writerow(itm.values())
        data_file.close()
        file=discord.File(r"./bank/bankdata.csv", filename="bank.csv")
        csvembed = discord.Embed(title="Bank CSV file", color=0x00FF00)
        csvembed.set_image(url="attachment://bank.csv")
        await ctx.send("CSV", file=file)

def setup(bot):
    bot.add_cog(csvbank(bot))