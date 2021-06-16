import discord
from discord import TextChannel
from discord.ext import commands
import asyncio
import random

emojilist = []
roledict = {}
msgid = 0
userid = 0

class atom(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def reactrole(self, ctx, channel: TextChannel = None):
        channel = ctx.channel if not channel else channel
        global userid
        userid = ctx.author.id
        lol = await ctx.reply("Please answer the following questions with in a minute each.")
        roleid=[]
        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel
        await lol.delete()
        msg = await ctx.send("Enter the category of the rolemenu")
        try:
            cat = await self.bot.wait_for('message', timeout=60, check=check)
        except asyncio.TimeoutError:
            resp = await ctx.send("You didn't respond in the given time. Please respond faster next time!")
            await asyncio.sleep(10)
            await resp.delete()
            await msg.delete()
            return
        else:
            category = cat.content
            await cat.delete()
        await msg.delete()
        msg = await ctx.send("Enter the number of roles:")
        try:
            x = await self.bot.wait_for('message', timeout=60, check=check)
        except asyncio.TimeoutError:
            resp = await ctx.send("You didn't respond in the given time. Please respond faster next time!")
            await asyncio.sleep(10)
            await resp.delete()
            await msg.delete()
            return
        n = int(x.content)
        await x.delete()
        await msg.delete()
        roles = []
        quer = await ctx.send("Mention the role one by one")
        for i in range(n):
            try:
                rep = await self.bot.wait_for('message', timeout=60, check=check)
            except asyncio.TimeoutError:
                resp = await ctx.send("You didn't respond in the given time. Please respond faster next time!")
                await quer.delete()
                await asyncio.sleep(10)
                await resp.delete()
                return
            else:
                roles.append(rep.content)
                await rep.delete()
                try:
                    roleid.append(int(roles[i][3:-1]))
                except Exception as e:
                    print(e)
                    resp = await ctx.send("You didn't mention the role properly.")
                    await asyncio.sleep(10)
                    await resp.delete()
                    return
        await quer.delete()
        for i in range(n):
            roles[i] = discord.utils.get(ctx.guild.roles, id=roleid[i])

        emojis = await ctx.send("React to this message with emojis according to the roles within 30 seconds.")
        await asyncio.sleep(30)
        msgreact = await ctx.fetch_message(emojis.id)
        emoji = [i.emoji for i in msgreact.reactions]
        emojilist = emoji
        itera=0
        while(len(emoji)!=n and itera<3):
            emoji.clear()
            resp = await ctx.send("You couldn't react with all emojis. Giving you more 30 seconds.")
            await asyncio.sleep(30)
            msgreact = await channel.fetch_message(emojis.id)
            emoji = [i.emoji for i in msgreact.reactions]
            print(itera+1)
            itera+=1
            await resp.delete()
        if(itera==3):
            resp=await ctx.send("You couldn't react with all emojis even with extra time. Ending process")
            await asyncio.sleep(5)
            await resp.delete()
            await emojis.delete()
            return
        await emojis.delete()
        resp = await ctx.send("The rolemenu is done. Creating embed.")
        for i in range(n):
            try:
                roledict[emoji[i].id]=roles[i].id
            except:
                roledict[emoji[i]]=roles[i].id
        emb = discord.Embed(title="__**React Roles**__", description=f"**Category**: {category}".title(), color=random.randint(0x000000, 0xFFFFFF))
        for i in range(n):
            user = roles[i]
            emb.add_field(name="** **",value=f"{emoji[i]} **->** {user.mention}", inline=False)
        emb.add_field(name="** **", value="** **",inline=False)
        emb.set_footer(text=f"Invoked by: {ctx.author}", icon_url=ctx.author.avatar_url)
        rolemenu = await channel.send(embed=emb)
        await resp.delete()
        global msgid
        msgid = rolemenu.id
        for i in emoji:
            await rolemenu.add_reaction(i)
        await ctx.message.delete()

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        if reaction.message.id == msgid:
            if not user.bot:
                try:
                    try:
                        role = discord.utils.get(user.guild.roles, id=int(roledict[reaction.emoji.id]))
                    except:
                        role = discord.utils.get(user.guild.roles, id=int(roledict[str(reaction)]))
                    await user.add_roles(role)
                except Exception as e:
                    print("Error: "+str(e))
                    return

    @commands.Cog.listener()
    async def on_reaction_remove(self, reaction, user):
        if reaction.message.id == msgid:
            if not user.bot:
                try:
                    try:
                        role = discord.utils.get(user.guild.roles, id=int(roledict[reaction.emoji.id]))
                    except:
                        role = discord.utils.get(user.guild.roles, id=int(roledict[str(reaction)]))
                    await user.remove_roles(role)
                except Exception as e:
                    print("Error: "+str(e))
                    return

    @reactrole.error
    async def somerandomemojierror(self, ctx, error):
        if isinstance(error, commands.CommandInvokeError):
            respo = await ctx.send("`Please use emojis from this server preferably.`")
            await asyncio.sleep(10)
            await respo.delete()
            await ctx.channel.purge(limit=1)

def setup(bot):
    bot.add_cog(atom(bot))