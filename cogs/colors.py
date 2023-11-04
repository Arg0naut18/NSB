import discord
from discord.ext import commands
import random
from PIL import Image, ImageFont, ImageDraw, ImageOps, ImageFilter, ImageChops
from io import BytesIO
import json


async def get_color_list():
    with open('./colors/colors.json', 'r') as f:
        color_list = json.load(f)
    return color_list


async def make_color_list(user):
    with open('./colors/colors.json', 'r') as f:
        colors = json.load(f)
    if str(user.guild.id) in colors:
        return False
    else:
        colors[str(user.guild.id)] = {}
        colors[str(user.guild.id)]["id"] = len(colors.keys())
    with open('./colors/colors.json', 'w') as f:
        json.dump(colors, f, indent=4)


class Colors(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.content.startswith("color : "):
            com, color = message.content.lower().split(": ")
            collist = await get_color_list()
            if color in collist[str(message.guild.id)]:
                for rol in collist[str(message.guild.id)]:
                    if rol in [r.name for r in message.author.roles]:
                        role = discord.utils.get(message.guild.roles, name=rol)
                        await message.author.remove_roles(role)
                role = discord.utils.get(message.guild.roles, id=collist[str(message.guild.id)][color][1])
                col = collist[str(message.guild.id)][color][0].replace("#", "0x")
                await message.author.add_roles(role)
                successmsg = discord.Embed(title="Success",
                                           description=f"Added role **{role.name}** to **{message.author.display_name}**!",
                                           color=discord.Colour(int(col, 16)))
                await message.channel.send(embed=successmsg)
            else:
                erroremb = discord.Embed(title="Error",
                                         description="This color doesn't exist as a role in this server. You can add it using add color command.")
                await message.channel.send(embed=erroremb)

    @commands.group()
    @commands.has_permissions(administrator=True)
    async def add(self, ctx):
        if ctx.invoked_subcommand is None:
            pass

    @add.group()
    async def color(self, ctx, colorname, colorhex):
        try:
            await make_color_list(ctx.author)
            colorname = str(colorname).lower()
            colorhex = colorhex.replace("#", "")
            col = discord.Colour(int(f"0x{colorhex}", 16))
            role = await ctx.guild.create_role(name=str(colorname), color=col)
            colorembed = discord.Embed(title=f"Success", description=f"Successfully added {colorname} to the roles.",
                                       color=col)
            await ctx.send(embed=colorembed)
            color_list = await get_color_list()
            color_list[str(ctx.guild.id)][colorname] = ['0x' + str(colorhex), role.id]
            with open('./colors/colors.json', 'w') as f:
                json.dump(color_list, f, indent=4)
        except Exception as e:
            emb = discord.Embed(title="Error Occurred!",
                                description="Lacking permission. Please check that the role of this bot is on top of the users that r gonna access it.",
                                color=0x00ff00)
            await ctx.send(embed=emb)
            raise e

    @add.group()
    async def default(self, ctx):
        try:
            await make_color_list(ctx.author)
            with open('./colors/colors.json', 'r') as f:
                colors = json.load(f)
            default_colors = colors["default"]
            def_cols = list(default_colors.items())

            i = 0
            for role in ctx.guild.roles:
                if "NotSoBasic" in role.name:
                    i += 1
                    break
                i += 1
            for item in def_cols:
                all_roles = await ctx.guild.fetch_roles()
                num_roles = len(all_roles) - i + 1
                print(num_roles, i, len(all_roles))
                color = discord.Colour(int(item[1], 16))
                role = await ctx.guild.create_role(name=item[0], color=color)
                i+=1
                await role.edit(position=num_roles)
                colors[str(ctx.guild.id)][str(item[0])] = [item[1], role.id]
            colorembed = discord.Embed(title=f"Success", description=f"Successfully added default colors to the roles.",
                                       color=0x00ff00)
            with open('./colors/colors.json', 'w') as f:
                json.dump(colors, f, indent=4)
            await ctx.send(embed=colorembed)
        except Exception as e:
            emb = discord.Embed(title="Error Occurred!",
                                description="Lacking permission. Please check that the role of this bot is on top of the users that r gonna access it.",
                                color=0x00ff00)
            await ctx.send(embed=emb)
            raise e

    @commands.command()
    async def colorlist(self, ctx):
        colors = await get_color_list()
        layout = Image.open(r"./colors/transbgm.png")
        layout.resize((300, 300))
        draw = ImageDraw.Draw(layout)
        font = ImageFont.truetype("./fonts/MPLUSRounded1c-Bold.ttf", 100)
        xoffset, yoffset = 10, 10
        i = 1
        try:
            colorlist = colors[str(ctx.guild.id)]
        except:
            await ctx.send("The list is empty for this server.")
            return
        for color in list(colors[str(ctx.guild.id)].items()):
            if color[0] == "id":
                continue
            col = color[1][0].replace("0x", "#")
            txt = str(i) + "." + color[0]
            draw.text((xoffset, yoffset), txt, font=font, fill=col)
            yoffset += 200
            i += 1
            if (i - 1) % 5 == 0:
                xoffset += 600
                yoffset = 10
        layout.save("colistedit.png")
        file = discord.File(r"colistedit.png", filename="image.png")
        await ctx.send(file=file)

    @commands.command()
    async def clearlist(self, ctx):
        collist = await get_color_list()
        for rol in collist[str(ctx.guild.id)]:
            if rol in [r.name for r in ctx.guild.roles]:
                role = discord.utils.get(ctx.guild.roles, name=rol)
                try:
                    await ctx.author.remove_roles(role)
                except:
                    pass
                await role.delete()
        del collist[str(ctx.guild.id)]
        with open(r'./colors/colors.json', 'w') as f:
            json.dump(collist, f, indent=4)
        await ctx.send("Successfully cleared list.")

    @commands.command()
    async def showcolor(self, ctx, hexcode):
        if "0x" in hexcode:
            hexcode = hexcode.replace("0x", "#")
        if "#" not in hexcode:
            await ctx.send("Invalid hexcode!")
        layout = Image.open(r"./colors/whitebgm.jpg")
        layout.resize((200, 200))
        img = Image.new('RGB', (300, 300), hexcode)
        layout.paste(img)
        layout.save(r"coloredit.jpg")
        file = discord.File(r"coloredit.jpg", filename="color.png")
        hexcode = hexcode.replace("#", "")
        col = discord.Colour(int(f"0x{hexcode}", 16))
        colorembed = discord.Embed(title=f"{hexcode}", color=col)
        colorembed.set_image(url="attachment://color.png")
        await ctx.send(embed=colorembed, file=file)


async def setup(bot):
    await bot.add_cog(Colors(bot))