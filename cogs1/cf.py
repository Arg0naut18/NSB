import discord
from discord.ext import commands
import json
import codeforces
import random
import urllib.request
from bs4 import BeautifulSoup
import re

j_file = open("divinesecrets.txt")
vari = json.load(j_file)
j_file.close()
key = vari["cfkey"]
secret = vari["cfsecret"]

async def get_problem():
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
        colorEmbed = random.randint(0x000000, 0xFFFFFF)
        problemEmbed = discord.Embed(title=attr[1][0], color=colorEmbed, url=attr[0])
        problemEmbed.add_field(name="Statement", value=attr[5]+"...", inline=False)
        problemEmbed.add_field(name="Input Specification",value=attr[3][5:], inline=False)
        problemEmbed.add_field(name="Output Specification",value=attr[4][6:], inline=False)
        await ctx.send(embed=problemEmbed)
        ex = []
        for i in range(len(attr[2])):
            ex.append(f"```Input:\n{attr[2][i][0]}\nOutput:\n{attr[2][i][1]}```")
        exampless = "\n".join(ex)
        exampleEmbed=discord.Embed(title="Examples:", description=exampless, color=colorEmbed)
        await ctx.send(embed=exampleEmbed)

async def setup(bot):
    await bot.add_cog(CodeForces(bot))