import discord
from discord.ext import commands, tasks
import json
from datetime import date
import calendar
import random

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
            date = str(day)+' '+month
            member = await self.bot.fetch_user(user_id)
            msg = msg + (f"**{member.mention}** => **{date}**\n")
        bdayembed = discord.Embed(title=f"Birthdays of members from {server.name}", description=msg, color=0x00FF00)
        await ctx.send(embed=bdayembed)

    @tasks.loop(hours=24)
    async def check(self):
        today = date.today()
        day, month = today.day, today.month
        if day<10:
            daystr = '0'+str(day)
        else:
            daystr = str(day)
        if month<10:
            monthstr = '0'+str(month)
        else:
            monthstr = str(month)
        todaydate = daystr+'-'+monthstr
        await self.bot.wait_until_ready()
        channel = self.bot.get_channel(855031679281397761)
        with open(r'./bday/bdays.json', 'r') as j:
            bdays = json.load(j)
        for server_id in bdays:
            for user_id in bdays[str(server_id)]:
                if bdays[server_id][user_id] == todaydate:
                    user = discord.utils.get(self.bot.get_all_members(), id=int(user_id))
                    await channel.send(f"A very big Happy Birthday 🎂 to you {user.mention} from <@!436844058217021441> and NSB community. <a:partyconfetti:860885019898937374>")
                    urls = ['https://media.tenor.com/images/e37ae589afa0cffe7c9957bee26e36cc/tenor.gif',
                    'https://media.tenor.com/images/72fead26968d18a5846f02298dacb3b3/tenor.gif',
                    'https://media.tenor.com/images/ee1cd9269f1872a5eb31cef9b86a20cd/tenor.gif',
                    'https://media.tenor.com/images/ac4f49e01b8d289c16271e2187ee62d8/tenor.gif',
                    'https://i.pinimg.com/originals/4f/b9/96/4fb996524beabfa60c7ca4394057bbc9.gif',
                    'https://media.tenor.com/images/25d627f3e0f09fe712f8b9fd4bd675cb/tenor.gif',
                    'https://media.tenor.com/images/0b6f0b738d777f1f393492918ef94eda/tenor.gif']
                    embed = discord.Embed(title=(f'__***NotSoBasicBot***__ is wishing **Happy Birthday** to __***{user.name}***__') ,color=0x00ff00)
                    embed.set_image(url=random.choice(urls))
                    await channel.send(embed=embed)
    
async def setup(bot):
    await bot.add_cog(bday(bot))