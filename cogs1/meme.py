import discord
from discord.ext import commands
import random
import praw
import json
from PIL import Image, ImageFont, ImageDraw
from io import BytesIO
import textwrap

color = [15158332, 3066993, 10181046, 3447003, 1752220, 15844367]
j_file = open("secrets.txt")
vari = json.load(j_file)
j_file.close()
client_id1 = vari["client_id"]
client_secret1 = vari["client_secret"]
user_agent1 = vari["user_agent"]
reddit = praw.Reddit(client_id=client_id1, client_secret=client_secret1,
                     user_agent=user_agent1, check_for_async=False)

class meme(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['memes', 'm'])
    async def meme(self, ctx):
        meme = ['memes', 'cursedcomments', 'animememes',
                'dankmemes']
        main_meme = random.choice(meme)
        color_main = random.choice(color)
        memes_submissions = reddit.subreddit(main_meme).top()
        post_to_pick = random.randint(1, 100)
        for i in range(0, post_to_pick):
            submission = next(x for x in memes_submissions if not x.stickied)
        slink = f'{submission.shortlink}'
        embed = discord.Embed(
            title=f"__{submission.title}__", color=color_main, url=slink)
        embed.set_image(url=submission.url)
        embed.set_footer(
            text=f'👍 {submission.score} | meme by u/{submission.author}  from {memes_submissions.url}')
        await ctx.reply(embed=embed)

    @commands.command(aliases=['awww'])
    async def aww(self, ctx):
        meme = ['aww', 'AnimalsBeingBros', 'NatureIsFuckingLit']
        main_meme = meme[random.randint(0, len(meme)-1)]
        color_main = color[random.randint(0, len(color)-1)]
        memes_submissions = reddit.subreddit(main_meme).new()
        post_to_pick = random.randint(1, 100)
        for i in range(0, post_to_pick):
            submission = next(x for x in memes_submissions if not x.stickied)
            slink = f'{submission.shortlink}'
            headerText = f"{submission.title}  [{slink}]"
            mainPart = submission.url
            footerText = f'Post by u/{submission.author}  from {memes_submissions.url}'
            await ctx.send(headerText+'\n'+mainPart+'\n'+footerText)
            break
            # if isVideo(submission.url):
            #     print("video!")
            #     slink = f'{submission.shortlink}'
            #     await ctx.reply(slink)
            #     await ctx.send(submission.url)
            #     break
            # else:
            #     embed = discord.Embed(
            #         title=f"__{submission.title}__, color=color_main, url=slink)
            #     embed.set_image(url=submission.url)
            #     embed.set_footer(
            #         text=f'Post by u/{submission.author}  from {memes_submissions.url}')
            #     await ctx.reply(embed=embed)
            #     break

    @commands.command()
    async def wanted(self, ctx, member: discord.Member = None):
        member = ctx.author if not member else member
        wanted = Image.open(r"./meme_templates/wanted.jpg")
        # 216,278  186,251
        asset = member.avatar_url_as(size=128)
        data = BytesIO(await asset.read())
        pfp = Image.open(data)
        pfp = pfp.resize((216, 278))
        wanted.paste(pfp, (186, 251))
        wanted.save(r"./meme_templates/wantprof.jpg")
        await ctx.send(file=discord.File(r"./meme_templates/wantprof.jpg"))

    @commands.command()
    async def delete(self, ctx, member: discord.Member = None):
        member = ctx.author if not member else member
        garb = Image.open(r"./meme_templates/garbage.jpg").convert('RGB')
        # 216,278  186,251
        asset = member.avatar_url_as(size=128)
        data = BytesIO(await asset.read())
        pfp = Image.open(data)
        pfp = pfp.resize((79, 78))
        garb.paste(pfp, (48, 54))
        garb.save(r"./meme_templates/garbagedit.jpg")
        await ctx.send(file=discord.File(r"./meme_templates/garbagedit.jpg"))    
        
    @commands.command()
    async def suntzu(self, ctx, *, msg):
        img = Image.open(r"./meme_templates/suntzu.jpg")
        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype("./MPLUSRounded1c-Regular.ttf", 42)
        # 669,359 446,142
        msg = "\n".join(textwrap.wrap(msg, width=34))
        draw.text((510, 211), msg, (255, 255, 255), font)
        img.save(r"./meme_templates/suntzuedit.jpg")
        await ctx.send(file=discord.File(r"./meme_templates/suntzuedit.jpg"))

    @commands.command()
    async def gandhi(self, ctx, *, msg):
        img = Image.open(r"./meme_templates/gandhi.jpg")
        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype("./MPLUSRounded1c-Regular.ttf", 15)
        # 669,359 446,142
        msg = "\n".join(textwrap.wrap(msg, width=18))
        draw.text((144, 29), msg, (255, 255, 255), font)
        img.save(r"./meme_templates/gandhiedit.jpg")
        await ctx.send(file=discord.File(r"./meme_templates/gandhiedit.jpg"))

    @commands.command()
    async def brain(self, ctx, *, msg):
        img = Image.open(r"./meme_templates/brain.jpg")
        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype("./MPLUSRounded1c-Regular.ttf", 20)
        # 669,359 446,142
        msg = "\n".join(textwrap.wrap(msg, width=25))
        draw.text((10, 276), msg, (0, 0, 0), font)
        img.save(r"./meme_templates/brainedit.jpg")
        await ctx.send(file=discord.File(r"./meme_templates/brainedit.jpg"))


def setup(bot):
    bot.add_cog(meme(bot))