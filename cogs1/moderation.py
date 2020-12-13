import discord
# from discord import channel
# from discord.embeds import Embed
from discord.ext import commands
from discord import TextChannel
import random
from discord.ext.commands import has_permissions, MissingPermissions
from discord.utils import get
import asyncio

color = [15158332, 3066993, 10181046, 3447003, 1752220, 15844367]


class Moderation(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def announce(self, ctx, chan: TextChannel, *, mssg):
        if chan:
            color_main = color[random.randint(0, 5)]
            embed = discord.Embed(title="Announcement!", description=mssg, color=color_main)
            await chan.send(embed=embed)
        else:
            await ctx.send("Channel not found!")

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(administrator=True)
    async def clear(self, ctx, amount=10):
        await ctx.channel.purge(limit=(amount + 1))

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        channel = get(ctx.guild.text_channels, id=757537306579173397)
        # india server channel id = 711086134956130370
        # bot test 3 server channel id = 765647163463434298
        # sci-cord channel id = 757537306579173397
        reason = "Not Given" if not reason else reason
        emb = discord.Embed(title="Member Kick Announcement")
        emb.add_field(name="Kicked member:", value=member.display_name, inline=False)
        emb.add_field(name="From:", value=ctx.guild.name, inline=False)
        emb.add_field(name="Reason:", value=reason, inline=False)
        emb.set_footer(text=f"Kicked by {ctx.author}", icon_url=ctx.author.avatar_url)
        await channel.send(embed=emb)
        await member.send(embed=emb)
        await member.kick(reason=reason)
        await asyncio.sleep(5)
        await ctx.channel.purge(limit=1)
        # chan = await member.create_dm()

    @announce.error
    async def noPerm(self, error, ctx):
        if isinstance(error, MissingPermissions):
            text = "Sorry {}, you do not have permissions to do that!".format(ctx.message.author)
            await ctx.send_message(ctx.message.channel, text)

    @clear.error
    async def noPerm(self, error, ctx):
        if isinstance(error, MissingPermissions):
            text = "Sorry {}, you do not have permissions to do that!".format(ctx.message.author)
            await ctx.send_message(ctx.message.channel, text)

    @kick.error
    async def noPerm(self, error, ctx):
        if isinstance(error, MissingPermissions):
            text = "Sorry {}, you do not have permissions to do that!".format(ctx.message.author)
            await ctx.send_message(ctx.message.channel, text)


def setup(bot):
    bot.add_cog(Moderation(bot))
