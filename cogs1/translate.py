import discord
from discord.ext import commands
from googletrans import Translator, LANGUAGES
import random

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
        await ctx.reply(embed=embed)

def setup(bot):
    bot.add_cog(trans(bot))
