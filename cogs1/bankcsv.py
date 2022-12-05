import discord
from discord.ext import commands
import json
import csv

async def get_bank_data(user=None):
    with open(r"./bank/bank.json", 'r') as f:
        bank = json.load(f)
    if user is None:
        return bank
    else:
        return bank[str(user.id)]

class csvbank(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(description="Get all your transactions")
    async def bank(self, ctx: commands.Context):
        ctx.defer(ephemeral=True)
        bank_data = await get_bank_data(ctx.author)
        data_file = open('./bank/bankdata.csv', 'w', newline='')
        columns = ["wallet", "bank", "banknote", "huntinggun", "fishingrod", "coinbomb", "padlock", "hpic"]
        csv_writer = csv.DictWriter(data_file, fieldnames=columns, extrasaction='ignore')
        csv_writer.writeheader()
        for item in bank_data:
            csv_writer.writerow(item)
        data_file.close()
        file=discord.File(r"./bank/bankdata.csv", filename="bank.csv")
        csvembed = discord.Embed(title=f"{ctx.author.name}'s Bank CSV", color=0x00FF00)
        csvembed.set_image(url=f"attachment://{ctx.author.name}-bank.csv")
        await ctx.send("CSV", file=file)

    @commands.hybrid_command(description="Get the csv file of the entire bank")
    @commands.has_permissions(administrator=True)
    async def totalbank(self, ctx):
        ctx.defer(ephemeral=True)
        bank_data = await get_bank_data()
        # bank_data = ast.literal_eval(bank_data)
        data_file = open('./bank/bankdata.csv', 'w', newline='')
        csv_writer = csv.writer(data_file)
        count = 1
        for data_id in bank_data:
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
        file=discord.File(r"./bank/bankdata.csv", filename="totalbank.csv")
        csvembed = discord.Embed(title="Bank CSV file", color=0x00FF00)
        csvembed.set_image(url="attachment://totalbank.csv")
        await ctx.send("CSV", file=file, ephemeral=True)

async def setup(bot):
    await bot.add_cog(csvbank(bot))