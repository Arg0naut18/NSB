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
        poll_entries = {}
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
        
        entries = int(answers[2])
        category = answers[0]
        time = timefinder(answers[1])
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
        penultimate = await ctx.send("Embed ready!")
        
        await asyncio.sleep(5)
        await penultimate.delete()
        await firs.delete()
        
        pollEmb = discord.Embed(color=0x00FF00)
        pollEmb.set_author(name=category.title(), icon_url=ctx.author.avatar_url)
        number = 0
        emojiid=["<:one:858420222841847828>", "<:two:858420222288723989>", "<:three:858420221915562046>", "<:four:858420222372610108>", "<:five:858420222527799306>", "<:six:858420222687576094>", "<:seven:858420222670536714>", "<:eight:858420222725062696>", "<:nine:858420222464622602>"]
        for entry in entry_list:
            pollEmb.add_field(name="** **", value=f"**{emojiid[number]}**\t\t<a:right_arrow:857929374255153194>\t\t**{entry}**", inline=False)
            number+=1
        ever = await channel.send("@everyone")
        pollembed = await channel.send(embed=pollEmb)
        #emojiid = [858380597268840491, 858381328898064386, 858381381829394493, 858381428512129025, 858381480673935370, 858381553414963230, 858381600748339211, 858381640417673266, 858381679071592469]
        for i in range(entries):
            #emoji = discord.utils.get(ctx.message.guild.emojis, id=emojiid[i])
            await pollembed.add_reaction(emojiid[i])

        await asyncio.sleep(time)

        embedreact = await channel.fetch_message(pollembed.id)

        i=0
        total_reactions = 0
        for entry in entry_list:
            users = embedreact.reactions[i].count
            total_reactions += users-1
            poll_entries[f"{entry}"] = users-1
            i+=1
        
        sorteddict = dict(sorted(poll_entries.items(), key=lambda item: item[1], reverse=True))
        winner = list(sorteddict.keys())[0]
        winpercent = (list(sorteddict.values())[0]*100)/total_reactions
        await ever.delete()
        await pollembed.delete()
        await channel.send("@everyone")
        winnerembed = discord.Embed(title="Poll Winner", color=0x00FF00)
        winnerembed.add_field(name="Poll query", value=category.title(), inline=False)
        winnerembed.add_field(name="Winner", value=winner, inline=False)
        winnerembed.add_field(name="Win Percentage", value=f"`{winpercent}`", inline=False)
        await channel.send(embed=winnerembed)

def setup(bot):
    bot.add_cog(poll(bot))