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
        users[str(user.id)]["safe"] = 0
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
        json.dump(users, j, indent=4)
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
        json.dump(users,f, indent=4)
    await update_bank_data(user, cost*-1)
    return [True,"Successful", cost]

async def get_inventory(user):
    users = await get_account_data()
    try:
        inv = users[str(user.id)]["bag"]
    except:
        inv = []
    return inv

async def is_in_inventory(user, item):
    inventory = await get_inventory(user)
    found = False
    for index in range(len(inventory)):
        if item == inventory[index]["item"]:
            found = True
    return found

async def open_shop():
    with open('./bank/shop.json', 'r') as f:
        mainshop = json.load(f)
    return mainshop

async def get_random_gift():
    shop = await open_shop()
    gift_item =  random.choice(shop)
    return [gift_item["display_name"], gift_item["name"], gift_item["price"]]

async def add_gift_to_inventory(user, amount=1):
    users = await get_account_data()
    gift_item = await get_random_gift()
    item_name = gift_item[1]
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
        json.dump(users,f, indent=4)
    return gift_item[0]

async def gift_this(user1, user2, item_name, amount):
    item_name = item_name.lower()
    amount = int(amount)
    inv = await get_inventory(user1)
    name_ = None
    for item in inv:
        name = item["item"].lower()
        if name == item_name:
            name_ = name
            no = item["amount"]
            break
    if name_ == None or amount>no:
        return [False, 1]
    if user1==user2:
        return [False, 2]
    users = await get_account_data()
    try:
        index=0
        t=None
        for thing in users[str(user2.id)]["bag"]:
            n=thing["item"]
            if n==item_name:
                old_amt = thing["amount"]
                new_amt = old_amt + amount
                users[str(user2.id)]["bag"][index]["amount"] = new_amt
                t=1
                break
            index+=1
        if t==None:
            obj={"item":item_name, "amount": amount}
            users[str(user2.id)]["bag"].append(obj)
    except Exception as e:
        obj = {"item": item_name, "amount": amount}
        users[str(user2.id)]["bag"]=[obj]
    for thing in inv:
        n=thing["item"]
        if n==item_name:
            old_amt = thing["amount"]
            new_amt = old_amt - amount
            if new_amt==0:
                del thing
                break
            else:
                thing["amount"] = new_amt
                print(thing["amount"])
                break    
    with open(r'./bank/bank.json', 'w') as f:
        json.dump(users,f, indent=4)
    return [True,"Successful"]

#async def update_inventory(user, item, amount):
#    users = await get_account_data()
#    for i in range(len(users[str(user.id)]["bag"])):
#        if item == users[str(user.id)]["bag"][i]["item"]:
#            if users[str(user.id)]["bag"][i]["amount"]+amount==0:
#                del users[str(user.id)]["bag"][i]
#                break
#            else:
#                users[str(user.id)]["bag"][i]["amount"]+=amount
#                break
#    with open(r'./bank/bank.json','w') as f:
#        json.dump(users, f, indent=4)

async def update_inventory(user, item, amount):
    users = await get_account_data()
    try:
        t=None
        for thing in users[str(user.id)]["bag"]:
            n=thing["item"]
            if n==item:
                old_amt = thing["amount"]
                new_amt = old_amt + amount
                thing["amount"] = new_amt
                t=1
                break
        if t==None:
            obj={"item":item, "amount": amount}
            users[str(user.id)]["bag"].append(obj)
    except Exception as e:
        print(e)
        obj = {"item": item, "amount": amount}
        users[str(user.id)]["bag"]=[obj]
    for i in range(len(users[str(user.id)]["bag"])):
        if item == users[str(user.id)]["bag"][i]["item"]:
            if users[str(user.id)]["bag"][i]["amount"]==0:
                del users[str(user.id)]["bag"][i]
                break
    with open(r'./bank/bank.json','w') as f:
        json.dump(users, f, indent=4)

async def get_tries(user):
    with open(r'./bank/fishingtries.json', 'r') as f:
        users = json.load(f)
    if str(user.id) in users:
        return False
    else:
        users[str(user.id)] = 0
    with open(r'./bank/fishingtries.json', 'w') as f:
        json.dump(users, f, indent=4)
    return True

async def start_log_transaction(user):
    with open(r'./bank/transactions.json', 'r') as f:
        users = json.load(f)
    if str(user.id) in users:
        return False
    else:
        users[str(user.id)] = []
    with open(r'./bank/transactions.json', 'w') as f:
        json.dump(users, f, indent=4)
    return True

async def get_transactions():
    with open(r'./bank/transactions.json', 'r') as f:
        transactions = json.load(f)
    return transactions

async def log_transaction(user, amount, string):
    await start_log_transaction(user)
    trans = await get_transactions()
    trans[str(user.id)].append({"amount":amount, "description": string})
    with open(r'./bank/transactions.json', 'w') as f:
        json.dump(trans, f, indent=4)

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
            await log_transaction(user, 5000, "For voting NSB.")
     
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
        if users[str(member.id)]["safe"] == 1:
            emb.set_footer(text=f"Invoked by: {ctx.author.name} | This user has a 🔒 on!", icon_url=ctx.author.avatar_url)
        else:
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
            await log_transaction(ctx.author, money, "From begging.")
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
            await log_transaction(ctx.author, amount, f"Deposited to bank.")
        elif bal[1]+amount >= maxbank and bal[1]<maxbank:
            updated_amount = maxbank - bal[1]
            await update_bank_data(ctx.author, updated_amount, "bank")
            await update_bank_data(ctx.author, -1*updated_amount)
            await ctx.send(f"You just deposited <:ncoin:857167494585909279>{updated_amount}!")
            await log_transaction(ctx.author, amount, f"Deposited to bank.")
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
        amount = int(amount)
        if int(amount)>bal[1]:
            await ctx.send("You don't have enough Ncoin.")
            return
        if int(amount)<0:
            await ctx.send("The amount can't be negative.")
            return
        await update_bank_data(ctx.author, int(amount))
        await update_bank_data(ctx.author, -1*int(amount), "bank")
        await ctx.send(f"You just withdrew <:ncoin:857167494585909279>{amount}!")
        await log_transaction(ctx.author, amount, f"Withdrew from bank.")

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
        amount = int(amount)
        if int(amount)>bal[0]:
            await ctx.send("You don't have enough Ncoin.")
            return
        if int(amount)<0:
            await ctx.send("The amount can't be negative.")
            return
        await update_bank_data(member, int(amount))
        await update_bank_data(ctx.author, -1*int(amount))
        await ctx.send(f"You just gave <:ncoin:857167494585909279>{amount} to {member.mention}! What a generous lad.")
        await log_transaction(ctx.author, amount, f"Gave to {member.display_name}.")
        await log_transaction(member, amount, f"Received from {ctx.author.display_name}")
    
    @commands.command()
    @commands.cooldown(1, 60, commands.BucketType.user)
    async def rob(self, ctx, member: discord.Member=None):
        if member is None:
            await ctx.send("You need to mention whom you wanna give the Ncoin to.")
            return
        await open_account(ctx.author)
        await open_account(member)
        users = await get_account_data()
        bal = await update_bank_data(ctx.author)
        membal = await update_bank_data(member)
        if bal[0]<50:
            await ctx.send("You need to have <:ncoin:857167494585909279>50 in your wallet to rob.")
            return
        if membal[0]<100:
            await ctx.send("It's not worth it man.")
            return
        chance = random.randrange(0,2)
        if chance==1 and users[str(member.id)]["safe"]!=1:
            amount = random.randrange(0, membal[0])
            await update_bank_data(member, -1*int(amount))
            await update_bank_data(ctx.author, int(amount))
            await ctx.send(f"You just robbed <:ncoin:857167494585909279>{amount} from {member.mention}! Poor lad.")
        elif users[str(member.id)]["safe"]==1:
            users[str(member.id)]["safe"] = 0
            await ctx.send(f"You tried to rob {member.display_name} but they had a padlock on. So the robbery failed. Better luck next time.")
            with open(r'./bank/bank.json', 'w') as f:
                json.dump(users, f, indent=4)
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
            await update_bank_data(ctx.author, money)
            await ctx.send(f"Great job {ctx.author.mention}! Your boss just gave you <:ncoin:857167494585909279>`{money}`! Congrats <a:partygif:855108791532388422>!")
            await log_transaction(ctx.author, money, f"Received from your boss.")
        else:
            await ctx.send(f"Ooh man! I expected you to do this simple job. Well atleast better luck next time.<:aqua_thumbsup:856058717119447040>")
            
    @commands.command()
    async def vote(self, ctx):
        vembed = discord.Embed(title="Thank you for choosing to vote for NSB.", description="You can vote the bot in the three mentioned websites and get <:ncoin:857167494585909279>5000 per vote instantly in your NSB wallet.", color=0x00FF00)
        vembed.add_field(name="<a:topggshrink:856942112670875718>",value=f"[Top.gg](https://top.gg/bot/743741872039657492/vote)", inline=False)
        vembed.add_field(name="<a:bfdspin:856942081679687721>",value=f"[Bots For Discord](https://botsfordiscord.com/bot/743741872039657492/vote)", inline=False)
        vembed.add_field(name="<:dbl:856926134549217330>",value=f"[Discord Bot List](https://discordbotlist.com/bots/notsobasic/upvote)", inline=False)
        vembed.set_footer(text=f"Invoked by {ctx.author} | Rewards for Discord bot list is currently unavailable.", icon_url=ctx.author.avatar_url)
        await ctx.reply(embed=vembed)        

    @commands.command()
    async def shop(self, ctx):
        mainshop = await open_shop()
        shopembed = discord.Embed(title="NSB Shop!", color=0x00FF00)
        i=1
        for item in mainshop:
            name = item["display_name"]
            price = item["price"]
            description = item["description"]
            id = item["name"]
            shopembed.add_field(name=f"{i}) {name}", value=f"Price: <:ncoin:857167494585909279>{price}\nDescription: {description}\nID: {id}", inline=False)
            i+=1
        shopembed.set_footer(text=f"Pro Tip: You can interact with the items in the shop using it's ID rather than it's Name.")
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
        await log_transaction(ctx.author, res[2], f"Bought {amount} {item}(s)")

    @commands.command(aliases=["inv"])
    async def inventory(self, ctx, user: discord.Member=None):
        user = ctx.author if not user else user
        await open_account(user)
        inv = await get_inventory(user)
        i=1
        msg = ''
        for item in inv: 
            name = item["item"].title()
            amount = item["amount"]
            msg += f"\n{i}) `{name}` | `{amount}`\n"
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
            await ctx.send(f'You just used {amount} bank note(s). Now your bank balance has increased from `{old_maxbank}` to `{users[str(ctx.author.id)]["maxbank"]}` <a:partygif:855108791532388422>')
        if found==1 and item=="padlock":
            users[str(ctx.author.id)]["safe"] = 1
            await ctx.send(f"You just applied a padlock :lock:. Now you're safe from one robbery.")    
        if found==1:    
            with open(r'./bank/bank.json','w') as f:
                json.dump(users, f, indent=4)
        else:
            await ctx.send("You don't own this item.'")
            return

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def fish(self, ctx):
        users = await get_account_data()
        user = ctx.author
        await get_tries(ctx.author)
        with open(f"./bank/fishingtries.json") as t:
            tries = json.load(t)
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
            money = random.randrange(20, 151)
            chance = random.randrange(0,20)
            correct=[0,2,4,5,8,6,9,13,15,18,10]
            spl = [7,17]
            bad = [1]
            if money != 0 and chance in correct:
                await update_bank_data(ctx.author, money)
                await ctx.send(f"Found a fish ! You sold it for <:ncoin:857167494585909279>`{money}` <a:partygif:855108791532388422>.")
                tries[str(user.id)]+=1
                with open(r'./bank/fishingtries.json','w') as f:
                    json.dump(tries, f, indent=4)
                return
            elif money != 0 and chance in spl:
                await update_bank_data(ctx.author, money)
                gift = await add_gift_to_inventory(user)
                await ctx.send(f"Found a fish ! You sold it for <:ncoin:857167494585909279>`{money}`.\nDamn you are lucky you also found `{gift}`! <a:partygif:855108791532388422>.")
                tries[str(user.id)]+=1
                with open(r'./bank/fishingtries.json','w') as f:
                    json.dump(tries, f, indent=4)
                return
            elif money != 0 and chance in bad and tries[str(user.id)]>=20:
                await ctx.send("You gave a hard jerk and the fishing rod broke <a:lmao:859292704650952704>. Anyway it was getting rusty. Time to buy another one. <:aqua_thumbsup:856058717119447040>")
                await update_inventory(ctx.author, "fishingrod", -1)
                tries[str(user.id)]=0
                with open(r'./bank/fishingtries.json','w') as f:
                    json.dump(tries, f, indent=4)
                return
            else:
                await ctx.send("You couldn't catch a fish. Try again later. <:aqua_thumbsup:856058717119447040>")
                tries[str(user.id)]+=1
                with open(r'./bank/fishingtries.json','w') as f:
                    json.dump(tries, f, indent=4)
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
            money = random.randrange(30, 151)
            chance = random.randrange(0,5)
            if money != 0 and chance==0 or chance==2 or chance== 4:
                await update_bank_data(ctx.author, money)
                await ctx.send(f"Found a skunk! You sold it for <:ncoin:857167494585909279>`{money}` <a:partygif:855108791532388422>.")
                return
            else:
                await ctx.send("You couldn't find a hunt. Try again later. <:aqua_thumbsup:856058717119447040>")
                return
        else:
            await ctx.send("You don't own a hunting gun to begin with!")

    @commands.command()
    async def gift(self, ctx, member: discord.Member=None, item=None, amount=1):
        users = await get_account_data()
        if member is None:
            await ctx.send("You need to mention who you wanna gift lol.")
            return
        if item is None:
            await ctx.send("You need to specify what you wanna gift lol.")
            return
        res = await gift_this(ctx.author, member, item, amount)
        if not res[0]:
            if res[1] == 1:
                await ctx.send(f"You don't have {amount} {item}(s) in your inventory!")
                return
            if res[1] == 2:
                await ctx.send(f"Bruh did u really think u can gift yourself stuff? LMAO")
                return
        #await update_inventory(member, item, amount)
        await ctx.send(f"You just gifted `{amount}` `{item}` to {member.mention} <a:partygif:855108791532388422>. I admire your generosity.")
        await update_inventory(ctx.author, item, -amount) 
            
    @commands.command()
    async def sell(self, ctx, item=None, amount=1):
        if item is None:
            await ctx.send("You need to mention what you want to sell.")
            return
        inv = await get_inventory(ctx.author)
        shop = await open_shop()
        for items in shop:
            if items["name"]==item:
                price = items["price"]
        index=0
        found = 0
        for index in range(len(inv)):
            if item == inv[index]["item"]:
                if inv[index]["amount"]-amount==0:
                    del inv[index]
                    found=1
                    break
                else:
                    found=1
                    inv[index]["amount"]-=amount
                    break
            index+=1
        if found==1:
            cost = price*amount/2
            await update_bank_data(ctx.author, cost)
            await ctx.send(f"You just sold `{amount}``{item}(s)` and received `{cost}`")
            await log_transaction(ctx.author, cost, f"Sold {amount} {item}(s)")
        else:
            await ctx.send(f"You don't have {item} in your inventory.")

def setup(bot):
    bot.add_cog(economy(bot))