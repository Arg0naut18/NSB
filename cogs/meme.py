import discord
from typing import Optional
from discord.ext import commands
import random
import praw
import os
from PIL import Image, ImageFont, ImageDraw
from io import BytesIO
import textwrap

color = [15158332, 3066993, 10181046, 3447003, 1752220, 15844367]
reddit = praw.Reddit(client_id=os.getenv("REDDIT_CLIENT_ID"), client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
                     user_agent=os.getenv("REDDIT_USER_AGENT"), check_for_async=False)

class meme(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.font = "./fonts/MPLUSRounded1c-Regular.ttf"

    @commands.hybrid_command(description = "Shows a meme", aliases=['memes', 'm'])
    async def meme(self, ctx: commands.Context):
        await ctx.defer(ephemeral=False)
        meme = ['memes', 'cursedcomments', 'animememes',
                'dankmemes']
        main_meme = random.choice(meme)
        color_main = random.choice(color)
        memes_submissions = reddit.subreddit(main_meme).top()
        post_to_pick = random.randint(1, 100)
        for _ in range(0, post_to_pick):
            submission = next(x for x in memes_submissions if not x.stickied)
        slink = f'{submission.shortlink}'
        embed = discord.Embed(
            title=f"__{submission.title}__", color=color_main, url=slink)
        embed.set_image(url=submission.url)
        embed.set_footer(
            text=f'👍{submission.score}   💬{submission.num_comments}\nMeme by u/{submission.author}  from {memes_submissions.url}')
        await ctx.reply(embed=embed)

    @commands.hybrid_command(description="Cuteness Overloaded", aliases=['awww'])
    async def aww(self, ctx):
        await ctx.defer(ephemeral=False)
        meme = ['aww', 'AnimalsBeingBros', 'NatureIsFuckingLit']
        main_meme = meme[random.randint(0, len(meme)-1)]
        memes_submissions = reddit.subreddit(main_meme).new()
        post_to_pick = random.randint(1, 100)
        for _ in range(0, post_to_pick):
            submission = next(x for x in memes_submissions if not x.stickied)
            slink = f'{submission.shortlink}'
            header_text = f"{submission.title}  [{slink}]"
            main_part = submission.url
            footer_text = f'Post by u/{submission.author}  from {memes_submissions.url}'
            await ctx.send(header_text+'\n'+main_part+'\n'+footer_text)
            break

    @commands.hybrid_command(description="Make someone wanted")
    async def wanted(self, ctx: commands.Context, member: Optional[discord.Member] = None):
        await ctx.defer(ephemeral=False)
        member = ctx.author if not member else member
        wanted = Image.open(r"./meme_templates/wanted.jpg")
        # 216,278  186,251
        asset = member.avatar.with_size(128)
        data = BytesIO(await asset.read())
        pfp = Image.open(data)
        pfp = pfp.resize((216, 278))
        wanted.paste(pfp, (186, 251))
        wanted.save(r"./meme_templates/wantprof.jpg")
        await ctx.send(file=discord.File(r"./meme_templates/wantprof.jpg"))

    @commands.hybrid_command(description="Turn someone into garbage")
    async def delete(self, ctx: commands.Context, member: Optional[discord.Member] = None):
        await ctx.defer(ephemeral=False)
        member = ctx.author if not member else member
        garb = Image.open(r"./meme_templates/garbage.jpg").convert('RGB')
        # 216,278  186,251
        asset = member.avatar.with_size(128)
        data = BytesIO(await asset.read())
        pfp = Image.open(data)
        pfp = pfp.resize((79, 78))
        garb.paste(pfp, (48, 54))
        garb.save(r"./meme_templates/garbagedit.jpg")
        await ctx.send(file=discord.File(r"./meme_templates/garbagedit.jpg"))    
        
    @commands.hybrid_command(description="Quote SunTzu")
    async def suntzu(self, ctx: commands.Context, *, msg: str):
        await ctx.defer(ephemeral=False)
        img = Image.open(r"./meme_templates/suntzu.jpg")
        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype(self.font, 42)
        # 669,359 446,142
        msg = "\n".join(textwrap.wrap(msg, width=34))
        draw.text((510, 211), msg, (255, 255, 255), font)
        img.save(r"./meme_templates/suntzuedit.jpg")
        await ctx.send(file=discord.File(r"./meme_templates/suntzuedit.jpg"))

    @commands.hybrid_command(description="Quote Gandhi")
    async def gandhi(self, ctx: commands.Context, *, msg: str):
        await ctx.defer(ephemeral=False)
        img = Image.open(r"./meme_templates/gandhi.jpg")
        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype(self.font, 15)
        # 669,359 446,142
        msg = "\n".join(textwrap.wrap(msg, width=18))
        draw.text((144, 29), msg, (255, 255, 255), font)
        img.save(r"./meme_templates/gandhiedit.jpg")
        await ctx.send(file=discord.File(r"./meme_templates/gandhiedit.jpg"))

    @commands.hybrid_command(description="Brain wakes u up meme")
    async def brain(self, ctx: commands.Context, *, msg:str):
        await ctx.defer(ephemeral=False)
        img = Image.open(r"./meme_templates/brain.jpg")
        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype(self.font, 20)
        # 669,359 446,142
        msg = "\n".join(textwrap.wrap(msg, width=25))
        draw.text((10, 276), msg, (0, 0, 0), font)
        img.save(r"./meme_templates/brainedit.jpg")
        await ctx.send(file=discord.File(r"./meme_templates/brainedit.jpg"))

    @commands.hybrid_command(description="Create a fake minecraft achievement")
    async def achievement(self, ctx: commands.Context, *, text: str):
        await ctx.defer(ephemeral=False)
        for c in text:
            if c==" ":
                text = text.replace(" ", "+")
        url = f"https://minecraftskinstealer.com/achievement/11/Advancement+Made%21/{text}"
        await ctx.send(url)
        
async def setup(bot):
    await bot.add_cog(meme(bot))