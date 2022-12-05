import discord
from discord.ext import commands
import random
import datetime

class help(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(name="helpindm", with_app_command=True)
    async def helpindm(self, ctx, category=None):
        if category is None:
            emb = discord.Embed(
                title="__**Ɖɨʋɨռɛ COMMANDS:**__", color=random.randint(0x000000, 0xFFFFFF))
            emb.add_field(name=":tools: Moderation",
                          value="`nsb help moderation`", inline=True)
            emb.add_field(name=":joy: Memes",
                          value="`nsb help memes`", inline=True)
            emb.add_field(name=":slight_smile: Trivial",
                          value="`nsb help trivial`", inline=True)
            emb.add_field(name=":arrow_forward: Youtube",
                          value="`nsb help youtube`", inline=True)
            emb.add_field(name=":musical_keyboard: Music",
                          value="`nsb help music`", inline=True)
            emb.add_field(name=":notebook_with_decorative_cover: Educational",
                          value="`nsb help edu`", inline=True)
            emb.add_field(name=":hugging: Emotes",
                          value="`nsb help emotes`", inline=True)
            emb.add_field(name=":man_zombie: Lifeafter",
                          value="`nsb help la`", inline=True)
            emb.add_field(name=":money_with_wings: Economy", value=f"`nsb help economy`", inline=True)
            emb.set_thumbnail(url=self.bot.user.avatar_url)
            emb.set_footer(
                text=f"Invoked by {ctx.author.display_name}", icon_url=ctx.author.avatar_url)
            emb.timestamp = datetime.datetime.now()
            await ctx.message.add_reaction("☑️")
            await ctx.author.send(embed=emb)

async def setup(bot):
    await bot.add_cog(help(bot))