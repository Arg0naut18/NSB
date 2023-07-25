import discord
from discord.ext import commands
import random

class fun(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot: commands.Bot = bot

    @commands.hybrid_command(name='8ball', with_app_command=True)
    async def _8ball(self, ctx: commands.Context, *, question: str):
        responses = ['It is certain.',
                     'It is decidedly so.',
                     'Without a doubt.',
                     'Yes – definitely.',
                     'You may rely on it.',
                     'As I see it, yes.',
                     'Most likely.',
                     'Outlook good.',
                     'Yes.',
                     'Signs point to yes.',
                     'Reply hazy, try again.',
                     'Ask again later.',
                     'Better not tell you now.',
                     'Cannot predict now.',
                     'Concentrate and ask again.',
                     "Don't count on it.",
                     'My reply is no.',
                     'My sources say no.',
                     'Outlook not so good.',
                     'Very doubtful.']
        await ctx.send(f'Question: {question}\nAnswer: {random.choice(responses)}', ephemeral=True)

    @commands.hybrid_command(name = "rolldice", with_app_command=True)
    async def rolldice(self, ctx:commands.Context):
        options = ['1', '2', '3', '4', '5', '6']
        await ctx.send(f'{random.choice(options)}', ephemeral=True)

async def setup(bot):
    await bot.add_cog(fun(bot))