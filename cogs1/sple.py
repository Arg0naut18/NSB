import discord
from discord.ext import commands
import random
import asyncio
from discord.utils import get

color = [15158332, 3066993, 10181046, 3447003, 1752220, 15844367]


class splEmotes(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context = True)
    @commands.guild_only()
    async def lock(self, ctx, emoji, role):
        emo = get(ctx.guild.emojis, name = emoji)
        role = get(ctx.guild.roles, id=role)
        emo.roles[role]
        await ctx.send(f"Locked :{emoji}: for {role} in this server!")

    # @commands.command(pass_context=True)
    # @commands.guild_only()
    # async def unlock(self, ctx, emoteId: discord.Emoji.name):
    #     emoteId.roles[""]
    #     await ctx.send(f"Unlocked {emoteId} for this server!")

def setup(bot):
    bot.add_cog(splEmotes(bot))
