import discord
from discord.ext import commands
import random
from PIL import Image, ImageFont, ImageDraw, ImageOps, ImageFilter, ImageChops
from io import BytesIO
import json


async def get_servers():
    with open(r'./welcome/welcome.json') as f:
        servers = json.load(f)
    return servers


async def open_account(user):
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
    with open(r'./bank/bank.json', 'w') as f:
        json.dump(users, f, indent=4)
    return True


async def get_account_data():
    with open(r"./bank/bank.json", 'rb') as j:
        bank = json.load(j)
    return bank


class welcome(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    #@commands.Cog.listener()
    #async def on_member_join(self, member):
    #    servers = await get_servers()
    #    if member.guild.id == 743741348578066442:
    #        await open_account(member)
    #        users = await get_account_data()
    #        users[str(member.id)]["multiplier"] += 1
    #        with open(r"./bank/bank.json", 'w') as bank:
    #            json.dump(users, bank, indent=4)
    #    if str(member.guild.id) in servers:
    #        server_name = member.guild.name
    #        welcome_channel = discord.utils.get(member.guild.text_channels, id=servers[str(member.guild.id)]["welcomechannel"])
    #        rule_channel = discord.utils.get(member.guild.text_channels, id=servers[str(member.guild.id)]["rulechannel"])
    #        chat_channel = discord.utils.get(member.guild.text_channels, id=servers[str(member.guild.id)]["chatchannel"])
    #        role = None
    #        if "role" in servers[str(member.guild.id)]:
    #            role = servers[str(member.guild.id)]["role"]
    #        ext = "th"
    #        if member.guild.member_count%10==1:
    #            ext="st"
    #        elif member.guild.member_count%10==2:
    #            ext="nd"
    #        elif member.guild.member_count%10==3:
    #            ext="rd"
    #        mssg = f"Welcome {member.mention} to {server_name}'s official discord server! Your are the {member.guild.member_count}{ext}  member\n<a:right_arrow2:857929909966995487> Please read the rules mentioned in {rule_channel.mention}.\n<a:right_arrow2:857929909966995487> I hope you have a great time in our discord server.\n<a:right_arrow2:857929909966995487>  Feel free to get started in {chat_channel.mention}\n<a:right_arrow2:857929909966995487> Feel free to ask help from any mods if needed."
    #        layout = Image.open(servers[str(member.guild.id)]["imagelocation"])
    #        asset = member.avatar_url_as(size=128)
    #        data = BytesIO(await asset.read())
    #        pfp = Image.open(data)
    #        bigsize = (pfp.size[0] * 3, pfp.size[1] * 3)
    #        mask = Image.new('L', bigsize, 0)
    #        draw = ImageDraw.Draw(mask)
    #        draw.ellipse((0, 0) + bigsize, fill=255)
    #        mask = mask.resize(pfp.size, Image.ANTIALIAS)
            # mask = ImageChops.darker(mask, pfp.split()[-1])
    #        pfp.putalpha(mask)
    #        pfp.crop((0, 0)+bigsize)
    #        pfp = pfp.resize((servers[str(member.guild.id)]["sizes"]["pfpsize"], servers[str(member.guild.id)]["sizes"]["pfpsize"])).convert("RGBA")
            # pfp = mask_circle_transparent(pfp, 1)
    #        layout.paste(pfp, (servers[str(member.guild.id)]["coordinates"]["pfp"][0], servers[str(member.guild.id)]["coordinates"]["pfp"][1]), pfp)
    #        draw = ImageDraw.Draw(layout)
    #        font1 = ImageFont.truetype("./MPLUSRounded1c-Medium.ttf", servers[str(member.guild.id)]["sizes"]["font1"])
    #        font2 = ImageFont.truetype("./MPLUSRounded1c-Bold.ttf", servers[str(member.guild.id)]["sizes"]["font2"])
    #        font3 = ImageFont.truetype("./BullettoKilla.ttf", servers[str(member.guild.id)]["sizes"]["font3"])
    #        imgdesc = f"{member}"
            # w, h = draw.textsize(imgdesc)
    #        if "belowmessage" in servers[str(member.guild.id)]:
    #            imgmssg = servers[str(member.guild.id)]["belowmessage"].format(member.guild.name)
                # imgmssg = servers[str(member.guild.id)]["belowmessage"].format("Ɖɨʋɨռɛ")
    #            draw.text((servers[str(member.guild.id)]["coordinates"]["belowmessage"][0], servers[str(member.guild.id)]["coordinates"]["belowmessage"][1]), imgmssg, (servers[str(member.guild.id)]["color"][0], servers[str(member.guild.id)]["color"][1], servers[str(member.guild.id)]["color"][2]), font2)
    #        draw.text((servers[str(member.guild.id)]["coordinates"]["membername"][0], servers[str(member.guild.id)]["coordinates"]["membername"][1]), imgdesc, (servers[str(member.guild.id)]["color"][0], servers[str(member.guild.id)]["color"][1], servers[str(member.guild.id)]["color"][2]), font1)
    #        draw.text((servers[str(member.guild.id)]["coordinates"]["welcome"][0], servers[str(member.guild.id)]["coordinates"]["welcome"][1]), "WELCOME!", (servers[str(member.guild.id)]["color"][0], servers[str(member.guild.id)]["color"][1], servers[str(member.guild.id)]["color"][2]), font3)
    #        layout.save(r"./welcome/welcomeedit.jpg")
    #        file = discord.File(r"./welcome/welcomeedit.jpg", filename="image.png")
    #        await welcome_channel.send(f"{member.mention}")
    #        welcomeEmbed = discord.Embed(description=mssg, color=0x00FF00)
    #        welcomeEmbed.set_author(name=f"Welcome {member.display_name}!", icon_url=member.avatar_url)
    #        welcomeEmbed.set_image(url="attachment://image.png")
    #        await welcome_channel.send(file=file, embed=welcomeEmbed)
    #        if role is not None:
    #            role_ = discord.utils.get(member.guild.roles, id=int(role))
    #            await member.add_roles(role_)
        
    #@commands.Cog.listener()
    #async def on_member_remove(self, member):
    #    if member.guild.id == 711079029624537098:
    #        camp_name = "Ɖɨʋɨռɛ"
    #        channel = discord.utils.get(member.guild.text_channels, id=848168452505075782)
    #        leaveEmbed = discord.Embed(title=f"{member.name} just left {camp_name}", color=0x00FF00)
    #        leaveEmbed.set_author(name=f"{member.name}", icon_url=member.avatar_url)
    #        leaveEmbed.set_footer(text=f"Now we have {channel.guild.member_count} members left.")
    #        await channel.send(embed=leaveEmbed)
    #    if member.guild.id == 743741348578066442:
    #        await open_account(member)
    #        users = await get_account_data()
    #        users[str(member.id)]["multiplier"] -= 1
    #        with open(r"./bank/bank.json", 'w') as bank:
    #            json.dump(users, bank, indent=4)
    
    @commands.command()
    async def intro(self, ctx):
        dev_name = "Argonaut#6921"
        dev_id = 436844058217021441
        # camp_name = "Ɖɨʋɨռɛ"
        dev = await self.bot.fetch_user(dev_id)
        msg = f"Thanks for you're concern. I am a \
bot developed by {dev} to help you out or entertain you in your daily busy lives."
        embed = discord.Embed(
            title=":wave: Intro!", description=msg, color=0x00FF00)
        await ctx.send(embed=embed)

    @commands.command()
    async def invitelink(self, ctx):
        await ctx.reply("Invite link for NSB\nhttps://discord.com/api/oauth2/authorize?client_id=743741872039657492&permissions=2130701687&scope=bot")

    @commands.command()
    @commands.is_owner()
    async def update_multiplier(self, ctx):
        users = await get_account_data()
        for user in ctx.guild.members:
            if str(user.id) in users:
                users[str(user.id)]["multiplier"]=2
        with open(r"./bank/bank.json", 'w') as bank:
            json.dump(users, bank, indent=4)


async def setup(bot):
    await bot.add_cog(welcome(bot))