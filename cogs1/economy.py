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
        users[str(user.id)]["maxbank"] = 15000
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

async def buy_this(user, item_name, amount):
    item_name = item_name.lower()
    with open('./bank/shop.json', 'r') as f:
            mainshop = json.load(f)
    name_ = None
    for item in mainshop:
        name = item["name"].lower()
        if name == item_name:
            name_ = name
            price = item["price"]
            break
    if name_ == None:
        return [False, 1]
    cost = price*amount
    users = await get_account_data()
    bal = await update_bank_data(user)
    if bal[0]<cost:
        return [False, 2]
    try:
        index=0
        t=None
        for thing in users[str(user.id)]["bag"]:
            n=thing["item"]
            if n==item_name:
                old_amt = thing["amount"]
                new_amt = old_amt + amount
                users[str(user.id)]["bag"][index]["amount"] = new_amt
                t=1
                break
            index+=1
        if t==None:
            obj={"item":item_name, "amount": amount}
            users[str(user.id)]["bag"].append(obj)
    except:
        obj = {"item": item_name, "amount": amount}
        users[str(user.id)]["bag"]=[obj]
    with open('./bank/bank.json', 'w') as f:
        json.dump(users,f)
    await update_bank_data(user, cost*-1)
    return [True,"Successful"]

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
            msg = ("Thanks a lot for voting the bot <a:flashingheart:856875077023039528>! Here is <:ncoin:857167494585909279>5000 as a gift <a:partygif:855108791532388422>.")
            voteembed = discord.Embed(title="Thanks for voting!", description=msg, color=0x00FF00)
            await user.send(embed=voteembed)
     
    @commands.command(aliases = ['bal'])
    async def balance(self, ctx, member: discord.Member = None):
        member = ctx.author if not member else member
        await open_account(member)
        users = await get_account_data()
        wallet_money = users[str(member.id)]["wallet"]
        bank_money = users[str(member.id)]["bank"]
        maxbank = users[str(member.id)]["maxbank"]
        emb = discord.Embed(title=f"{member.name}'s Balance", color=0x00FF00)
        emb.add_field(name=":money_with_wings: Wallet balance", value=f"`{wallet_money}`", inline=False)
        emb.add_field(name=":bank: Bank balance", value=f"`{bank_money}/{maxbank}`", inline=False)
        emb.set_footer(text=f"Invoked by: {ctx.author.name}", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=emb)

    @commands.command()
    @commands.cooldown(1, 15, commands.BucketType.user)
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
            await ctx.send(f"Someone just gave you <:ncoin:857167494585909279>`{money}`! Congrats <a:partygif:855108791532388422>!")
        else:
            await ctx.send(f"{random.choice(responses)}")

    @commands.command(aliases=['dep'])
    async def deposit(self, ctx, amount=None):
        if amount is None:
            await ctx.send("You need to mention the amount you wanna deposit.")
            return
        await open_account(ctx.author)
        users = await get_account_data()
        bal = await update_bank_data(ctx.author)
        maxbank = int(users[str(ctx.author.id)]["maxbank"])
        if amount == "all" or amount == "max":
            amount = bal[0]
        amount = int(amount)
        if int(amount)>bal[0]:
            await ctx.send("You don't have enough Ncoin.")
            return
        if int(amount)<0:
            await ctx.send("The amount can't be negative.")
            return
        if bal[1]+amount<maxbank:
            await update_bank_data(ctx.author, int(amount), "bank")
            await update_bank_data(ctx.author, -1*int(amount))
            await ctx.send(f"You just deposited <:ncoin:857167494585909279>{amount}!")
        elif bal[1]+amount >= maxbank and bal[1]<maxbank:
            updated_amount = maxbank - bal[1]
            await update_bank_data(ctx.author, updated_amount, "bank")
            await update_bank_data(ctx.author, -1*updated_amount)
            await ctx.send(f"You just deposited <:ncoin:857167494585909279>{updated_amount}!")
        else:
            await ctx.send("Your bank is full. Use Bank note to get more bank storage.")

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
            await ctx.send("You don't have enough Ncoin.")
            return
        if int(amount)<0:
            await ctx.send("The amount can't be negative.")
            return
        await update_bank_data(ctx.author, int(amount))
        await update_bank_data(ctx.author, -1*int(amount), "bank")
        await ctx.send(f"You just withdrew <:ncoin:857167494585909279>{amount}!")

    @commands.command()
    async def give(self, ctx, member: discord.Member=None, amount=None):
        if amount is None:
            await ctx.send("You need to mention the amount you wanna deposit.")
            return
        if member is None:
            await ctx.send("You need to mention whom you wanna give the Ncoin to.")
            return
        await open_account(ctx.author)
        await open_account(member)
        bal = await update_bank_data(ctx.author)
        if amount == "all" or amount == "max":
            amount = bal[0]
        if int(amount)>bal[0]:
            await ctx.send("You don't have enough Ncoin.")
            return
        if int(amount)<0:
            await ctx.send("The amount can't be negative.")
            return
        await update_bank_data(member, int(amount))
        await update_bank_data(ctx.author, -1*int(amount))
        await ctx.send(f"You just gave <:ncoin:857167494585909279>{amount} to {member.mention}! What a generous lad.")
    
    @commands.command()
    @commands.cooldown(1, 60, commands.BucketType.user)
    async def rob(self, ctx, member: discord.Member=None):
        if member is None:
            await ctx.send("You need to mention whom you wanna give the Ncoin to.")
            return
        await open_account(ctx.author)
        await open_account(member)
        bal = await update_bank_data(ctx.author)
        membal = await update_bank_data(member)
        if bal[0]<50:
            await ctx.send("You need to have <:ncoin:857167494585909279>50 in your wallet to rob.")
            return
        if membal[0]<100:
            await ctx.send("It's not worth it man.")
            return
        chance = random.randrange(0,2)
        if chance==1:
            amount = random.randrange(0, membal[0])
            await update_bank_data(member, -1*int(amount))
            await update_bank_data(ctx.author, int(amount))
            await ctx.send(f"You just robbed <:ncoin:857167494585909279>{amount} from {member.mention}! Poor lad.")
        else:
            await update_bank_data(ctx.author, -50)
            await ctx.send(f"Failed to rob {member.mention}. You lost <:ncoin:857167494585909279>50!")
            
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
            await ctx.send(f"Great job! Your boss just gave you <:ncoin:857167494585909279>`{money}`! Congrats <a:partygif:855108791532388422>!")
        else:
            await ctx.send(f"Ooh man! I expected you to do this simple job. Well atleast better luck next time.<:aqua_thumbsup:856058717119447040>")
            
    @commands.command()
    async def vote(self, ctx):
        vembed = discord.Embed(title="Thank you for choosing to vote for NSB.", description="You can vote the bot in the three mentioned websites and get <:ncoin:857167494585909279>5000 instantly in your NSB wallet.", color=0x00FF00)
        vembed.add_field(name="<a:topggshrink:856942112670875718>",value=f"[Top.gg](https://top.gg/bot/743741872039657492/vote)", inline=False)
        vembed.add_field(name="<a:bfdspin:856942081679687721>",value=f"[Bots For Discord](https://botsfordiscord.com/bot/743741872039657492/vote)", inline=False)
        vembed.add_field(name="<:dbl:856926134549217330>",value=f"[Discord Bot List](https://discordbotlist.com/bots/notsobasic/upvote)", inline=False)
        vembed.set_footer(text=f"Invoked by {ctx.author} | Rewards for Discord bot list is currently unavailable.", icon_url=ctx.author.avatar_url)
        await ctx.reply(embed=vembed)        

    @commands.command()
    async def shop(self, ctx):
        with open('./bank/shop.json', 'r') as f:
            mainshop = json.load(f)
        shopembed = discord.Embed(title="NSB Shop!", color=0x00FF00)
        i=1
        for item in mainshop:
            name = item["display_name"]
            price = item["price"]
            description = item["description"]
            id = item["name"]
            shopembed.add_field(name=f"{i}) {name}", value=f"Price: <:ncoin:857167494585909279>{price}\nDescription: {description}\nID: {id}", inline=False)
            i+=1
        await ctx.send(embed=shopembed)

    @commands.command()
    async def buy(self, ctx, item, amount=1):
        res = await buy_this(ctx.author, item, amount)
        if not res[0]:
            if res[1] == 1:
                await ctx.send("This item isn't available on the shop yet! Please type the item ID properly.")
                return
            if res[1]== 2:
                await ctx.send(f"You don't have enough Ncoin in your wallet to buy {amount} {item}(s)")
                return
        await ctx.send(f"Added `{amount}` `{item}` to your inventory <a:partygif:855108791532388422>.")

    @commands.command(aliases=["inv"])
    async def inventory(self, ctx, user: discord.Member=None):
        user = ctx.author if not user else user
        await open_account(user)
        users = await get_account_data()
        try:
            inv = users[str(user.id)]["bag"]
        except:
            inv = []
        i=1
        msg = ''
        for item in inv: 
            name = item["item"].title()
            amount = item["amount"]
            msg += f"{i}) `{name}` | `{amount}`\n"
            i+=1
        if msg=='':
            msg = "You don't own anything yet lmao!"    
        invembed = discord.Embed(title=f"{user.display_name}'s Inventory", description=msg, color=0x00FF00)
        await ctx.send(embed=invembed)
        
    @commands.command()
    async def use(self, ctx, item=None, amount=1):
        if item is None:
            await ctx.send("You need to mention the item you want to use.")
            return
        user = ctx.author
        users = await get_account_data()
        try:
            inv = users[str(user.id)]["bag"]
        except:
            await ctx.send("You don't own anything to use.")
            return
        found = 0
        for index in range(len(inv)):
            if item == inv[index]["item"]:
                if inv[index]["amount"]-amount==0:
                    del inv[index]
                    found = 1
                    break
                else:
                    inv[index]["amount"]-=amount
                    found = 1
                    break
        if found==1 and item=="banknote":
            old_maxbank = users[str(ctx.author.id)]["maxbank"]
            users[str(ctx.author.id)]["maxbank"]+=amount*10000
            await ctx.send(f'You just used a bank note. Now your bank balance has increased from `{old_maxbank}` to `{users[str(ctx.author.id)]["maxbank"]}` <a:partygif:855108791532388422>')
        if found==1:    
            with open(r'./bank/bank.json','w') as f:
                json.dump(users, f)
        else:
            await ctx.send("You don't own this item.'")
            return

    @commands.command()
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def fish(elf, ctx):
        users = await get_account_data()
        user = ctx.author
        try:
            inv = users[str(user.id)]["bag"]
        except:
            await ctx.send("You don't own anything to use.")
            return
        found = 0
        for index in range(len(inv)):
            if "fishingrod" == inv[index]["item"]:
                found=1
                break
        if found==1:
            money = random.randrange(1, 151)
            chance = random.randrange(0,5)
            if money != 0 and chance==0 or chance==2 or chance== 4:
                await update_bank_data(ctx.author, money)
                await ctx.send(f"Found a fish ! You sold it for <:ncoin:857167494585909279>`{money}` <a:partygif:855108791532388422>.")
                return
            else:
                await ctx.send("You couldn't catch a fish. Try again later. <:aqua_thumbsup:856058717119447040>")
                return
        else:
            await ctx.send("You don't own a fishing rod to begin with!")
        
    @commands.command()
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def hunt(elf, ctx):
        users = await get_account_data()
        user = ctx.author
        try:
            inv = users[str(user.id)]["bag"]
        except:
            await ctx.send("You don't own anything to use.")
            return
        found = 0
        for index in range(len(inv)):
            if "huntinggun" == inv[index]["item"]:
                found=1
                break
        if found==1:
            money = random.randrange(1, 151)
            chance = random.randrange(0,5)
            if money != 0 and chance==0 or chance==2 or chance== 4:
                await update_bank_data(ctx.author, money)
                await ctx.send(f"Found a boar! You sold it for <:ncoin:857167494585909279>`{money}` <a:partygif:855108791532388422>.")
                return
            else:
                await ctx.send("You couldn't find a hunt. Try again later. <:aqua_thumbsup:856058717119447040>")
                return
        else:
            await ctx.send("You don't own a hunting gun to begin with!")

def setup(bot):
    bot.add_cog(economy(bot))