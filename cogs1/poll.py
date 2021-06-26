import discord
from discord.ext import commands
import asyncio
from num2words import num2words

def timefinder(time):
    units = ["s", "m", "h"]
    unitdict = {"s": 1, "m": 60, "h": 3600}
    unit = time[-1]
    if unit not in units:
        return -1
    try:
        val = int(time[:-1])
    except:
        return -2
    return val*unitdict[unit]

class poll(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def poll(self, ctx, channel: discord.TextChannel = None):
        channel = channel or ctx.channel
        firs = await ctx.reply("Please answer the following questions in 60 seconds each.")
        msg = ["What is the contest criteria?",
               "What is the duration of the poll? (end with s,m or h) `Example: 5m or 2h or 10s`",
               "What is the number of contestants?"]
        answers = []

        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel
        for i in msg:
            quer = await ctx.send(i)
            try:
                rep = await self.bot.wait_for('message', timeout=30, check=check)
            except asyncio.TimeoutError:
                resp = await ctx.send("You didn't respond in the given time. Please respond faster next time!")
                quer.delete()
                await asyncio.sleep(10)
                await resp.delete()
                return
            else:
                answers.append(rep.content)
                await quer.delete()
                await rep.delete()
        entries = answers[2]
        category = answers[0]
        entry_list = []
        q2 = await ctx.send('Enter the entries one by one:')
        for entry in range(entries):
            try:
                contestants = await self.bot.wait_for('message', timeout=60, check=check)
            except asyncio.TimeoutError:
                resp = await ctx.send("You didn't respond in the given time. Please respond faster next time!")
                await asyncio.sleep(10)
                await resp.delete()
                await q2.delete()
                return
            else:
                entry_list.append(contestants.content)
                await contestants.delete()
        await q2.delete()
        pollEmb = discord.Embed(color=0x00FF00)
        pollEmb.set_author(name=category.title(), icon_url=ctx.author.avatar_url)
        number = 1
        for entry in entry_list:
            pollEmb.add_field(name="** **", value=f"{entry} ==> :f{num2words(number)}:", inline=False)
        pollembed = await channel.send(embed=pollEmb)


def setup(bot):
    bot.add_cog(poll(bot))