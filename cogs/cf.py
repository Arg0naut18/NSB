import discord
from discord.ext import commands
import json
import codeforces
import random
import urllib.request
from bs4 import BeautifulSoup
import re
from configs import CODEFORCES_KEY, CODEFORCES_SECRET


async def get_problem():
    contests = codeforces.api.call('contest.list', key=CODEFORCES_KEY, secret=CODEFORCES_SECRET)
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
    for i in range(2):
        st=(statement[i].text.replace("$$$", " "))
        t+=re.sub(r'[^a-zA-Z0-9_ ]',' ',st)
    return [url, problem, examples, inp, output, t]


class CodeForces(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['cf', 'codeforces'])
    async def cfproblem(self, ctx):
        attr = await get_problem()
        color_embed = random.randint(0x000000, 0xFFFFFF)
        problem_embed = discord.Embed(title=attr[1][0], color=color_embed, url=attr[0])
        problem_embed.add_field(name="Statement", value=attr[5]+"...", inline=False)
        problem_embed.add_field(name="Input Specification",value=attr[3][5:], inline=False)
        problem_embed.add_field(name="Output Specification",value=attr[4][6:], inline=False)
        await ctx.send(embed=problem_embed)
        ex = []
        for i in range(len(attr[2])):
            ex.append(f"```Input:\n{attr[2][i][0]}\nOutput:\n{attr[2][i][1]}```")
        exampless = "\n".join(ex)
        example_embed=discord.Embed(title="Examples:", description=exampless, color=color_embed)
        await ctx.send(embed=example_embed)

async def setup(bot):
    await bot.add_cog(CodeForces(bot))