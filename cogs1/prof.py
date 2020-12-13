import discord
from discord.ext import commands
import random


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
        joined = member.joined_at
        perm_list = [perm[0] for perm in member.guild_permissions if perm[1]]
        perms = ", ".join([str(x) for x in perm_list])

        embed = discord.Embed(color=color_main, description=member.mention)
        embed.set_thumbnail(url=member.avatar_url)
        embed.set_author(name=f"{member.name}", icon_url=member.avatar_url)
        # embed.add_field(name="Name", value=member.name, inline=True)
        embed.add_field(name="Roles", value=role_names, inline=False)
        embed.add_field(name="Status", value=str(member.status), inline=False)
        embed.add_field(name="Created at", value=creation.strftime("%a, %b %d, %Y, %I:%M%p"), inline=True)
        embed.add_field(name="Joined at", value=joined.strftime("%a, %b %d, %Y, %I:%M%p"), inline=True)
        embed.add_field(name="Permissions", value=perms.replace("_", " "), inline=False)
        embed.set_footer(text=f"id: {member.id}", icon_url=member.avatar_url)
        await ctx.send(embed=embed)
        # else:
        #     roles = member.roles
        #     role_s = [role.mention for role in roles]
        #     role_names = " ".join([str(x) for x in role_s[:0:-1]])
        #     # role_perms = [role.permissions.value for role in member.roles]
        #     # permissions = member.guild_permissions
        #     # perms = " ".join([str(x) for x in role_perms])
        #     creation = member.created_at
        #     joined = member.joined_at
        #     perm_list = [perm[0] for perm in member.guild_permissions if perm[1]]
        #     perms = ", ".join([str(x) for x in perm_list])

        #     embed = discord.Embed(title=f"__{member}__", color=color_main, description=member.mention)
        #     embed.set_thumbnail(url = member.avatar_url)
        #     # embed.add_field(name="Name", value=member.name, inline=True)
        #     embed.add_field(name="Roles", value=role_names, inline=False)
        #     embed.add_field(name="Status", value=str(member.status), inline=False)
        #     embed.add_field(name="Created at", value=creation.strftime("%a, %b %d, %Y, %I:%M%p"), inline=True)
        #     embed.add_field(name="Joined at", value=joined.strftime("%a, %b %d, %Y, %I:%M%p"), inline=True)
        #     embed.add_field(name="Permissions", value=perms.replace("_", " "), inline=False)
        #     embed.set_footer(text=f"id: {member.id}")
        #     await ctx.send(embed=embed)

    @commands.command(aliases=['av'])
    async def avatar(self, ctx, member: discord.Member = None):
        color_main = random.randint(0x000000, 0xFFFFFF)
        # await ctx.send(f"{ctx.author.mention} Thanks for your concern! Please join our discord server.\nhttps://discord.gg/MtWY9Vb")
        member = ctx.author if not member else member
        embed = discord.Embed(
            color=color_main
        )
        embed.set_author(name=f"{member.display_name}", icon_url=member.avatar_url)
        embed.set_image(url=member.avatar_url)
        embed.set_footer(text=f"invoked by: {ctx.author}", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)

    @commands.command()
    async def stat(self, ctx, member: discord.Member):
        await ctx.send(str(member.status))


def setup(bot):
    bot.add_cog(prof(bot))
