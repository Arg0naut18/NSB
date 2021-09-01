import discord
from discord.ext import commands
import json
import codeforces
import random
import urllib.request
from bs4 import BeautifulSoup

j_file = open("secrets.txt")
vari = json.load(j_file)
j_file.close()
key = vari["cfkey"]
secret = vari["cfsecret"]

class CodeForces(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def problem(self, ctx):
        contests = codeforces.api.call('contest.list', key=key, secret=secret)
        contest = random.choice(contests)
        contest_id = contest['id']
        index_list = ['A', 'B', 'C', 'D', 'E']
        index = random.choice(index_list)
        problem = codeforces.problem.get_info(contest_id, index, lang='en')
        examples = list(problem[3])
        url = f"https://codeforces.com/problemset/problem/{contest_id}/{index}"
        html_data = urllib.request.urlopen(url).read()
        soup = BeautifulSoup(html_data, 'lxml')
        statement = soup.find_all("p")
        inp = soup.find("div", class_="input-specification").text
        output = soup.find("div", class_="output-specification").text
        t = " "
        for i in range(3):
            t.join(statement[i].text.replace("$$$", " "))
        exampless = "\n"
        problemEmbed = discord.Embed(title=problem[0], color=random.randint(0x000000, 0xFFFFFF))
        problemEmbed.add_field(name="Statement", value=t+"...", inline=False)
        problemEmbed.add_field(name="Input Specification",value=inp, inline=False)
        problemEmbed.add_field(name="Output Specification",value=output, inline=False)
        exampless.join([f"Input:\n{examples[i][0]}\nOutput:\n{examples[i][1]}"] for i in range(len(examples)))
        problemEmbed.add_field(name="Examples", value=exampless, inline=False)
        await ctx.send(embed=problemEmbed)

def setup(bot):
    bot.add_cog((bot))