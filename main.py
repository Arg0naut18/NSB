import time
from selenium import webdriver
#importing necessary modules
import discord
from discord.ext import commands
import os
import json
from discord.ext import tasks
from itertools import cycle
import asyncio

# setting things up
j_file = open("secrets.txt")
vari = json.load(j_file)
j_file.close()
token = vari["token"]
def pref(client, message):
    BOT_PREFIX = ["sci ", "Sci ", "SCI "]
    return commands.when_mentioned_or(*BOT_PREFIX)(client, message)

intents = discord.Intents.all()
intents.members =True
bot = commands.Bot(command_prefix=pref,intents=intents,
                   owner_id=436844058217021441, case_insensitive=True, help_command = None)

#main thing starts here
@bot.event
async def on_ready():
    print("Logged in as: " + bot.user.name + "\n")

async def status():
    await bot.wait_until_ready()
    s = cycle([f"{len(bot.guilds)} servers.", "Prefix='sci'", "sci help", "GenosOP#6921's instructions"])
    while not bot.is_closed():
        await bot.change_presence(activity=discord.Activity(type = discord.ActivityType.watching, name = next(s)))
        await asyncio.sleep(10)
bot.loop.create_task(status())


@bot.command(aliases = ["l"])
async def load(ctx, extension):
    try:
        bot.load_extension(f"cogs1.{extension}")
        await ctx.send(f"{extension} loaded!")
    except Exception as e:
        await ctx.send(f"Error loading {extension}")
        print(e)


@bot.command(aliases = ["u"])
async def unload(ctx, extension):
    try:
        bot.unload_extension(f"cogs1.{extension}")
        await ctx.send(f"{extension} unloaded!")
    except Exception as e:
        await ctx.send(f"Error unloading {extension}")
        print(e)


@bot.command(aliases = ["r"])
async def reload(ctx, extension):
    try:
        bot.unload_extension(f"cogs1.{extension}")
        bot.load_extension(f"cogs1.{extension}")
        await ctx.send(f"{extension} re-loaded!")
    except Exception as e:
        await ctx.send(f"Error re-loading {extension}")
        print(e)


@bot.command(aliases = ["ra"])
async def reloadall(ctx):
    try:
        for file in os.listdir('./cogs1'):
            if file.endswith(".py"):
                bot.unload_extension(f"cogs1.{file[:-3]}")
                bot.load_extension(f"cogs1.{file[:-3]}")
        await ctx.send("All cogs reloaded!")
    except Exception as e:
        await ctx.send(f"Error re-loading cogs.")
        print(e)

for file in os.listdir('./cogs1'):
    if file.endswith(".py"):
        bot.load_extension(f"cogs1.{file[:-3]}")

bot.run(token)
