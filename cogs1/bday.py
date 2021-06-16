import discord
import random
from discord.ext import commands
from discord.utils import tasks
import json
from datetime import date


class bday(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
     
    @commands.command()
    async def setbday(self, ctx, member: discord.Member, bday):
        with open(r'./bday/bdays.json', 'r') as k:
            bdays = json.load(k)
        bdays[str(ctx.guild.id)][str(member.id)] = f'{bday}'
        with open(r'./bday/bdays.json', 'w') as j:
            json.dump(bdays, j, indent=4)
        await ctx.send(f"Birthday of {member.display_name} set on {bday}")

    @tasks.loop(hours=24)
    async def check(self):
        today = date.today()
        day, month = today.day, today.month
        today = day+'-'+month
        with open(r'./bday/bdays.json', 'r') as j:
            bdays = json.load(j)
        

def setup(bot):
    bot.add_cog(bday(bot))