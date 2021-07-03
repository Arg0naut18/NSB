import discord
from discord.ext import commands, tasks
import json
from datetime import date
import calendar

class bday(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.check.start()
     
    @commands.command()
    async def setbday(self, ctx, member: discord.Member, bday):
        with open(r'./bday/bdays.json', 'r') as k:
            bdays = json.load(k)
        try:
            bdays[str(ctx.guild.id)][str(member.id)] = f'{bday}'
        except KeyError:
            bdays[str(ctx.guild.id)] = {}
            bdays[str(ctx.guild.id)][str(member.id)] = f'{bday}'
        with open(r'./bday/bdays.json', 'w') as j:
            json.dump(bdays, j, indent=4)
        await ctx.send(f"Birthday of {member.display_name} set on {bday}")
    
    @commands.command()
    async def showbdays(self, ctx, server: discord.Guild=None):
        server = ctx.guild if not server else server
        with open(r'./bday/bdays.json', 'r') as j:
            bdays = json.load(j)
        msg = ''
        for user_id in bdays[str(server.id)]:
            date = bdays[str(server.id)][user_id]
            day, month = date.split('-')
            day = int(day)
            month = int(month)
            month = calendar.month_name[month]
            date = str(day) + ' ' +month
            member = await self.bot.fetch_user(user_id)
            msg = msg + (f"**{member.mention}** => **{date}**\n")
        bdayembed = discord.Embed(title=f"Birthdays of members from {server.name}", description=msg, color=0x00FF00)
        await ctx.send(embed=bdayembed)

    @tasks.loop(minutes=1)
    async def check(self):
        today = date.today()
        day, month = today.day, today.month
        if day<10:
            daystr = '0'+str(day)
        else:
            daystr = day
        if month<10:
            monthstr = '0'+str(month)
        else:
            monthstr = month
        todaydate = daystr+'-'+monthstr
        channel = discord.utils.get(self.bot.get_all_channels(), id=855031679281397761)
        with open(r'./bday/bdays.json', 'r') as j:
            bdays = json.load(j)
        for server_id in bdays:
            for user_id in server_id:
                if bdays[str(server_id)][str(user_id)] == todaydate:
                    user = discord.utils.get(self.bot.get_all_members(), id=user_id)
                    await channel.send(f"A very big Happy Birthday to you {user.mention}.")

def setup(bot):
    bot.add_cog(bday(bot))