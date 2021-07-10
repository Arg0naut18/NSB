import discord
from discord.ext import commands
import random
import json


async def error_embed(channel, error):
    if isinstance(error, discord.errors.Forbidden):
        emb = discord.Embed(title="Error Occurred!", description="Lacking permission. Please check that the role of this bot is on top of the users that r gonna access it.", color=0x00ff00)
        await channel.send(embed=emb)


async def get_color_list():
    with open('./colors/colors.json', 'r') as f:
        color_list = json.load(f)
    return color_list


async def make_color_list(user):
    color_list = await get_color_list()
    if str(user.guild.id) in color_list:
        return False
    else:
        color_list[str(user.guild.id)] = {}
    with open('./colors/colors.json', 'r') as f:
        json.dump(color_list, f, indent=4)


class Colors(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.group()
    async def add(self, ctx):
        if ctx.invoked_subcommand is None:
            pass

    @add.group()
    async def color(self, ctx, colorname, colorhex):
        try:
            await make_color_list(ctx.author)
            col = discord.Colour(int(f"0x{colorhex}", 16))
            ctx.guild.create_role(name=str(colorname), colour = col)
            colorembed = discord.Embed(title=f"Success", description=f"Successfully added {colorname} to the roles.", color=col)
            await ctx.send(embed=colorembed)
            color_list = await get_color_list()
            color_list.append()
        except Exception as error:
            await error_embed(ctx, error)
