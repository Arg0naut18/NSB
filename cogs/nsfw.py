import discord
from discord.ext import commands
import random
import praw
import json
import urllib.request
from PIL import Image, ImageFont, ImageDraw
from io import BytesIO
import textwrap
from configs import CLIENT_ID, CLIENT_SECRET, USER_AGENT

color = [15158332, 3066993, 10181046, 3447003, 1752220, 15844367]
reddit = praw.Reddit(client_id=CLIENT_ID, client_secret=CLIENT_SECRET,
                     user_agent=USER_AGENT, check_for_async=False)

async def get_account_data():
    with open(r'./bank/bank.json', 'r') as j:
        users = json.load(j)
    return users

class nsfw(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['hpic'])
    @commands.is_nsfw()
    async def hentaipic(self, ctx):
        users = await get_account_data()
        user = ctx.author
        item = "hpic"
        amount = 1
        try:
            inv = users[str(user.id)]["bag"]
        except:
            await ctx.send("You don't own anything to use.")
            return
        found = 0
        for index in range(len(inv)):
            if item == inv[index]["item"]:
                if inv[index]["amount"]-amount==0:
                    del inv[index]
                    found = 1
                    break
                else:
                    inv[index]["amount"]-=amount
                    found = 1
                    break
        if found==1:
            meme = ['Hentai', 'AnimeMILFS', 'Paizuri']
            main_meme = meme[random.randint(0, len(meme)-1)]
            color_main = color[random.randint(0, len(color)-1)]
            memes_submissions = reddit.subreddit(main_meme).top()
            post_to_pick = random.randint(1, 100)
            for i in range(0, post_to_pick):
                submission = next(x for x in memes_submissions if not x.stickied)
            slink = f'{submission.shortlink}'
            embed = discord.Embed(
                title=f"__{submission.title}__", color=color_main, url=slink)
            embed.set_image(url=submission.url)
            embed.set_footer(
                text=f'meme by u/{submission.author}  from {memes_submissions.url}')
            await ctx.reply(embed=embed)
        else:
            await ctx.send("You need to have atleast 1 Hentai Pic in your inventory to use this command. You can buy it from the shop.")
        with open(r'./bank/bank.json',"w") as f:
            json.dump(users, f)    

async def setup(bot):
    await bot.add_cog(nsfw(bot))
