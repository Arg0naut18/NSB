import discord
from discord.ext import commands

class command_log(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        channel = self.bot.get_channel(859367933331374081)
        try:
            await channel.send(f"<a:wrong:859371475482705920> **{ctx.author.name}** just invoked `{ctx.command}` in **{ctx.guild.name}** which didn't work.\nError: {error}")
        except:
            await channel.send(f"<a:wrong:859371475482705920> Someone just invoked `{ctx.command}` which didn't work.\nError: {error}")
            
    @commands.Cog.listener()
    async def on_command_completion(self, ctx):
        channel = self.bot.get_channel(859367933331374081)
        try:
            await channel.send(f"<a:tick:859371473772347403> **{ctx.author.name}** just invoked `{ctx.command}` in **{ctx.guild.name}** which worked successfully.")
        except:
            await channel.send(f"<a:tick:859371473772347403> Someone just invoked `{ctx.command}` which worked successfully.")

async def setup(bot):
    await bot.add_cog(command_log(bot))