import discord
from discord.ext import commands
import random
import praw
import json

color = [15158332, 3066993, 10181046, 3447003, 1752220, 15844367]
j_file = open("secrets.txt")
vari = json.load(j_file)
j_file.close()
client_id1 = vari["client_id"]
client_secret1 = vari["client_secret"]
user_agent1 = vari["user_agent"]
reddit = praw.Reddit(client_id = client_id1, client_secret = client_secret1, user_agent = user_agent1)


class meme(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases = ['memes', 'm'])
    async def meme(self, ctx):
        meme = ['memes', 'cursedcomments', 'animememes', 'dankmemes', 'historymemes', 'AdviceAnimals', 'starterpacks']
        main_meme = meme[random.randint(0, len(meme)-1)]
        color_main = color[random.randint(0,len(color)-1)]
        memes_submissions = reddit.subreddit(main_meme).top()
        post_to_pick = random.randint(1, 100)
        for i in range(0, post_to_pick):
            submission = next(x for x in memes_submissions if not x.stickied)
        slink = f'{submission.shortlink}'
        embed = discord.Embed(title=f"__{submission.title}__", color=color_main, url=slink)
        embed.set_image(url = submission.url)
        embed.set_footer(text = f'meme by u/{submission.author}  from {memes_submissions.url}')
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(meme(bot))
