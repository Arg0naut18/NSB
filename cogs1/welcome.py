import discord
from discord.ext import commands
import random
color = [15158332, 3066993, 10181046, 3447003, 1752220, 15844367]

class welcome(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        color_main = color[random.randint(0, len(color)-1)]
        for channel in guild.text_channels:
            if channel.permissions_for(guild.me).send_messages:
                mssg = "Hello! I am __**NotSoBasic**__ bot!\nI am an under development bot who is being developed by Genos (GenosOP#6921). I hope your server will enjoy my presence!\nType `nsb help` for help regarding the usage of the bot.\n Thank You"
                embed = discord.Embed(title = "NotSoBasic Bot", description = mssg, color = color_main)
                embed.set_thumbnail(url = self.bot.avatar_url)
                await channel.send(embed = embed)
            break

    @commands.command()
    async def intro(self, ctx):
        msg = "Thanks for you're concern. So I am a \
    bot developed by Genos to do some fun tasks for you. Right now I can play 8ball, \
     show memes and many more stuffs. Actually give the dev some ideas if u have any. He'll try to \
    add em xd."
        color_main = color[random.randint(0,5)]
        embed = discord.Embed(title="Intro!", description=msg, color=color_main)
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(welcome(bot))
