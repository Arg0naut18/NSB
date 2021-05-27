import discord
from udpy import UrbanClient
from discord.ext import commands
import random
import asyncio

class dict(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["ud", "dictionary", "define", "def"])
    async def dict(self, ctx, *, word):
        client = UrbanClient()
        defs = client.get_definition(word)
        try:
            word = defs[0].word
        except:
            noWord = await ctx.reply("`Word not found!`")
            await asyncio.sleep(10)
            await noWord.delete()
            return
        embed = discord.Embed(
            title=f"{defs[0].word}".title(), description="If this is the word react with ✅", color=random.randint(0x000000, 0xFFFFFF))
        meaning = await ctx.reply(embed=embed)
        await meaning.add_reaction("✅")

        def check1(reaction, user):
            if not user.bot:
                return reaction.message.id == meaning.id and str(reaction.emoji) == "✅"
            else:
                return False
        try:
            await self.bot.wait_for("reaction_add", timeout=30, check=check1)
        except TimeoutError:
            resp = await ctx.send("Sorry couldn't find the meaning.")
            await asyncio.sleep(5)
            await resp.delete()
            return
        else:
            i = 0

            def check(reaction, user):
                if not user.bot:
                    return reaction.message.id == meaning.id
                else:
                    return False

            embed = discord.Embed(
                title=f"__**{defs[i].word}**__".title(), color=random.randint(0x000000, 0xFFFFFF))
            embed.add_field(name="__Definition__", value=str(
                defs[i].definition), inline=False)
            embed.add_field(name="__Example__", value=str(
                defs[i].example), inline=False)
            embed.set_footer(text=f"Meaning:{i+1}/{len(defs)}")
            await meaning.edit(embed=embed)
            await meaning.add_reaction("⬅️")
            await meaning.add_reaction("➡️")
            while i < len(defs):
                # try:
                try:
                    reaction, user = await self.bot.wait_for("reaction_add", timeout=60, check=check)
                except asyncio.TimeoutError:
                    await meaning.clear_reactions()
                else:
                    if str(reaction.emoji) == "➡️":
                        try:
                            i += 1
                            embed = discord.Embed(
                                title=f"__**{defs[i].word}**__".title(), color=random.randint(0x000000, 0xFFFFFF))
                            embed.add_field(name="__Definition__", value=str(
                                defs[i].definition), inline=False)
                            embed.add_field(name="__Example__", value=str(
                                defs[i].example), inline=False)
                            embed.set_footer(text=f"Meaning:{i+1}/{len(defs)}")
                            await meaning.edit(embed=embed)
                            await meaning.remove_reaction("➡️", user)
                        except:
                            await meaning.remove_reaction("➡️", user)
                            responseex = await ctx.send("`That's the end of definitions.`")
                            await meaning.clear_reactions()
                            await asyncio.sleep(5)
                            await responseex.delete()
                    elif str(reaction.emoji) == "⬅️":
                        if not i==0:
                            i -= 1
                            embed = discord.Embed(
                                title=f"__**{defs[i].word}**__".title(), color=random.randint(0x000000, 0xFFFFFF))
                            embed.add_field(name="__Definition__", value=str(
                                defs[i].definition), inline=False)
                            embed.add_field(name="__Example__", value=str(
                                defs[i].example), inline=False)
                            embed.set_footer(text=f"Meaning:{i+1}/{len(defs)}")
                            await meaning.edit(embed=embed)
                            await meaning.remove_reaction("⬅️", user)
                        if i==0:
                            await meaning.remove_reaction("⬅️", user)
                    else:
                        return

def setup(bot):
    bot.add_cog(dict(bot))