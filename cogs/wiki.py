import discord
from discord.ext import commands
import random
import wikipedia
import asyncio

color = [15158332, 3066993, 10181046, 3447003, 1752220, 15844367]


class wiki(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases = ['wikipedia'])
    async def wiki(self, ctx, *, query, member: discord.Member = None):
        #wikipedia.set_lang("en-in")
        # page_obj = wikipedia.page(query)
        # page_title = page_obj.original_title
        try:
            result = wikipedia.summary(query, sentences = 3, auto_suggest=True, redirect=True)
            res = wikipedia.page(title = query, auto_suggest=True)
        except wikipedia.exceptions.DisambiguationError as e:
            s = random.choice(e.options)
            res = wikipedia.page(title = s, auto_suggest=True)
            result = wikipedia.summary(s, sentences = 3)

        color_main = color[random.randint(0,5)]
        if member is None:
            # await ctx.send(f"{ctx.author.mention}")
            embed = discord.Embed(title=res.title, description = result, color=color_main, url = res.url)
            # embed.set_thumbnail(page_obj.images)
            await ctx.reply(embed=embed)
        else:
            # await ctx.send(f"{member.mention}")
            embed = discord.Embed(title=query, description = result, color=color_main)
            # embed.set_thumbnail(page_obj.images)
            await ctx.reply(embed=embed)
    
    @wiki.error
    async def wikinotfound(self, ctx, error):
        if isinstance(error, commands.CommandInvokeError):
            msg = await ctx.send("`Wiki not found!`")
            print(error)
            await asyncio.sleep(5)
            await msg.delete()
            
async def setup(bot):
    await bot.add_cog(wiki(bot))
