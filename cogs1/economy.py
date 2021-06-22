import discord
from discord.ext import commands
import json
from datetime import date
import calendar
import random
import re

async def open_account(user):
    with open(r'./bank/bank.json', 'r') as f:
        users = json.load(f)
    if str(user.id) in users:
        return False
    else:
        users[str(user.id)] = {}
        users[str(user.id)]["wallet"] = 0
        users[str(user.id)]["bank"] = 0
    with open(r'./bank/bank.json', 'w') as f:
        json.dump(users, f, indent=4)
    return True

async def get_account_data():
    with open(r'./bank/bank.json', 'r') as j:
        users = json.load(j)
    return users

async def update_bank_data(user,amount=0,mode="wallet"):
    users = await get_account_data()
    users[str(user.id)][mode] += amount
    with open(r'./bank/bank.json', 'w') as j:
        json.dump(users, j)
    bal = [users[str(user.id)]["wallet"], users[str(user.id)]["bank"]]
    return bal

async def get_key_dict(val, dicti):
    for key,value in dicti.items():
        if val == value:
             return key
            
async def get_total_balance(user):
    users = await get_account_data()
    total = users[str(user.id)]["wallet"]+users[str(user.id)]["bank"]
    user_stats = [users[str(user.id)]["wallet"], users[str(user.id)]["bank"], total]
    return user_stats

class economy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_message(self,message):
        if message.channel.id == 856873592570773521:
            data = message.content.split(" ")
            user_info = re.sub("\D", "", data[6])
            try:
                user = self.bot.get_user(int(user_info)) or await self.bot.fetch_user(int(user_info))
            except Exception as e:
                print(e)
                return
            await open_account(user)
            await update_bank_data(user, 5000)
            msg = ("Thanks a lot for voting the bot <a:flashingheart:856875077023039528>! Here is :coin:5000 as a gift <a:partygif:855108791532388422>.")
            voteembed = discord.Embed(title="Thanks for voting!", description=msg, color=0x00FF00)
            await user.send(embed=voteembed)
     
    @commands.command(aliases = ['bal'])
    async def balance(self, ctx, member: discord.Member = None):
        member = ctx.author if not member else member
        await open_account(member)
        users = await get_account_data()
        wallet_money = users[str(member.id)]["wallet"]
        bank_money = users[str(member.id)]["bank"]
        emb = discord.Embed(title=f"{member.name}'s Balance", color=0x00FF00)
        emb.add_field(name=":money_with_wings: Wallet balance", value=f"`{wallet_money}`", inline=False)
        emb.add_field(name=":bank: Bank balance", value=f"`{bank_money}`", inline=False)
        emb.set_footer(text=f"Invoked by: {ctx.author.name}", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=emb)

    @commands.command()
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def beg(self, ctx):
        responses = ["You got shooed away! Better luck next time. <:sadcrypeace:855109649962369054>", "Mr. Selfish said he doesn't have time. Don't worry. Try again. <:aqua_thumbsup:856058717119447040>", "Mrs. Idon'tcare said she doesn't trust you coz you're poor! Yea she's a nitwit. Don't worry. Try again! <:aqua_thumbsup:856058717119447040>", "Mr. Selfish said he doesn't trust you coz you're poor! Yea he's a nitwit. Don't worry. Try again! <:aqua_thumbsup:856058717119447040>", "Mrs. Idon'tcare just considered you a ghost. Don't worry. Try again. <:aqua_thumbsup:856058717119447040>"]
        await open_account(ctx.author)
        users = await get_account_data()
        money = random.randrange(1, 151)
        chance = random.randrange(0,5)
        if money != 0 and chance==0 or chance==2 or chance== 4:
            users[str(ctx.author.id)]["wallet"] += money
            with open(r'./bank/bank.json', 'w') as f:
                json.dump(users, f, indent=4)
            await ctx.send(f"Someone just gave you :coin:`{money}`! Congrats <a:partygif:855108791532388422>!")
        else:
            await ctx.send(f"{random.choice(responses)}")

    @commands.command(aliases=['dep'])
    async def deposit(self, ctx, amount=None):
        if amount is None:
            await ctx.send("You need to mention the amount you wanna deposit.")
            return
        await open_account(ctx.author)
        bal = await update_bank_data(ctx.author)
        if amount == "all" or amount == "max":
            amount = bal[0]
        if int(amount)>bal[0]:
            await ctx.send("You don't have enough money.")
            return
        if int(amount)<0:
            await ctx.send("The amount can't be negative.")
            return
        await update_bank_data(ctx.author, int(amount), "bank")
        await update_bank_data(ctx.author, -1*int(amount))
        await ctx.send(f"You just deposited :coin:{amount}!")

    @commands.command(aliases=['with'])
    async def withdraw(self, ctx, amount=None):
        if amount is None:
            await ctx.send("You need to mention the amount you wanna deposit.")
            return
        await open_account(ctx.author)
        bal = await update_bank_data(ctx.author)
        if amount == "all" or amount == "max":
            amount = bal[1]
        if int(amount)>bal[1]:
            await ctx.send("You don't have enough money.")
            return
        if int(amount)<0:
            await ctx.send("The amount can't be negative.")
            return
        await update_bank_data(ctx.author, int(amount))
        await update_bank_data(ctx.author, -1*int(amount), "bank")
        await ctx.send(f"You just withdrew :coin:{amount}!")

    @commands.command()
    async def give(self, ctx, member: discord.Member=None, amount=None):
        if amount is None:
            await ctx.send("You need to mention the amount you wanna deposit.")
            return
        if member is None:
            await ctx.send("You need to mention whom you wanna give the money to.")
            return
        await open_account(ctx.author)
        await open_account(member)
        bal = await update_bank_data(ctx.author)
        if amount == "all" or amount == "max":
            amount = bal[0]
        if int(amount)>bal[0]:
            await ctx.send("You don't have enough money.")
            return
        if int(amount)<0:
            await ctx.send("The amount can't be negative.")
            return
        await update_bank_data(member, int(amount))
        await update_bank_data(ctx.author, -1*int(amount))
        await ctx.send(f"You just gave :coin:{amount} to {member.mention}! What a generous lad.")
    
    @commands.command()
    @commands.cooldown(1, 60, commands.BucketType.user)
    async def rob(self, ctx, member: discord.Member=None):
        if member is None:
            await ctx.send("You need to mention whom you wanna give the money to.")
            return
        await open_account(ctx.author)
        await open_account(member)
        bal = await update_bank_data(ctx.author)
        membal = await update_bank_data(member)
        if bal[0]<50:
            await ctx.send("You need to have :coin:50 in your wallet to rob.")
            return
        if membal[0]<100:
            await ctx.send("It's not worth it man.")
            return
        chance = random.randrange(0,2)
        if chance==1:
            amount = random.randrange(0, membal[0])
            await update_bank_data(member, -1*int(amount))
            await update_bank_data(ctx.author, int(amount))
            await ctx.send(f"You just robbed :coin:{amount} from {member.mention}! Poor lad.")
        else:
            await update_bank_data(ctx.author, -50)
            await ctx.send(f"Failed to rob {member.mention}. You lost :coin:50!")
            
    @commands.command(aliases=['ranks'])
    async def leaderboard(self, ctx):
        users = await get_account_data()
        total_list = {}
        for user in users:
            member = self.bot.get_user(int(user)) or await self.bot.fetch_user(int(user))
            if ctx.author.guild in member.mutual_guilds:
                total = await get_total_balance(member)
                total_list[f"{member.id}"]=total[2]
        sorteddict = dict(sorted(total_list.items(), key=lambda item: item[1], reverse=True))
        lb = discord.Embed(title=f"{ctx.author.guild.name}'s Leaderboard!", color=0x00FF00)
        for player_id in sorteddict.keys():
            member = await self.bot.fetch_user(int(player_id))
            lb.add_field(name=f"{member.display_name}".title(), value=f'Wallet: {users[str(player_id)]["wallet"]} | Bank: {users[str(player_id)]["bank"]} | Total: {users[str(player_id)]["wallet"]+users[str(player_id)]["bank"]}', inline=False)
        lb.set_footer(text=f"Invoked by: {ctx.author.display_name}", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=lb)
        
    @commands.command()
    @commands.cooldown(1, 3600, commands.BucketType.user)
    async def work(self, ctx):
        await open_account(ctx.author)
        users = await get_account_data()
        with open('./bank/questions.json') as qt:
            questions = json.load(qt)
        question_list = list(questions.items())
        query = random.choice(question_list)
        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel
        await ctx.send(query[0])
        answer = await self.bot.wait_for('message', timeout=60, check=check)
        is_it_correct = False
        if answer.content.lower().strip() == query[1]:
            is_it_correct=True
        if is_it_correct==True:
            money = 1000
            users[str(ctx.author.id)]["wallet"] += money
            with open(r'./bank/bank.json', 'w') as f:
                json.dump(users, f, indent=4)
            await ctx.send(f"Great job! Your boss just gave you :coin:`{money}`! Congrats <a:partygif:855108791532388422>!")
        else:
            await ctx.send(f"Ooh man! I expected you to do this simple job. Well atleast better luck next time.<:aqua_thumbsup:856058717119447040>")
            
    @commands.command()
    async def vote(self, ctx):
        vembed = discord.Embed(title="Thank you for choosing to vote for NSB.", description="You can vote the bot in the three mentioned websites and get :coin:5000 instantly in your NSB wallet.", color=0x00FF00)
        vembed.add_field(name="<:topgg:856926154510696488>",value=f"[Top.gg](https://top.gg/bot/743741872039657492)", inline=False)
        vembed.add_field(name="<:bfd:856926116655923200>",value=f"[Bots For Discord](https://botsfordiscord.com/bot/743741872039657492)", inline=False)
        vembed.add_field(name="<:dbl:856926134549217330>",value=f"[Discord Bot List](https://discordbotlist.com/bots/notsobasic)", inline=False)
        await ctx.reply(embed=vembed)        

def setup(bot):
    bot.add_cog(economy(bot))