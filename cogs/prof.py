import discord
from discord.ext import commands
import random
from discord.utils import get
from pytz import timezone

# import datetime
# from discord import Status

# color = [15158332, 3066993, 10181046, 3447003, 1752220, 15844367]

class prof(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["prof", "whois", "ui", "userinfo"])
    async def profile(self, ctx, member: discord.Member = None):
        # ctx.message.author.server_permission
        member = ctx.author if not member else member
        color_main = random.randint(0x000000, 0xFFFFFF)
        # member = ctx.message.author
        roles = member.roles
        # permissions = member.guild_permissions
        role_s = [role.mention for role in roles]
        role_names = " ".join([str(x) for x in role_s[:0:-1]])
        # role_perms = [role.permissions for role in member.roles]
        creation = member.created_at
        creation = creation.replace(tzinfo=timezone('UTC')).astimezone(timezone('Asia/Kolkata'))
        joined = member.joined_at
        joined = joined.replace(tzinfo=timezone('UTC')).astimezone(timezone('Asia/Kolkata'))
        perm_list = [perm[0] for perm in member.guild_permissions if perm[1]]
        perms = ", ".join([str(x) for x in sorted(perm_list)])
        embed = discord.Embed(color=color_main, description=member.mention)
        embed.set_thumbnail(url=member.avatar_url)
        embed.set_author(name=f"{member.name}", icon_url=member.avatar_url)
        # embed.add_field(name="Name", value=member.name, inline=True)
        embed.add_field(name="Roles", value=role_names, inline=False)
        customstats = None
        try:
            stats = str(member.status)
            for s in member.activities:
                if isinstance(s, discord.CustomActivity):
                    customstats = s
        except:
            stats = "Can't say!"
        if stats == "online":
            embed.add_field(name="Status", value=":green_circle:" + f" {stats}".title(), inline=True)
        if stats == "dnd":
            embed.add_field(name="Status", value=":red_circle:"+f" {stats}".upper(), inline=True)
        if stats == "idle":
            embed.add_field(name="Status", value=":orange_circle:"+f" {stats}".title(), inline=True)
        if stats == "Can't say!":
            embed.add_field(name="Status", value=f"{stats}", inline=True)
        if(customstats is not None):
            embed.add_field(name=" Custom Status", value=f"{customstats}", inline=False)
        embed.add_field(name="Created at", value=creation.strftime(
            "%a, %b %d, %Y, %I:%M%p IST"), inline=True)
        embed.add_field(name="Joined at", value=joined.strftime(
            "%a, %b %d, %Y, %I:%M%p IST"), inline=True)
        embed.add_field(name="Permissions",
                        value=perms.replace("_", " "), inline=False)
        embed.set_footer(text=f"id: {member.id}", icon_url=member.avatar_url)
        await ctx.reply(embed=embed)

    @commands.command(aliases=['av', 'pfp'])
    async def avatar(self, ctx, member: discord.Member = None):
        color_main = random.randint(0x000000, 0xFFFFFF)
        # await ctx.send(f"{ctx.author.mention} Thanks for your concern! Please join our discord server.\nhttps://discord.gg/MtWY9Vb")
        member = ctx.author if not member else member
        embed = discord.Embed(
            color=color_main
        )
        embed.set_author(name=f"{member.display_name}",
                         icon_url=member.avatar_url)
        embed.set_image(url=member.avatar_url)
        embed.set_footer(
            text=f"invoked by: {ctx.author}", icon_url=ctx.author.avatar_url)
        await ctx.reply(embed=embed)

    @commands.command(aliases=['sicon'])
    async def servericon(self, ctx):
        # await ctx.send(f"{ctx.author.mention} Thanks for your concern! Please join our discord server.\nhttps://discord.gg/MtWY9Vb")
        embed = discord.Embed(
            color=random.randint(0x000000, 0xFFFFFF)
        )
        embed.set_author(name=f"{ctx.guild.name}")
        embed.set_image(url=ctx.guild.icon_url)
        embed.set_footer(
            text=f"invoked by: {ctx.author}", icon_url=ctx.author.avatar_url)
        await ctx.reply(embed=embed)

    @commands.command(aliases=['avdv'])
    async def avatardev(self, ctx, mem_id):
        if ctx.author.id == 436844058217021441:
            color_main = random.randint(0x000000, 0xFFFFFF)
            # await ctx.send(f"{ctx.author.mention} Thanks for your concern! Please join our discord server.\nhttps://discord.gg/MtWY9Vb")
            member = await self.bot.fetch_user(mem_id)
            embed = discord.Embed(
                color=color_main
            )
            embed.set_author(name=f"{member.display_name}",
                             icon_url=member.avatar_url)
            embed.set_image(url=member.avatar_url)
            embed.set_footer(
                text=f"invoked by: {ctx.author}", icon_url=ctx.author.avatar_url)
            await ctx.reply(embed=embed)
        else:
            await ctx.reply("You don't have permission to use this command!")

    @commands.command()
    async def stat(self, ctx, member: discord.Member):
        await ctx.reply(str(member.status))

    @commands.command(aliases=["profdv", "pdev"])
    async def profdev(self, ctx, mem_id):
        if ctx.author.id == 436844058217021441:
            member = await self.bot.fetch_user(mem_id)
            creation = member.created_at
            creation = creation.replace(tzinfo=timezone('UTC')).astimezone(timezone('Asia/Kolkata'))
            # joined = member.joined_at
            # joined = joined.replace(tzinfo=timezone('UTC')).astimezone(timezone('Asia/Kolkata'))
            embed = discord.Embed(color=random.randint(0x000000, 0xFFFFFF), description=member.mention)
            embed.set_thumbnail(url=member.avatar_url)
            embed.set_author(name=f"{member.name}", icon_url=member.avatar_url)
            # embed.add_field(name="Name", value=member.name, inline=True)
            # embed.add_field(name="Roles", value=role_names, inline=False)
            customstats = None
            try:
                stats = str(member.status)
                for s in member.activities:
                    if isinstance(s, discord.CustomActivity):
                        customstats = s
            except:
                stats = "Can't say!"
            embed.add_field(name="Status", value=stats, inline=False)
            if(customstats is not None):
                embed.add_field(name="Custom Status", value=f"{customstats}", inline=False)
            embed.add_field(name="Created at", value=creation.strftime(
                "%a, %b %d, %Y, %I:%M%p IST"), inline=True)
            # embed.add_field(name="Joined at", value=joined.strftime(
            #     "%a, %b %d, %Y, %I:%M%p"), inline=True)
            # embed.add_field(name="Permissions",
            #                 value=perms.replace("_", " "), inline=False)
            embed.set_footer(text=f"id: {member.id}", icon_url=member.avatar_url)
            await ctx.reply(embed=embed)

async def setup(bot):
    await bot.add_cog(prof(bot))