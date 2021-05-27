import discord
import random
from discord.ext import commands
import json
import asyncio


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


class giveaway(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["giveaway"])
    @commands.has_role("events hoster")
    async def gstart(self, ctx):
        firs = await ctx.reply("Please answer the following questions in 30 seconds each.")
        msg = ["Which channel should it be hosted in? Mention the channel.",
               "What is the duration of the giveaway? (end with s,m or h) `Example: 5m or 2h or 10s`",
               "What is the reward of the giveaway?"]
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
        try:
            chanid = int(answers[0][2:-1])
        except:
            resp = await ctx.send("You didn't mention the channel properly.")
            await asyncio.sleep(10)
            await resp.delete()
            return
        print(chanid)
        channel = self.bot.get_channel(chanid)
        time = timefinder(answers[1])
        if time == -1:
            resp = await ctx.send("You didn't mention the time properly.")
            await asyncio.sleep(10)
            await resp.delete()
            return
        elif time == -2:
            resp = await ctx.send("Time has to be an integer.")
            await asyncio.sleep(10)
            await resp.delete()
            return
        finaldraft = await ctx.send(f"Giveaway is ready to be done in {channel.mention} and the results will be announced in {answers[1]}")
        await firs.delete()
        await ctx.message.delete()
        await asyncio.sleep(20)
        await finaldraft.delete()
        ann = await ctx.send("@everyone")
        
        embed = discord.Embed(
            title="Giveaway!", description=f"Reward is {answers[2]}", color=random.randint(0x000000, 0xFFFFFF))
        embed.add_field(name="Hosted by:", value=f"{ctx.author.mention}")
        embed.set_footer(
            text=f"Ends {answers[1]} from the time of embed posted.")
        giveawayembed = await channel.send(embed=embed)

        await giveawayembed.add_reaction("✋")
        await asyncio.sleep(time)
        embedreact = await channel.fetch_message(giveawayembed.id)
        users = await embedreact.reactions[0].users().flatten()
        users.pop(users.index(self.bot.user))
        winner = random.choice(users)

        embed = discord.Embed(
            title="Giveaway!", description=f"Reward is {answers[2]}", color=random.randint(0x000000, 0xFFFFFF))
        embed.add_field(name="Winner", value=f"{winner.mention}", inline=False)
        embed.add_field(name="Hosted by:",
                        value=f"{ctx.author.mention}", inline=False)
        embed.set_footer(
            text=f"Ends {answers[1]} from the time of embed posted.")
        winnerembed = await giveawayembed.edit(embed=embed)
        await channel.send(f"Congratulations {winner.mention}!\nYou won {answers[2]}.")
        await ann.delete()

def setup(bot):
    bot.add_cog(giveaway(bot))
