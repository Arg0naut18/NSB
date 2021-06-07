import discord
import mendeleev
import random
from discord.ext import commands
import json
import wikipedia
from molmass import Formula

# attributes = ['atomic', 'symbol', 'name', 'mass']


class atom(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
     
    @commands.command()
    async def atom(self, ctx, elem1):
        try:
            if type(elem1) != int:
                elem = mendeleev.element(elem1.title())
            else:
                elem = mendeleev.element(elem1)
            res = wikipedia.page(title = elem.name.title(), auto_suggest=True)
            embed = discord.Embed(title=f'__{elem.name.title()}__', color=random.randint(0x000000, 0xFFFFFF))
            embed.add_field(name="Symbol", value=f'`{elem.symbol}`', inline=True)
            embed.add_field(name="Element", value=f'`{elem.name.title()}`', inline=True)
            embed.add_field(name="Atomic no.", value=f'`{elem.atomic_number}`', inline=True)
            embed.add_field(name="Atomic mass", value=f'`{elem.mass}`', inline=True)
            try:
                embed.add_field(name="Group", value=f'`{elem.group.symbol} or {elem.group.name}`', inline=True)
            except:
                pass
            embed.add_field(name="Electronic Configuration", value=f'`{elem.ec}`', inline=False)
            embed.add_field(name="Wikipedia Link", value=f'{res.url}', inline = False)
            await ctx.send(embed=embed)
        except Exception as e:
            print(e)
            await ctx.send("Error loading database! Please check the element.")

    @commands.command(aliases=['periodic', 'periodictable'])
    async def ptable(self, ctx):
        with open(r'./meme_templates/ptable.jpg', 'rb') as f:
            picture=discord.File(f)
            await ctx.send(file=picture)

    @commands.command(aliases=['mass', 'amass'])
    async def atomicmass(self, ctx, compound):
        f = Formula(compound)
        await ctx.send(f"`{f.mass} g/mol`")

def setup(bot):
    bot.add_cog(atom(bot))