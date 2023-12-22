import discord
from discord.ext import commands
from discord import TextChannel, app_commands
import random
import asyncio
import datetime
import json
from typing import Optional
import DiscordUtils
from utils.db import db

picchannels = [801811950119157790, 711217046272344094, 753632407332192366, 711095542486269964,
               771968223797051413, 780830237512433675, 778548218110803998, 827201189439078442]
ytchannel = [747320665073385493]
common = [753914881727660062, 753632407332192366, 818192348793798667,
          711086134956130370, 747320665073385493, 770503986364547093, 711089041482711101, 770503986364547093, 711090925417267211, 851024775169703936, 855814133898412052]
notypezone = [711087692582223873]
blocked_words = []
level_check = [822527895296933918]
dbe = db.economy

async def open_account(user):
    check = await dbe.find_one({"_id": str(user.id)})
    if check is None:
        insert = {
            "_id": str(user.id), "wallet": 0, "bank": 0, "maxbank": 15000, "safe": 0, "multiplier": 1, "usedmulti": 0 
        }
        await dbe.insert_one(insert)
    with open(r'./bank/bank.json', 'r') as f:
        users = json.load(f)
    if str(user.id) in users:
        return False
    else:
        users[str(user.id)] = {}
        users[str(user.id)]["wallet"] = 0
        users[str(user.id)]["bank"] = 0
        users[str(user.id)]["maxbank"] = 15000
        users[str(user.id)]["safe"] = 0
        users[str(user.id)]["multiplier"] = 1
        users[str(user.id)]["usedmulti"] = 0
    with open(r'./bank/bank.json', 'w') as f:
        json.dump(users, f, indent=4)
    return True

async def get_account_data(user=None):
    if user is None:
        with open(r'./bank/bank.json', 'r') as j:
            users = json.load(j)
        return users
    data = await dbe.find_one({"_id": str(user.id)})
    return data

class moderation(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, mssg):
        channel = mssg.channel
        if mssg.guild is not None:
            if mssg.guild.id == 743741348578066442:
                if channel.id == 764073807627157515:
                    if mssg.content.lower() == "nsb verify":
                        role = discord.utils.get(mssg.guild.roles, id=764059798719037460)
                        await mssg.author.add_roles(role)
                        await mssg.delete()
                        member = mssg.author
                        await open_account(member)
                        users = await get_account_data()
                        users[str(member.id)]["multiplier"]=2
                        with open(r"./bank/bank.json", 'w') as bank:
                            json.dump(users, bank, indent=4)
            
            if mssg.guild.id == 711079029624537098:
                if channel.id in notypezone:
                    if not mssg.author.bot:
                        await mssg.delete()
                if channel.id != 753632407332192366:
                    words = mssg.content.split(" ")
                    for word in words:
                        if word in blocked_words:
                            await mssg.delete()
                            nsfw = discord.utils.get(mssg.guild.text_channels, id=753632407332192366)
                            resp = await channel.send(f"U used a bad word. Please refrain from using it. U can use it in {nsfw.mention}")
                            await asyncio.sleep(10)
                            await resp.delete()
                if not channel.id in common:
                    if len(mssg.attachments) > 0:
                        if channel.id not in picchannels:
                            if not mssg.author.bot:
                                await mssg.delete()
                                picC1 = discord.utils.get(mssg.guild.text_channels, id=801811950119157790)
                                picC2 = discord.utils.get(mssg.guild.text_channels, id=711217046272344094)
                                resp = await channel.send(f"Please send the image in {picC1.mention} or {picC2.mention}")
                                await asyncio.sleep(10)
                                await resp.delete()
                        #elif mssg_sp != None:
                    elif "https://youtu.be/" in mssg.content and channel.id not in ytchannel:
                        if not mssg.author.bot:
                            await mssg.delete()
                            yt = discord.utils.get(mssg.guild.text_channels, id=747320665073385493)
                            respo = await channel.send(f"Please send the link in {yt.mention}")
                            await asyncio.sleep(10)
                            await respo.delete()
                    elif "!rank" in mssg.content.lower() and channel.id not in level_check:
                        if not mssg.author.bot:
                            await mssg.delete()
                            levelChannel = discord.utils.get(mssg.guild.text_channels, id=822527895296933918)
                            respo = await channel.send(f"Please use this command in {levelChannel.mention}")
                            await asyncio.sleep(10)
                            await respo.delete()
                            await mssg.channel.purge(limit=1)

    @commands.hybrid_command()
    @commands.has_permissions(administrator=True)
    async def announce(self, ctx, chan: TextChannel, *, mssg):
        await ctx.defer()
        if chan:
            embed = discord.Embed(
                title="Announcement!", description=mssg, color=random.randint(0x000000, 0xFFFFFF))
            await chan.send(embed=embed)
        else:
            await ctx.send("Channel not found!")
            
    @commands.hybrid_command()
    @app_commands.rename(msgID="msgid")
    @commands.has_permissions(administrator=True)
    async def editannounce(self, ctx, msgID, *, newmsg):
        await ctx.defer()
        for channel in ctx.guild.channels:
            try:
                msg = await channel.fetch_message(msgID)
            except:
                pass
        embed = discord.Embed(
                title="Announcement!", description=newmsg, color=random.randint(0x000000, 0xFFFFFF))
        await msg.edit(embed=embed)
        await ctx.send("Announcement edited!")
    
    @commands.hybrid_command()
    @commands.is_owner()
    async def leaveserver(self, ctx, guild : discord.Guild = None):
        guild = ctx.guild if guild is None else guild
        await guild.leave()
        await ctx.author.send(f"Successfully left {guild.name}!")

    @commands.hybrid_command(aliases=["purge", "prune"])
    @commands.has_permissions(manage_channels=True)
    async def clear(self, ctx, amount:Optional[int]=10):
        await ctx.defer()
        await ctx.channel.purge(limit=(amount + 1))

    @commands.hybrid_command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        await ctx.defer()
        try:
            await member.ban(reason=reason)
            await ctx.channel.purge(limit=1)
            respo = await ctx.send(f'User {member} has been kick')
            await asyncio.sleep(10)
            await respo.delete()
        except discord.Forbidden:
            respo=await ctx.send("Role is too high for me to access!")
            await asyncio.sleep(10)
            await respo.delete()

    # The below code unbans player.
    @commands.hybrid_command()
    @commands.has_permissions(administrator=True)
    async def unban(self, ctx, *, member):
        await ctx.defer()
        banned_users = await ctx.guild.bans()
        member_name, member_discriminator = member.split("#")
        for ban_entry in banned_users:
            user = ban_entry.user
            if (user.name, user.discriminator) == (member_name, member_discriminator):
                await ctx.guild.unban(user)
                await ctx.channel.purge(limit=1)
                respo=await ctx.send(f'Unbanned {user.mention}')
                await asyncio.sleep(10)
                await respo.delete()
                return

    # The below code kicks player
    @commands.hybrid_command()
    @commands.has_permissions(ban_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        await ctx.defer()
        try:
            await member.kick(reason=reason)
            await ctx.channel.purge(limit=1)
            respo = await ctx.send(f'User {member} has been kick')
            await asyncio.sleep(10)
            await respo.delete()
        except discord.Forbidden:
            respo=await ctx.send("Role is too high for me to access!")
            await asyncio.sleep(10)
            await respo.delete()

    @commands.hybrid_command(aliases=["tempmute"])
    @commands.has_permissions(ban_members=True)
    async def mute(self, ctx, member: discord.Member, *, reason=None):
        await ctx.defer()
        role = discord.utils.get(ctx.guild.roles, id = 711447121391255602)
        try:
            await member.add_roles(role)
            await ctx.channel.purge(limit=1)
            respo=await ctx.send(f'User {member.mention} has been muted for 10 minutes!')
            await asyncio.sleep(10)
            await respo.delete()
            await asyncio.sleep(590)
            await member.remove_roles(role)
            respo=await ctx.send(f"User {member.mention} has been unmuted now! Please don't repeat the same mistake :pray:.")
            await asyncio.sleep(10)
            await respo.delete()
        except discord.Forbidden:
            respo=await ctx.send("Role is too high for me to access!")
            await asyncio.sleep(10)
            await respo.delete()

    @commands.hybrid_command(aliases=["permamute", "pmute"])
    @commands.has_permissions(ban_members=True)
    async def permmute(self, ctx, member: discord.Member, *, reason=None):
        await ctx.defer()
        role = discord.utils.get(ctx.guild.roles, id = 711447121391255602)
        try:
            await member.add_roles(role)
            await ctx.channel.purge(limit=1)
            respo=await ctx.send(f'User {member.mention} has been muted indefinitely!')
            await asyncio.sleep(10)
            await respo.delete()
        except discord.Forbidden:
            respo=await ctx.send("Role is too high for me to access!")
            await asyncio.sleep(10)
            await respo.delete()

    @commands.hybrid_command()
    @commands.has_permissions(ban_members=True)
    async def unmute(self, ctx, member: discord.Member, *, reason=None):
        await ctx.defer()
        role = discord.utils.get(ctx.guild.roles, id = 711447121391255602)
        try:
            await member.remove_roles(role)
            await ctx.channel.purge(limit=1)
            respo=await ctx.send(f"User {member.mention} has been unmuted now! Please don't repeat the same mistake :pray:.")
            await asyncio.sleep(10)
            await respo.delete()
        except discord.Forbidden:
            respo=await ctx.send("Role is too high for me to access!")
            await asyncio.sleep(10)
            await respo.delete()

    @commands.hybrid_command(description="Lock a channel")
    @commands.has_permissions(administrator=True)
    async def chlock(self, ctx, channel: discord.TextChannel = None):
        await ctx.defer()
        time = 100000
        timeInHrs = time/3600
        channel = channel or ctx.channel
        overwrite = channel.overwrites_for(ctx.guild.default_role)
        overwrite.send_messages = False
        await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
        # msg = await ctx.send('Channel locked.')
        msg = discord.Embed(title=":lock: Channel Locked! :lock:")
        msg.timestamp = datetime.datetime.now()
        msg.add_field(name="Channel", value=f"{channel.mention}", inline=False)
        # msg.add_field(name="Duration (By Default)", value=f"{0:.2f} hours".format(timeInHrs), inline=False)
        msg.add_field(name="Duration (By Default)", value=f"{'%0.2f'%timeInHrs} Hours", inline=False)
        msg.set_footer(text=f"Invoked by {ctx.author.display_name}", icon_url=f"{ctx.author.avatar_url}")
        embed = await channel.send(embed=msg)
        await asyncio.sleep(time)
        await embed.delete()
        overwrite.send_messages = True
        await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
        msg = await ctx.send('Channel is unlocked :unlock:.')
        await asyncio.sleep(10)
        await msg.delete()

    @commands.hybrid_command(description="Unlocks a locked channel")
    @commands.has_permissions(administrator=True)
    async def chunlock(self, ctx, channel: discord.TextChannel = None):
        await ctx.defer()
        channel = channel or ctx.channel
        overwrite = channel.overwrites_for(ctx.guild.default_role)
        overwrite.send_messages = True
        await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
        msg = await channel.send('Channel is unlocked :unlock:. Please ignore any embed stating the channel is still locked if u r able to message here.')
        await asyncio.sleep(10)
        await msg.delete()
        await ctx.message.delete()

async def setup(bot):
    await bot.add_cog(moderation(bot))