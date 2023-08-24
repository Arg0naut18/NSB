#importing necessary modules

import discord
from discord import app_commands, utils
from discord.ext import commands, tasks
from discord.ext.commands import has_permissions
import os
import datetime
from interruptingcow import timeout
import random
import json
import asyncio
from dbUtil.db import db

# setting the secrets
j_file = open("divinesecrets.txt")
vari = json.load(j_file)
j_file.close()
TOKEN = vari["TOKEN"]
token = vari["nsbtoken"]
ipcsecret = vari["ipcsecret"]
dev_id = 436844058217021441
guild_id = 743741348578066442

class button_view(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="verify", style=discord.ButtonStyle.green, custom_id="verify")
    async def verify(self, interaction: discord.Interaction, button: discord.ui.Button):
        if type(MyBot.verRole) is not discord.Role:
            MyBot.verRole = interaction.guild.get_role()
        if MyBot.verRole not in interaction.user.roles:
            await interaction.user.add_roles(MyBot.verRole)
            await interaction.response.send_message(f"You are now {MyBot.verRole.mention}!", ephemeral=True)
        else:
            await interaction.response.send_message(f"You already are {MyBot.verRole.mention}!", ephemeral=True)

class MyBot(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.verRole = 764059798719037460
        self.added = False
        self.db = db
        #self.synced = False
    
    async def on_ready(self):
        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"Prefix: nsb | {len(bot.guilds)} guilds and {len(bot.users)} members."))
        if not self.added:
            self.add_view(button_view())
            self.added = True
        print("Logged in as: " + bot.user.name + "\n")
        
    async def setup_hook(self):
        for file in os.listdir('./divinecogs'):
            if file.endswith(".py"):
                with timeout(300, exception=RuntimeError):
                    print(f"Loading divinecogs.{file[:-3]}...")
                    await bot.load_extension(f"divinecogs.{file[:-3]}")
                    print(f"divinecogs.{file[:-3]} loaded!")
        #if not self.synced:
        await self.tree.sync()
            #self.synced = True
        
        
        #self.ipc=ipc.Server(self, secret_key=ipcsecret)
    #async def on_ipc_ready(self):
        #print("IPC ready!")
    #async def on_ipc_error(self, endpoint, error):
        #print(endpoint, "raised", error)

def get_prefix(client, message):
    if message.guild is None: return commands.when_mentioned_or('nsb ')(client, message)
    try:
        with open('./prefixes/prefixes.json', 'r') as f:
            prefixes = json.load(f)
            prefixes_list = [prefixes[str(message.guild.id)], prefixes[str(message.guild.id)].lower(), prefixes[str(message.guild.id)].upper(), prefixes[str(message.guild.id)].title()]
            return commands.when_mentioned_or(*prefixes_list)(client, message)
        
    except KeyError: # if the guild's prefix cannot be found in 'prefixes.json'
        with open('./prefixes/prefixes.json', 'r') as k:
            prefixes = json.load(k)
        prefixes[str(message.guild.id)] = 'nsb '

        with open('./prefixes/prefixes.json', 'w') as j:
            json.dump(prefixes, j, indent = 4)

        with open('./prefixes/prefixes.json', 'r') as t:
            prefixes = json.load(t)
            return prefixes[str(message.guild.id)]
        
    except: # I added this when I started getting dm error messages
        pass

intents = discord.Intents.all()
intents.members = True
bot = MyBot(command_prefix=(get_prefix), intents=intents, owner_id=436844058217021441,
                   case_insensitive=True, help_command=None, description="Made by Argonaut#6921 for NSB")

#main thing starts here

@bot.event
async def on_guild_join(guild): #when the bot joins the guild
    with open('./prefixes/prefixes.json', 'r') as f: #read the prefix.json file
        prefixes = json.load(f) #load the json file

    prefixes[str(guild.id)] = 'nsb '#default prefix

    with open('./prefixes/prefixes.json', 'w') as f: #write in the prefix.json "message.guild.id": "bl!"
        json.dump(prefixes, f, indent=4) #the indent is to make everything look a bit neater
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"Prefix: nsb | {len(bot.guilds)} guilds and {len(bot.users)} members."))    

@bot.event
async def on_guild_remove(guild): #when the bot is removed from the guild
    with open('./prefixes/prefixes.json', 'r') as f: #read the file
        prefixes = json.load(f)
    prefixes.pop(str(guild.id)) #find the guild.id that bot was removed from
    with open('./prefixes/prefixes.json', 'w') as f: #deletes the guild.id as well as its prefix
        json.dump(prefixes, f, indent=4)
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"Prefix: nsb | {len(bot.guilds)} guilds and {len(bot.users)} members."))

@bot.hybrid_command(description="Sync all slash commands")
@commands.is_owner()
async def syncall(ctx):
    await commands.Bot.tree.sync()

@bot.hybrid_command(description="Change the prefix for this guild", pass_context=True, aliases=["setprefix"])
@has_permissions(administrator=True) #ensure that only administrators can use this command
async def changeprefix(ctx, *, prefix): #command: bl!changeprefix ...
    with open('./prefixes/prefixes.json', 'r') as f:
        prefixes = json.load(f)

    prefixes[str(ctx.guild.id)] = prefix

    with open('./prefixes/prefixes.json', 'w') as f: #writes the new prefix into the .json
        json.dump(prefixes, f, indent=4)

    await ctx.send(f'Prefix changed to: {prefix}') #confirms the prefix it's been changed to
#next step completely optional: changes bot nickname to also have prefix in the nickname

@bot.hybrid_command(name="verify", description="Gives you member role to be able to access the server.")
@app_commands.guilds(discord.Object(743741348578066442))
@commands.is_owner()
async def verify(interaction: discord.Interaction):
    await interaction.response.send_message(view=button_view())

@bot.hybrid_command(name="help", with_app_command=True, description="Helps you use the bot")
async def help(ctx: commands.Context, category=None):
    prefix = get_prefix(bot, ctx.message)
    if category is None:
        emb = discord.Embed(
            # title="__**NSB COMMANDS:**__", color=random.randint(0x000000, 0xFFFFFF))
            title="__**NSB COMMANDS:**__", color=random.randint(0x000000, 0xFFFFFF))
        emb.add_field(name="Prefix", value=f"`{prefix[2]}`", inline=False)
        emb.add_field(name=":tools: Moderation", value=f"`{prefix[2]}help moderation`", inline=True)
        emb.add_field(name=":joy: Memes", value=f"`{prefix[2]}help memes`", inline=True)
        emb.add_field(name=":slight_smile: Trivial", value=f"`{prefix[2]}help trivial`", inline=True)
        emb.add_field(name=":arrow_forward: Youtube", value=f"`{prefix[2]}help youtube`", inline=True)
        emb.add_field(name=":musical_keyboard: Music", value=f"`{prefix[2]}help music`", inline=True)
        emb.add_field(name=":notebook_with_decorative_cover: Educational", value=f"`{prefix[2]}help edu`", inline=True)
        emb.add_field(name=":hugging: Emotes", value=f"`{prefix[2]}help emotes`", inline=True)
        emb.add_field(name=":man_zombie: Lifeafter", value=f"`{prefix[2]}help la`", inline=True)
        emb.add_field(name=":money_with_wings: Economy", value=f"`{prefix[2]}help economy`", inline=True)
        emb.set_thumbnail(url=bot.user.avatar.url)
        emb.set_footer(text=f"Invoked by {ctx.author.display_name}. Type {prefix[2]}vote to support the bot.",icon_url=ctx.author.avatar.url)
        emb.timestamp = datetime.datetime.now()
        await ctx.send(embed=emb, ephemeral=True)
        await ctx.send("Stuck? Need help? Join our community server!\nhttps://discord.gg/Q8Xtjs4SAt", ephemeral=True)
    
    elif category.lower() == "moderation":
        msg = f"All the moderation commands require your role to have **Administrator Permissions** or **Banning Permissions** in case of ban, kick and mute.\n\n·announce\n`{prefix[2]}announce #<channel-name> <message>`\n\n·profile\n`{prefix[2]}prof`\n\n·clear/purge (clears chats)\n`{prefix[2]}clear 50`\n\n·mute\n`{prefix[2]}mute <character mention>`\n\n·kick\n`{prefix[2]}kick <character mention>`\n\n·ban\n`{prefix[2]}ban <character mention>`\n\n·Channel Lock\n`{prefix[2]}chlock <channel-name (optional)>`\n\n·Channel Unlock\n`{prefix[2]}chunlock`\n\nTHANK YOU"
        emb = discord.Embed(title=":tools: __**NSB MODERATION COMMANDS:**__", description=msg, color=random.randint(0x000000, 0xFFFFFF))
        emb.set_footer(
            text=f"Invoked by {ctx.author.display_name}", icon_url=ctx.author.avatar_url)
        emb.timestamp = datetime.datetime.now()
        await ctx.send(embed=emb)
    
    elif category.lower() == "memes":
        msg = f"·meme\n`{prefix[2]}meme`\n\n·aww\n`{prefix[2]}aww`\n\n·wanted\n`{prefix[2]}wanted <@member>`\n\n·gandhi\n`{prefix[2]}gandhi <quote>`\n\n·suntzu\n`{prefix[2]}suntzu <quote>`\n\n·brain\n`{prefix[2]}brain <something that can keep u awake>`\n\nTHANK YOU"
        emb = discord.Embed(title=":joy: __**NSB MEMES COMMANDS:**__",
                            description=msg, color=random.randint(0x000000, 0xFFFFFF))
        emb.set_footer(
            text=f"Invoked by {ctx.author.display_name}", icon_url=ctx.author.avatar_url)
        emb.timestamp = datetime.datetime.now()
        await ctx.send(embed=emb)
    
    elif category.lower() == "trivial":
        msg = f"·8ball\n`{prefix[2]}8ball Am I gonna be rich?`\n\n·giveaway(gstart)\n`{prefix[2]}gstart`\n\n·translate\n`{prefix[2]}translate <word>`\n\n·reactrole (reaction roles rolemenu setup)\n`{prefix[2]}reactrole  <channel=optional>`\n\nTHANK YOU"
        emb = discord.Embed(title=":slight_smile: __**NSB TRIVIAL COMMANDS:**__",
                            description=msg, color=random.randint(0x000000, 0xFFFFFF))
        emb.set_footer(
            text=f"Invoked by {ctx.author.display_name}", icon_url=ctx.author.avatar_url)
        emb.timestamp = datetime.datetime.now()
        await ctx.send(embed=emb)
    
    elif category.lower() == "youtube" or category.lower() == "yt":
        msg = f"·yts (Youtube search)\n`{prefix[2]}yts <youtube video name>`\n\n·subs\n`{prefix[2]}subs PewDiePie`\n\n·ytc(subs comparison)\n`{prefix[2]}ytc PewDiePie tseries`\n\nTHANK YOU"
        emb = discord.Embed(title=":arrow_forward: __**NSB YOUTUBE COMMANDS:**__",
                            description=msg, color=random.randint(0x000000, 0xFFFFFF))
        emb.set_footer(
            text=f"Invoked by {ctx.author.display_name}", icon_url=ctx.author.avatar_url)
        emb.timestamp = datetime.datetime.now()
        await ctx.send(embed=emb)
    
    elif category.lower() == "edu" or category.lower() == "educational":
        msg = f"·wiki\n`{prefix[2]}wiki Shahrukh Khan`\n\n·dictionary\n`{prefix[2]}define <word>`\n\n·sol (solve equations upto 3 variables)\n`{prefix[2]}sol x+y-3 x-y-1`\n\n·differentiate\n`{prefix[2]}derivate x^2+2x+1`\n\n·integrate\n`{prefix[2]}integrate x^2+2x+1`\n\n·atom\n`{prefix[2]}atom Uranium`\n\n·Periodic Table\n`{prefix[2]}ptable`\n\n·Molar Mass\n`{prefix[2]}mass H2SO4`\n\nTHANK YOU"
        emb = discord.Embed(title=":notebook_with_decorative_cover: __**NSB EDUCATIONAL COMMANDS:**__",
                            description=msg, color=random.randint(0x000000, 0xFFFFFF))
        emb.set_footer(
            text=f"Invoked by {ctx.author.display_name}", icon_url=ctx.author.avatar_url)
        emb.timestamp = datetime.datetime.now()
        await ctx.send(embed=emb)
    
    elif category.lower() == "emotes":
        msg = f"·gif\n`{prefix[2]}gif <gif name>`\n\n·hug\n`{prefix[2]}hug <@member>`\n\n·punch\n`{prefix[2]}punch <@member>`\n\n·nom\n`{prefix[2]}nom <@member>`\n\n·slap\n`{prefix[2]}slap <@member>`\n\n·kill\n`{prefix[2]}kill <@member>`\n\n·pat\n`{prefix[2]}pat <@member>`\n\n·dance\n`{prefix[2]}dance <@member>`\n\n·birthday\n`{prefix[2]}bday <@member>`\n\nTHANK YOU"
        emb = discord.Embed(title=":hugging: __**NSB EMOTE COMMANDS:**__",
                            description=msg, color=random.randint(0x000000, 0xFFFFFF))
        emb.set_footer(
            text=f"Invoked by {ctx.author.display_name}", icon_url=ctx.author.avatar_url)
        emb.timestamp = datetime.datetime.now()
        await ctx.send(embed=emb)

    elif category.lower() == "music":
        msg = f"·play\n`{prefix[2]}play <song name>`\n\n·pause\n`{prefix[2]}pause`\n\n·stop\n`{prefix[2]}stop`\n\n·leave\n`{prefix[2]}dc`\n\n·queue\n`{prefix[2]}queue`\n\n·skip\n`{prefix[2]}skip`\n\nTHANK YOU"
        emb = discord.Embed(title=":musical_keyboard: __**NSB MUSIC COMMANDS:**__",
                            description=msg, color=random.randint(0x000000, 0xFFFFFF))
        emb.set_footer(
            text=f"Invoked by {ctx.author.display_name}", icon_url=ctx.author.avatar_url)
        emb.timestamp = datetime.datetime.now()
        await ctx.send(embed=emb)
    
    elif category.lower() == "lifeafter" or category.lower() == "la":
        msg = f"·res (Maps with resource)\n`{prefix[2]}res <name-of-resource>`\n\n·<name-of-map> (To get the name of the resources of the map.)\n`{prefix[2]}<name-of-map>`\n\nTHANK YOU"
        emb = discord.Embed(title=":man_zombie: __**NSB LIFEAFTER COMMANDS:**__",
                            description=msg, color=random.randint(0x000000, 0xFFFFFF))
        emb.set_footer(
            text=f"Invoked by {ctx.author.display_name}", icon_url=ctx.author.avatar_url)
        emb.timestamp = datetime.datetime.now()
        await ctx.send(embed=emb)

    elif category.lower() == "economy":
        msg = f"·Balance\n`{prefix[2]}balance <@member>/<member_id>`\n\n·Beg\n`{prefix[2]}beg`\n\n·Rob\n`{prefix[2]}rob <@member>/<member_id>`\n\n·Give\n`{prefix[2]}give <@member>/<member_id> <amount>`\n\n·Deposit\n`{prefix[2]}deposit <amount>`\n\n·Withdraw\n`{prefix[2]}withdraw <amount>`\n\n·work\n`{prefix[2]}work`\n\n·shop\n`{prefix[2]}shop`\n\n·Buy\n`{prefix[2]}buy <item_name>`\n\n·Hunting\n`{prefix[2]}hunt`\n\n·Fishing\n`{prefix[2]}fish`\n\n·Use\n`{prefix[2]}use <item_name>`\n\n·Inventory\n`{prefix[2]}inv`\n\n------NSFW Command------\n\n·hpic (`Works only if you have atleast 1 hpic in your inventory`)\n`{prefix[2]}hpic`\n\nTHANK YOU"
        emb = discord.Embed(title=":money_with_wings: __**NSB ECONOMY COMMANDS:**__",
                            description=msg, color=random.randint(0x000000, 0xFFFFFF))
        emb.set_footer(
            text=f"Invoked by {ctx.author.display_name}", icon_url=ctx.author.avatar_url)
        emb.timestamp = datetime.datetime.now()
        await ctx.send(embed=emb)


        
@bot.hybrid_command(description="Loads a cog", aliases=["l"])
@commands.is_owner()
async def load(ctx: commands.Context, extension: str):
    if ctx.message.author.id == dev_id:
        try:
            await bot.load_extension(f"divinecogs.{extension}")
            respo = await ctx.reply(f"{extension} loaded!")
            print(f"{extension} loaded!")
            await asyncio.sleep(5)
            await respo.delete()
            try:
                await ctx.message.delete()
            except:
                pass
        except Exception as e:
            respo = await ctx.reply(f"Error loading {extension}")
            await asyncio.sleep(5)
            await respo.delete()
            try:
                await ctx.message.delete()
            except:
                pass
            print(e)

@bot.hybrid_command(description="Unloads a cog", aliases=["u"])
@commands.is_owner()
async def unload(ctx: commands.Context, extension: str):
    if ctx.message.author.id == dev_id:
        try:
            await bot.unload_extension(f"divinecogs.{extension}")
            respo = await ctx.send(f"{extension} unloaded!", ephemeral=True)
            await asyncio.sleep(5)
            await respo.delete()
            try:
                await ctx.message.delete()
            except:
                pass
        except Exception as e:
            respo = await ctx.send(f"Error unloading {extension}", ephemeral=True)
            await asyncio.sleep(5)
            await respo.delete()
            try:
                await ctx.message.delete()
            except:
                pass
            print(e)


@bot.hybrid_command(description="Reloads a cog", aliases=["r"])
@commands.is_owner()
async def reload(ctx: commands.Context, extension: str):
    if ctx.message.author.id == dev_id:
        try:
            await bot.unload_extension(f"divinecogs.{extension}")
            await bot.load_extension(f"divinecogs.{extension}")
            respo = await ctx.send(f"{extension} re-loaded!", ephemeral=True)
            await asyncio.sleep(5)
            await respo.delete()
            try:
                await ctx.message.delete()
            except:
                pass
        except Exception as e:
            respo = await ctx.send(f"Error re-loading {extension}", ephemeral=True)
            await asyncio.sleep(5)
            await respo.delete()
            try:
                await ctx.message.delete()
            except:
                pass
            print(e)


@bot.hybrid_command(description="Reloads all cogs", aliases=["ra"])
@commands.is_owner()
async def reloadall(ctx: commands.Context):
    if ctx.message.author.id == dev_id:
        try:
            for file in os.listdir('./divinecogs'):
                if file.endswith(".py"):
                    await bot.unload_extension(f"divinecogs.{file[:-3]}")
                    await bot.load_extension(f"divinecogs.{file[:-3]}")
                    respo = await ctx.reply(f"All Divine cogs reloaded!")
                    await asyncio.sleep(5)
                    await respo.delete()
                    try:
                        await ctx.message.delete()
                    except:
                        pass
        except Exception as e:
            respo = await ctx.reply(f"Error re-loading divinecogs.")
            await asyncio.sleep(5)
            await respo.delete()
            try:
                await ctx.message.delete()
            except:
                pass
            print(e)
            
bot.run(token)