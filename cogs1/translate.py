import discord
from discord.ext import commands
from googletrans import Translator, LANGUAGES
import random
import asyncio

color = [15158332, 3066993, 10181046, 3447003, 1752220, 15844367]

class trans(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["tr"])
    async def translate(self, ctx, *, sentence):
        translator = Translator()
        translation = translator.translate(sentence)
        color_main = color[random.randint(0, len(color)-1)]
        embed = discord.Embed(title=" ", color=color_main)
        embed.add_field(name="Translation", value=translation.text, inline=False)
        embed.add_field(name="Source Lang.", value=LANGUAGES[translation.src].title(), inline=False)
        t = await ctx.reply(embed=embed)
        await t.add_reaction("<a:wrong:859371475482705920>")
        def check1(reaction, user):
            if not user.bot:
                return reaction.message.id == t.id and str(reaction.emoji) == "<a:wrong:859371475482705920>"
            else:
                return False
        try:
            await self.bot.wait_for("reaction_add", timeout=30, check=check1)
        except TimeoutError:
            return
        else:
            await ctx.send("Enter the language you think the sentence is in:")
            def check2(m):
                return m.author == ctx.author and m.channel == ctx.channel
            try:
                lang = await self.bot.wait_for("message", timeout=30, check=check2)
            except:
                pass
            else:
                translator = Translator()
                try:
                    translation = translator.translate(sentence, src=lang.content.lower())
                except:
                    await ctx.send("Language not supported!")
                    return
                color_main = color[random.randint(0, len(color)-1)]
                embed = discord.Embed(title=" ", color=color_main)
                embed.add_field(name="Translation", value=translation.text, inline=False)
                embed.add_field(name="Source Lang.", value=LANGUAGES[translation.src].title(), inline=False)
                t = await ctx.reply(embed=embed)



def setup(bot):
    bot.add_cog(trans(bot))