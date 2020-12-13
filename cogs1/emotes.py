import discord
from discord.ext import commands
import random

color = [15158332, 3066993, 10181046, 3447003, 1752220, 15844367]

class emotes(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        # self.member = member

    @commands.command()
    async def hug(self, ctx, member: discord.Member = None):
        if member is None:
            await ctx.send("You can't hug yourself! lol")
        else:
            urls = ['https://media.tenor.com/images/4d5a77b99ab86fc5e9581e15ffe34b5e/tenor.gif',
            'https://media1.tenor.com/images/11b756289eec236b3cd8522986bc23dd/tenor.gif?itemid=10592083',
            'https://media1.tenor.com/images/452bf03f209ca23c668826ffa07ea6a7/tenor.gif?itemid=15965620',
            'https://media1.tenor.com/images/fd47e55dfb49ae1d39675d6eff34a729/tenor.gif?itemid=12687187',
            'https://media1.tenor.com/images/f3ffd3669c13ee8d091a6b583976efe9/tenor.gif?itemid=9322908',
            'https://cdn.weeb.sh/images/BysjuO7D-.gif']
            color_main = color[random.randint(0,len(color)-1)]
            embed = discord.Embed(title=(f'__***{ctx.author.name}***__ just hugged __***{member.name}***__') ,color=color_main)
            embed.set_image(url=urls[random.randint(0, len(urls)-1)])
            await ctx.send(embed=embed)

    @commands.command(aliases = ['hbd'])
    async def bday(self, ctx, member: discord.Member):
        urls = ['https://media.tenor.com/images/e37ae589afa0cffe7c9957bee26e36cc/tenor.gif',
                'https://media.tenor.com/images/72fead26968d18a5846f02298dacb3b3/tenor.gif',
                'https://media.tenor.com/images/ee1cd9269f1872a5eb31cef9b86a20cd/tenor.gif',
                'https://media.tenor.com/images/ac4f49e01b8d289c16271e2187ee62d8/tenor.gif',
                'https://media.tenor.com/images/25d627f3e0f09fe712f8b9fd4bd675cb/tenor.gif',
                'https://media.tenor.com/images/0b6f0b738d777f1f393492918ef94eda/tenor.gif']
        color_main = color[random.randint(0,len(color)-1)]
        embed = discord.Embed(title=(f'__***{ctx.author.name} and NotSoBasicBot***__ is wishing **Happy Birthday** to __***{member.name}***__') ,color=color_main)
        embed.set_image(url=urls[random.randint(0, len(urls)-1)])
        await ctx.send(embed=embed)

    @commands.command()
    async def punch(self, ctx, member: discord.Member = None):
        if member is None:
            await ctx.send("You don't wanna punch yourself do you? lol")
        else:
            urls = ['https://i.chzbgr.com/full/6531699968/h446929A1/ya-like-my-zangief-impression-doc',
            'https://media0.giphy.com/media/AlsIdbTgxX0LC/giphy.gif',
            'https://media1.giphy.com/media/11HeubLHnQJSAU/giphy.gif?cid=ecf05e47ducbjg7i13ay8wyxrqu4ir3x5vovozl5stw4e1um&rid=giphy.gif',
            'https://media2.giphy.com/media/xULW8EM7Br1usb0s9O/giphy.gif?cid=ecf05e47ducbjg7i13ay8wyxrqu4ir3x5vovozl5stw4e1um&rid=giphy.gif',
            'https://media3.giphy.com/media/GoN89WuFFqb2U/giphy.gif?cid=ecf05e47newmpccn5poukaf496q8dx12fazspr7v86owyic6&rid=giphy.gif',
            'https://media3.giphy.com/media/RkLaH1ptACyAzQ1dWj/giphy.gif?cid=ecf05e47b99bf549bf0f9d706d40d906ae4686eddd55d337&rid=giphy.gif']
            color_main = color[random.randint(0,len(color)-1)]
            embed = discord.Embed(title=(f'__***{ctx.author.name}***__ just punched __***{member.name}***__') ,color=color_main)
            embed.set_image(url=urls[random.randint(0, len(urls)-1)])
            await ctx.send(embed=embed)

    @commands.command()
    async def slap(self, ctx, member: discord.Member = None):
        if member is None:
            urls = ['https://media4.giphy.com/media/S7EOLaVLLTPNuIFUHT/giphy.gif?cid=ecf05e477iprb3tp8c173xvxsym9geky10acmpx69zojufir&rid=giphy.gif',
            'https://media2.giphy.com/media/2nGfl4QfpCtW/giphy.gif?cid=ecf05e477iprb3tp8c173xvxsym9geky10acmpx69zojufir&rid=giphy.gif',
            'https://media1.giphy.com/media/q8AiNhQJVyDoQ/giphy.gif?cid=ecf05e47df40091nuwwrqdo8nbw6cy2r2xbi0ot2a4vwx7rs&rid=giphy.gif']
            color_main = color[random.randint(0,len(color)-1)]
            embed = discord.Embed(title=(f'__***{ctx.author.name}***__ just slapped themselves. Wierd!') ,color=color_main)
            embed.set_image(url=urls[random.randint(0, len(urls)-1)])
            await ctx.send(embed=embed)
        else:
            urls = ['https://media4.giphy.com/media/Gf3AUz3eBNbTW/giphy.gif?cid=ecf05e470ab7ia5vgss64ntvnmwj2v0b6dg8q2yxyft5uyjy&rid=giphy.gif',
            'https://media1.giphy.com/media/k1uYB5LvlBZqU/giphy.gif?cid=ecf05e47e1efc2fb975b942072a24b70e9faef0d90ed3e81&rid=giphy.gif',
            'https://media1.giphy.com/media/10DRaO76k9sgHC/giphy.gif?cid=ecf05e470ab7ia5vgss64ntvnmwj2v0b6dg8q2yxyft5uyjy&rid=giphy.gif',
            'https://media0.giphy.com/media/3XlEk2RxPS1m8/giphy.gif?cid=ecf05e47486a0f0cef11ddd3b254e9c37ab326f8b254bda3&rid=giphy.gif',
            'https://media0.giphy.com/media/htiVRuP7N0XK/giphy.gif?cid=ecf05e477dd392a9f80fc10b58ae47c3af36eea496449063&rid=giphy.gif',
            'https://media2.giphy.com/media/3o752gPI09ZLYk84Ok/giphy.gif?cid=ecf05e47ead92fdffe9293b39f8d43042e4eeb13b5bbb84f&rid=giphy.gif']
            color_main = color[random.randint(0,len(color)-1)]
            embed = discord.Embed(title=(f'__***{ctx.author.name}***__ just slapped __***{member.name}***__') ,color=color_main)
            embed.set_image(url=urls[random.randint(0, len(urls)-1)])
            await ctx.send(embed=embed)

    @commands.command()
    async def kill(self, ctx, member: discord.Member = None):
        if member is None:
            await ctx.send("You don't wanna kill yourself do you? lol")
        else:
            urls = ['https://media1.tenor.com/images/ff2dcd44504000e320c21ae5682b5369/tenor.gif?itemid=5749160',
            'https://media.tenor.com/images/e4f4de39be542c0820a7725b767ec1a0/tenor.gif',
            'https://media.tenor.com/images/dba9097be6354e9be123441eacdad947/tenor.gif',
            'https://media.tenor.com/images/edf55b40599fb382f7a8c87e609d5094/tenor.gif',
            'https://media.tenor.com/images/5b25354209f6de4b064f0833f5eca8ad/tenor.gif',
            'https://media.tenor.com/images/557bcc935fe237761da4963e3213bd2e/tenor.gif']
            color_main = color[random.randint(0,len(color)-1)]
            embed = discord.Embed(title=(f'__***{ctx.author.name}***__ just killed __***{member.name}***__') ,color=color_main)
            embed.set_image(url=urls[random.randint(0, len(urls)-1)])
            await ctx.send(embed=embed)

    @commands.command()
    async def nom(self, ctx, member: discord.Member = None):
        if member is None:
            await ctx.send("You don't wanna eat yourself do you? lol")
        else:
            urls = ['https://media.tenor.com/images/333c4f19849451c7e1ddff454c9f9372/tenor.gif',
            'https://media.tenor.com/images/12aaaf60c46d563e3f8f2609f1df3c53/tenor.gif',
            'https://media1.tenor.com/images/dc499a9859fab7fee5a23aebfc646dbf/tenor.gif?itemid=11833453',
            'https://media.tenor.com/images/e5c65ea4d878d4165e682d7b984ab48b/tenor.gif',
            'https://media.tenor.com/images/8260bc43f1522aa93616ff5a4389f139/tenor.gif',
            'https://media.tenor.com/images/f9bba4a32a2f9bde7faa8c334aeaa4e5/tenor.gif']
            color_main = color[random.randint(0,len(color)-1)]
            embed = discord.Embed(title=(f'__***{ctx.author.name}***__ just nommed __***{member.name}***__') ,color=color_main)
            embed.set_image(url=urls[random.randint(0, len(urls)-1)])
            await ctx.send(embed=embed)

    @commands.command()
    async def pat(self, ctx, member: discord.Member = None):
        if member is None:
            await ctx.send("You don't wanna pat yourself do you? lol")
        else:
            urls = ['https://media.tenor.com/images/0203a7bdba3302f6d8a473ba461e1581/tenor.gif',
            'https://media.tenor.com/images/1da6bb86ef23dc4dff5051209843a296/tenor.gif',
            'https://media1.tenor.com/images/f79a9ec48bde0e592e55447b17ecfbad/tenor.gif?itemid=8053566',
            'https://media1.tenor.com/images/f41b3974036070fd1c498acf17a3a42e/tenor.gif?itemid=14751753',
            'https://media1.tenor.com/images/5466adf348239fba04c838639525c28a/tenor.gif?itemid=13284057',
            'https://media.tenor.com/images/0be5d465674b432bcf0bae0056f5621f/tenor.gif']
            color_main = color[random.randint(0,len(color)-1)]
            embed = discord.Embed(title=(f'__***{ctx.author.name}***__ just patted __***{member.name}***__') ,color=color_main)
            embed.set_image(url=urls[random.randint(0, len(urls)-1)])
            await ctx.send(embed=embed)

    @commands.command()
    async def dance(self, ctx, member: discord.Member=None):
        if member is None:
            urls = ['https://media3.giphy.com/media/6fScAIQR0P0xW/giphy.gif?cid=ecf05e47tg1vl88unml2kr0tg3sn01482oa1jqstgs7d028u&rid=giphy.gif',
            'https://i.imgur.com/wstXmJw.gif',
            'https://64.media.tumblr.com/9c7b6dec09a2e5cebb5cb5fa1e3c1f2f/tumblr_npk6npowW21qicfexo1_540.gifv']
            color_main = color[random.randint(0,len(color)-1)]
            embed = discord.Embed(title=(f'__***{ctx.author.name}***__ is dancing.') ,color=color_main)
            embed.set_image(url=urls[random.randint(0, len(urls)-1)])
            await ctx.send(embed=embed)
        else:
            urls = ['https://media1.giphy.com/media/gCy8PslyGfBu0/giphy.gif?cid=ecf05e47xpjyr0upvq7tex2zj2hwp90md5g7hrn9bsj78dsv&rid=giphy.gif',
            'https://media4.giphy.com/media/daBzBXPM1bSdpEW6MV/giphy.gif?cid=ecf05e47xpjyr0upvq7tex2zj2hwp90md5g7hrn9bsj78dsv&rid=giphy.gif',
            'https://media0.giphy.com/media/kXfImJBeF6S7m/giphy.gif?cid=ecf05e474mru95iml5dnq7vydfkcdd0kktcbl7zkjq45hgwt&rid=giphy.gif',
            'https://media3.giphy.com/media/PGp3hlI74uVxK/giphy.gif?cid=ecf05e47xpjyr0upvq7tex2zj2hwp90md5g7hrn9bsj78dsv&rid=giphy.gif']
            # 'https://media.tenor.com/images/5b25354209f6de4b064f0833f5eca8ad/tenor.gif',
            # 'https://media.tenor.com/images/557bcc935fe237761da4963e3213bd2e/tenor.gif']
            color_main = color[random.randint(0,len(color)-1)]
            embed = discord.Embed(title=(f'__***{ctx.author.name}***__ is dancing with __***{member.name}***__') ,color=color_main)
            embed.set_image(url=urls[random.randint(0, len(urls)-1)])
            await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(emotes(bot))
