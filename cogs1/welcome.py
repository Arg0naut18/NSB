import discord
from discord.ext import commands
import random
from PIL import Image, ImageFont, ImageDraw, ImageOps, ImageFilter, ImageChops
from io import BytesIO

color = [15158332, 3066993, 10181046, 3447003, 1752220, 15844367]


class welcome(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        if member.guild.id == 711079029624537098:
            # channel = discord.channel.id(711083892068581377)
            camp_name = "Ɖɨʋɨռɛ"
            rule_channel = discord.utils.get(member.guild.text_channels, id=711440316695183386)
            channel = discord.utils.get(member.guild.text_channels, id=711083892068581377)
            role = discord.utils.get(member.guild.roles, id=771981552837328897)
            chat_channel = discord.utils.get(member.guild.text_channels, id=711086382579187794)
            await member.add_roles(role)
            #if channel.id == 765647163463434298:
            mssg = f"Welcome {member.mention} to camp {camp_name}'s official discord server!\n<a:right_arrow2:857929909966995487> Please read the rules mentioned in {rule_channel.mention}.\n<a:right_arrow2:857929909966995487> I hope you have a great time in our camp and our discord server. Feel free to chat in {chat_channel.mention} and ask help from any officials if needed."
            # await channel.send(mssg)
            # Welcome Image
            layout = Image.open(r"./meme_templates/heaven.jpg")
            asset = member.avatar_url_as(size=128)
            data = BytesIO(await asset.read())
            pfp = Image.open(data)
            bigsize = (pfp.size[0] * 3, pfp.size[1] * 3)
            mask = Image.new('L', bigsize, 0)
            draw = ImageDraw.Draw(mask)
            draw.ellipse((0, 0) + bigsize, fill=255)
            mask = mask.resize(pfp.size, Image.ANTIALIAS)
            #mask = ImageChops.darker(mask, pfp.split()[-1])
            pfp.putalpha(mask)
            pfp.crop((0, 0)+bigsize)
            pfp = pfp.resize((95, 95)).convert("RGBA")
            #pfp = mask_circle_transparent(pfp, 1)
            layout.paste(pfp, (162, 92), pfp)
            draw = ImageDraw.Draw(layout)
            font1 = ImageFont.truetype("./MPLUSRounded1c-Regular.ttf", 32)
            font2 = ImageFont.truetype("./BullettoKilla.ttf", 24)
            font3 = ImageFont.truetype("./BullettoKilla.ttf", 46)
            imgdesc = f"{member}"
            #w, h = draw.textsize(imgdesc)
            imgmssg = f"Welcome to DIVINE! Hope you have a blessed stay!"
            draw.text((275, 112), imgdesc, (0, 0, 0), font1)
            draw.text((45, 217), imgmssg, (0, 0, 0), font2)
            draw.text((194, 14), "WELCOME!", (0, 0, 0), font3)
            layout.save(r"./meme_templates/heavenedit.jpg")
            file=discord.File(r"./meme_templates/heavenedit.jpg", filename="image.png")
            welcomeEmbed = discord.Embed(description=mssg, color=0x00FF00)
            welcomeEmbed.set_author(name=f"Welcome {member.display_name}!", icon_url=member.avatar_url)
            welcomeEmbed.set_image(url="attachment://image.png")
            await channel.send(file=file, embed=welcomeEmbed)

    @commands.Cog.listener()
    async def on_member_leave(self, member):
        if member.guild.id == 711079029624537098:
            camp_name = "Ɖɨʋɨռɛ"
            channel = discord.utils.get(member.guild.text_channels, id=848168452505075782)
            leaveEmbed = discord.Embed(title=f"{member.name} just left {camp_name}")
            leaveEmbed.set_author(name=f"{member.name}", icon_url=member.avatar_url)
            leaveEmbed.set_footer(text=f"Now we have {channel.guild.member_count} members left.")
            await channel.send(embed=leaveEmbed)

    @ commands.command()
    async def intro(self, ctx):
        dev_name = "Argonaut#6921"
        dev_id = 436844058217021441
        #camp_name = "Ɖɨʋɨռɛ"
        dev = await self.bot.fetch_user(dev_id)
        msg = f"Thanks for you're concern. I am a \
bot developed by {dev} to help you out or entertain you in your daily busy lives."
        color_main = color[random.randint(0, 5)]
        embed = discord.Embed(
            title=":wave: Intro!", description=msg, color=color_main)
        await ctx.send(embed=embed)

    @commands.command()
    async def invitelink(self, ctx):
        await ctx.reply("Invite link for NSB\nhttps://discord.com/api/oauth2/authorize?client_id=743741872039657492&permissions=2130701687&scope=bot")

def setup(bot):
    bot.add_cog(welcome(bot))