import discord
from discord.ext import commands
import random

color = [15158332, 3066993, 10181046, 3447003, 1752220, 15844367]
mslist = ["Old Cypress", "cypress leaf", "Cracked tough hide", "ginko seedling", "Aluminium ore", "malachite", "kyanite", "flax leaf", "flax petal", "kenaf leaf", "grease", "beast horn", "rugged leather", "berries", "Matsutake Mushroom", "cave mushroom", "pumpkin", "ice", "honey"]
mslist = [estring.title() for estring in mslist]
umlist = ["Old Cypress", "cypress leaf", "Cracked tough hide", "ginko seedling", "Aluminium ore", "malachite", "kyanite", "flax leaf",
          "flax petal", "kenaf leaf", "grease", "beast horn", "rugged leather", "berries", "carrot"]
umlist = [estring.title() for estring in umlist]
wflist = ["twigs", "hardwood wine", "sapling", "iron ore", "flint", "cast iron drill bit", "plant root", "bone", "hide", "berries", "Mushroom", "Autumn Fall exclusive: Honewdew Melon"]
wflist = [estring.title() for estring in wflist]

srlist = ["Twigs", "hardwood vine",  "sapling", "iron ore", "flint", "iron drill", "plant root", "bone", "hide",  "berries", "mushroom", "rapeseed"]
srlist = [estring.title() for estring in srlist]
ahlist = ["Resin", " woodcore", "oak seedling", "Tin ore", "sulphure", "Alloy drill", "hemp steam", "hemp bast", "castor seed", "claw", "beast tendon", "berries", "straeberry", "honeydew melon"]
ahlist = [estring.title() for estring in ahlist]
bhlist = ["Resin", "woodcore", "oak seedling", "Tin ore", "sulphure,Alloy drill", "hemp steam", "hemp bast", "castor seed", "clow", "beast tendon", "berries", "straeberry", "honeydew melon"]
bhlist = [estring.title() for estring in bhlist]
aglist = ["Resin", "woodcore", "oak seedling", "Tin ore", "sulphure,Alloy drill", "hemp steam", "hemp bast", "castor seed", "clow", "beast tendon", "berries", "straeberry", "honeydew melon"]
aglist = [estring.title() for estring in aglist]
gwlist = ["White Birch", "Birch Bark", "Phosphorite Ore", "Apatite", "Urtica Leaf", "Urtica Stem", "Bone Spur", "Tentacle", "Berries", "Watermelon"]

mglist = ["White Birch", "Birch Bark", "Phosphorite Ore", "Apatite", "Urtica Leaf", "Urtica Stem", "Bone Spur", "Tentacle", "Berries", "Matsutake Mushroom"]

vsplist = ["White Birch", "Birch Bark", "Phosphorite Ore", "Apatite", "Urtica Leaf", "Urtica Stem", "Bone Spur", "Tentacle", "Berries", "Watermelon"]
cvlist = ["White Birch", "Birch Bark", "Phosphorite Ore", "Apatite", "Urtica Leaf", "Urtica Stem", "Bone Spur", "Tentacle", "Berries", "Carrot"]

rllist = ["White Birch", "Birch Bark", "Phosphorite Ore", "Apatite", "Urtica Leaf", "Urtica Stem", "Bone Spur", "Tentacle", "Berries", "Strawberry"]
desdlist = ["Elm Leaves", "Elm Bark", "Kamacite", "Pyrite", "Kendir", "Dogbane Stalk", "Beast Tail", "Scale", "Berries", "Strawberry"]

bwlist = ["Elm Leaves", "Elm Bark", "Kamacite", "Pyrite", "Kendir", "Dogbane Stalk", "Beast Tail", "Scale", "Berries", "Strawberry"]

sclist = ["Elm Leaves", "Elm Bark", "Kamacite", "Pyrite", "Kendir", "Dogbane Stalk", "Beast Tail", "Scale", "Berries", "Strawberry", "Watermelon"]

splist = ["Elm Leaves", "Elm Bark", "Kamacite", "Pyrite", "Kendir", "Dogbane Stalk", "Beast Tail", "Scale", "Berries", "Strawberry"]

swblist = ["Redwood", "Nanmu", "Cedar Leaves", "Gold Ore", "Quicksilver", "Rare Ore", "Nettle Leaf", "Hops", "Castor Bast", "Beast Hoof", "Beast Spine", "Berries", "Blueberry"]

lblist = ["Redwood", "Nanmu", "Cedar Leaves", "Gold Ore", "Quicksilver", "Rare Ore", "Nettle Leaf", "Hops", "Castor Bast", "Beast Hoof", "Beast Spine", "Berries", "Blueberry", "Cayenne Pepper", "Strawberry"]

malist = ["Old Oak", "Birch Root", "Silver Ore", "Pyragyrite", "Sisal Leaf", "Kenaf Bast", "Beast Blood", "Rugged Tail", "Berries", "Corn", "Carrot"]

lesplist = ["Old Oak", "Birch Root", "Silver Ore", "Pyragyrite", "Sisal Leaf", "Kenaf Bast", "Beast Blood", "Rugged Tail", "Berries", "Watermelon", "Matsutake Mushroom", "Coconut"]

twclist = ["Old Oak", "Birch Root", "Silver Ore", "Pyragyrite", "Sisal Leaf", "Kenaf Bast", "Beast Blood", "Rugged Tail", "Berries", "Watermelon"]
rwtlist = ["Old Oak", "Birch Root", "Silver Ore", "Pyragyrite", "Sisal Leaf", "Kenaf Bast", "Beast Blood", "Rugged Tail", "Berries", "Corn", "Carrot"]
santolist = ["Old Oak", "Birch Root", "Silver Ore", "Pyragyrite", "Sisal Leaf", "Kenaf Bast", "Beast Blood", "Rugged Tail", "Berries", "Strawberry", "Cayenne Pepper", "Sea Mushroom", "Coconut"]

rivalist = ["Boxwood", "Broadleaf", "Copper Ore", "Diamond Drill Bit", "Silicon", "Jute Leaf", "Jute Stem", "Beast Tooth", "Beast Fur", "Berries", "Watermelon"]
wolflist = ["Boxwood", "Broadleaf", "Copper Ore", "Diamond Drill Bit", "Silicon", "Jute Leaf", "Jute Stem", "Beast Tooth", "Beast Fur", "Berries", "Strawberry"]
bpalist = ["Boxwood", "Broadleaf", "Copper Ore", "Diamond Drill Bit", "Silicon", "Jute Leaf", "Jute Stem", "Beast Tooth", "Beast Fur", "Berries", "Strawberry"]
miskalist = ["Boxwood", "Broadleaf", "Copper Ore", "Diamond Drill Bit", "Silicon", "Jute Leaf", "Jute Stem", "Beast Tooth", "Beast Fur", "Berries", "Watermelon"]

ronalist = ["Camphor", "Camphor Leaf", "Volcanic Rock", "Bornite", "Bugbane", "Bugbane Stem", "Dorsal Fin", "Beast Antler", "Wood Ash", "Volcanic Ash", "Berries", "Morel"]
ptlist = ["Old Cypress", "Cypress Leaf", "Cracked Tough Hide", "Ginko Seedling", "Aluminum Ore", "Kyanite", "Malachite", "Flax Leaf", "Flax Petal", "Kenaf Leaf", "Grease", "Beast Horn", "Rugged Leather", "Berries", "Matsutake Mushroom", "Ice"]
fflist = ["Twig", "Hardwood Vine", "Sapling", "Iron Ore", "Flint", "Cast Iron Drill Bit", "Plant Root", "Bone", "Hide", "Berries", "Mushroom", "Rapeseed", "Honey"]

swamplist = ["Redwood", "Nanmu", "Cedar Leaves", "Gold Ore", "Quicksilver", "Rare Ore", "Nettle Leaf", "Hops", "Castor Bast", "Beast Hoof", "Beast Spine", "Berries", "Blueberry"]
mouthlist = ["Redwood", "Nanmu", "Cedar Leaves", "Gold Ore", "Quicksilver", "Rare Ore", "Nettle Leaf", "Hops", "Castor Bast", "Beast Hoof", "Beast Spine", "Berries", "Blueberry", "Cayenne Pepper"]
shlist = ["Old Cypress", "Cypress Leaf", "Cracked Tough Hide", "Ginko Seedling", "Aluminum Ore", "Kyanite", "Malachite", "Flax Leaf", "Flax Petal", "Kenaf Leaf", "Grease", "Beast Horn", "Rugged Leather", "Berries", "Matsutake Mushroom", "Ice"]

total = [{"Mount Snow":mslist}, {"Clear Sky Wheat field":wflist}, {"Snow Highlands":shlist}, {"Ultz Mine":umlist}, {"Summer Rain Highway":srlist}, {"Assyrian Hills": ahlist}, {"Blade Hunter Base": bhlist}, {"Assyrian Grassfields":aglist}, {"Gatey Woods":gwlist}, {"Mount Gray Bear":mglist}, {"Vina Snow Park":vsplist}, {"Christmas Village" : cvlist}, {"Red Water Lake":rllist}, {"Desolate Desert":desdlist}, {"Barren Wilds":bwlist}, {"Sand Castle":sclist}, {"Silent Plain":splist}, {"Swamp Border":swblist}, {"Lawrence Bay":lblist}, {"Mount Apparition": malist}, {"Lesins Port":lesplist}, {"Twin Ways City":twclist}, {"Redwood Town":rwtlist}, {"Santopany":santolist}, {"River Area": rivalist}, {"Wolf Hunting Field":wolflist}, {"Black Pearl Area":bpalist}, {"Miska Town":miskalist}, {"St. Rona":ronalist}, {"Polar Tjaele":ptlist}, {"Fall Forest":fflist}, {"Mouth Swamp":swamplist}, {"Mouth Town":mouthlist}]
class resources(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        # self.member = member

    @commands.command(aliases = ["ms", "msnow"])
    async def mountsnow(self, ctx):
        color_main = color[random.randint(0,len(color)-1)]
        embed = discord.Embed(title='__**Mount Snow**__' ,color=color_main)
        embed.add_field(name="Resource level", value="3", inline=False)
        embed.add_field(name="Recommended Combat level", value="26", inline=False)
        embed.add_field(name="Gold bars from Assistance quests", value="750", inline=False)
        embed.add_field(name="Resources",value="\n".join(mslist[:len(mslist)]), inline=False)
        embed.set_footer(text=f"Invoked by {ctx.author}", icon_url=ctx.author.avatar_url)
        await ctx.reply(embed=embed)

    @commands.command(aliases=["cswf", "wf"])
    async def wheatfield(self, ctx):
        color_main = color[random.randint(0, len(color)-1)]
        embed = discord.Embed(title='__**Clear Sky Wheat Field**__', color=color_main)
        embed.add_field(name="Resource level", value="1", inline=False)
        embed.add_field(name="Recommended Combat level", value="1", inline=False)
        embed.add_field(name="Gold bars from Assistance quests", value="700", inline=False)
        embed.add_field(name="Resources",
                        value="\n".join(wflist[:len(wflist)]), inline=False)
        embed.set_footer(text=f"Invoked by {ctx.author}", icon_url=ctx.author.avatar_url)
        await ctx.reply(embed=embed)

    @commands.command(aliases=["sh"])
    async def snowhighlands(self, ctx):
        color_main = color[random.randint(0, len(color)-1)]
        embed = discord.Embed(title='__**Snow Highlands**__', color=color_main)
        embed.add_field(name="Resource level", value="3", inline=False)
        embed.add_field(name="Recommended Combat level",
                        value="28", inline=False)
        embed.add_field(name="Gold bars from Assistance quests",
                        value="750", inline=False)
        embed.add_field(name="Resources", value="\n".join(
            shlist[:len(shlist)]), inline=False)
        embed.set_footer(
            text=f"Invoked by {ctx.author}", icon_url=ctx.author.avatar_url)
        await ctx.reply(embed=embed)

    @commands.command(aliases=["um"])
    async def ultzmine(self, ctx):
        color_main = color[random.randint(0, len(color)-1)]
        embed = discord.Embed(title='__**Ultz Mine**__', color=color_main)
        embed.add_field(name="Resource level", value="3", inline=False)
        embed.add_field(name="Recommended Combat level",
                        value="21", inline=False)
        embed.add_field(name="Gold bars from Assistance quests",
                        value="750", inline=False)
        embed.add_field(name="Resources", value="\n".join(
            umlist[:len(umlist)]), inline=False)
        embed.set_footer(
            text=f"Invoked by {ctx.author}", icon_url=ctx.author.avatar_url)
        await ctx.reply(embed=embed)

    @commands.command(aliases=["srh", "rh", "sr"])
    async def rainhighway(self, ctx):
        color_main = color[random.randint(0, len(color)-1)]
        embed = discord.Embed(title='__**Summer Rain Highway**__', color=color_main)
        embed.add_field(name="Resource level", value="2", inline=False)
        embed.add_field(name="Recommended Combat level",
                        value="6", inline=False)
        embed.add_field(name="Gold bars from Assistance quests",
                        value="700", inline=False)
        embed.add_field(name="Resources", value="\n".join(
            srlist[:len(srlist)]), inline=False)
        embed.set_footer(
            text=f"Invoked by {ctx.author}", icon_url=ctx.author.avatar_url)
        await ctx.reply(embed=embed)

    @commands.command(aliases=["ah"])
    async def assyrianhills(self, ctx):
        color_main = color[random.randint(0, len(color)-1)]
        embed = discord.Embed(title='__**Assyrian Hills**__', color=color_main)
        embed.add_field(name="Resource level", value="3", inline=False)
        embed.add_field(name="Recommended Combat level",
                        value="26", inline=False)
        embed.add_field(name="Gold bars from Assistance quests",
                        value="750", inline=False)
        embed.add_field(name="Resources", value="\n".join(
            ahlist[:len(ahlist)]), inline=False)
        embed.set_footer(
            text=f"Invoked by {ctx.author}", icon_url=ctx.author.avatar_url)
        await ctx.reply(embed=embed)
    
    @commands.command(aliases=["bh"])
    async def bladehunterbase(self, ctx):
        color_main = color[random.randint(0, len(color)-1)]
        embed = discord.Embed(title='__**Blade Hunter Base**__', color=color_main)
        embed.add_field(name="Resource level", value="2", inline=False)
        embed.add_field(name="Recommended Combat level",
                        value="13", inline=False)
        embed.add_field(name="Gold bars from Assistance quests",
                        value="700", inline=False)
        embed.add_field(name="Resources", value="\n".join(
            bhlist[:len(bhlist)]), inline=False)
        embed.set_footer(
            text=f"Invoked by {ctx.author}", icon_url=ctx.author.avatar_url)
        await ctx.reply(embed=embed)

    @commands.command(aliases=["ag"])
    async def assyriangrassfields(self, ctx):
        color_main = color[random.randint(0, len(color)-1)]
        embed = discord.Embed(title='__**Assyrian Grassfields**__', color=color_main)
        embed.add_field(name="Resource level", value="3", inline=False)
        embed.add_field(name="Recommended Combat level",
                        value="26", inline=False)
        embed.add_field(name="Gold bars from Assistance quests",
                        value="750", inline=False)
        embed.add_field(name="Resources", value="\n".join(
            aglist[:len(aglist)]), inline=False)
        embed.set_footer(
            text=f"Invoked by {ctx.author}", icon_url=ctx.author.avatar_url)
        await ctx.reply(embed=embed)

    @commands.command(aliases=["gw", "gatey"])
    async def gateywoods(self, ctx):
        color_main = color[random.randint(0, len(color)-1)]
        embed = discord.Embed(title='__**Gatey Woods**__', color=color_main)
        embed.add_field(name="Resource level", value="3", inline=False)
        embed.add_field(name="Recommended Combat level",
                        value="26", inline=False)
        embed.add_field(name="Gold bars from Assistance quests",
                        value="750", inline=False)
        embed.add_field(name="Resources", value="\n".join(
            gwlist[:len(gwlist)]), inline=False)
        embed.set_footer(
            text=f"Invoked by {ctx.author}", icon_url=ctx.author.avatar_url)
        await ctx.reply(embed=embed)

    @commands.command(aliases=["mg", "graybear"])
    async def mountgraybear(self, ctx):
        color_main = color[random.randint(0, len(color)-1)]
        embed = discord.Embed(title='__**Mount Gray Bear**__', color=color_main)
        embed.add_field(name="Resource level", value="9", inline=False)
        embed.add_field(name="Recommended Combat level",
                        value="93", inline=False)
        embed.add_field(name="Gold bars from Assistance quests",
                        value="800", inline=False)
        embed.add_field(name="Resources", value="\n".join(
            mglist[:len(mglist)]), inline=False)
        embed.set_footer(
            text=f"Invoked by {ctx.author}", icon_url=ctx.author.avatar_url)
        await ctx.reply(embed=embed)

    @commands.command(aliases=["vsp", "vina", "snowpark"])
    async def vinasnowpark(self, ctx):
        color_main = color[random.randint(0, len(color)-1)]
        embed = discord.Embed(title='__**Vina Snow Park**__', color=color_main)
        embed.add_field(name="Resource level", value="3", inline=False)
        embed.add_field(name="Recommended Combat level",
                        value="93", inline=False)
        embed.add_field(name="Gold bars from Assistance quests",
                        value="800", inline=False)
        embed.add_field(name="Resources", value="\n".join(
            vsplist[:len(vsplist)]), inline=False)
        embed.set_footer(
            text=f"Invoked by {ctx.author}", icon_url=ctx.author.avatar_url)
        await ctx.reply(embed=embed)

    @commands.command(aliases = ["cv", "christmas"])
    async def christmasvillage(self, ctx):
        color_main = color[random.randint(0,len(color)-1)]
        embed = discord.Embed(title='__**Christmas Village**__' ,color=color_main)
        embed.add_field(name="Resource level", value="3", inline=False)
        embed.add_field(name="Recommended Combat level", value="26", inline=False)
        embed.add_field(name="Gold bars from Assistance quests", value="750", inline=False)
        embed.add_field(name="Resources",value="\n".join(cvlist[:len(cvlist)]), inline=False)
        embed.set_footer(text=f"Invoked by {ctx.author}", icon_url=ctx.author.avatar_url)
        await ctx.reply(embed=embed)

    @commands.command(aliases=["rl", "redwater"])
    async def redwaterlake(self, ctx):
        color_main = color[random.randint(0, len(color)-1)]
        embed = discord.Embed(title='__**Redwater Lake**__', color=color_main)
        embed.add_field(name="Resource level", value="9", inline=False)
        embed.add_field(name="Recommended Combat level",
                        value="91", inline=False)
        embed.add_field(name="Gold bars from Assistance quests",
                        value="800", inline=False)
        embed.add_field(name="Resources", value="\n".join(
            rllist[:len(rllist)]), inline=False)
        embed.set_footer(
            text=f"Invoked by {ctx.author}", icon_url=ctx.author.avatar_url)
        await ctx.reply(embed=embed)

    @commands.command(aliases=["desd", "desolate", "desert"])
    async def desolatedesert(self, ctx):
        color_main = color[random.randint(0, len(color)-1)]
        embed = discord.Embed(title='__**Desolate Desert**__', color=color_main)
        embed.add_field(name="Resource level", value="7", inline=False)
        embed.add_field(name="Recommended Combat level",
                        value="71", inline=False)
        embed.add_field(name="Gold bars from Assistance quests",
                        value="800", inline=False)
        embed.add_field(name="Resources", value="\n".join(
            desdlist[:len(desdlist)]), inline=False)
        embed.set_footer(
            text=f"Invoked by {ctx.author}", icon_url=ctx.author.avatar_url)
        await ctx.reply(embed=embed)

    @commands.command(aliases=["bw"])
    async def barrenwilds(self, ctx):
        color_main = color[random.randint(0, len(color)-1)]
        embed = discord.Embed(title='__**Barren Wilds**__', color=color_main)
        embed.add_field(name="Resource level", value="7", inline=False)
        embed.add_field(name="Recommended Combat level",
                        value="73", inline=False)
        embed.add_field(name="Gold bars from Assistance quests",
                        value="800", inline=False)
        embed.add_field(name="Resources", value="\n".join(
            bwlist[:len(bwlist)]), inline=False)
        embed.set_footer(
            text=f"Invoked by {ctx.author}", icon_url=ctx.author.avatar_url)
        await ctx.reply(embed=embed)

    @commands.command(aliases = ["sc"])
    async def sandcastle(self, ctx):
        color_main = color[random.randint(0,len(color)-1)]
        embed = discord.Embed(title='__**Sand Castle**__' ,color=color_main)
        embed.add_field(name="Resource level", value="7", inline=False)
        embed.add_field(name="Recommended Combat level", value="76", inline=False)
        embed.add_field(name="Gold bars from Assistance quests", value="800", inline=False)
        embed.add_field(name="Resources",value="\n".join(sclist[:len(sclist)]), inline=False)
        embed.set_footer(text=f"Invoked by {ctx.author}", icon_url=ctx.author.avatar_url)
        await ctx.reply(embed=embed)

    @commands.command(aliases=["sp"])
    async def silentplain(self, ctx):
        color_main = color[random.randint(0, len(color)-1)]
        embed = discord.Embed(title='__**Silent Plain**__', color=color_main)
        embed.add_field(name="Resource level", value="7", inline=False)
        embed.add_field(name="Recommended Combat level",
                        value="78", inline=False)
        embed.add_field(name="Gold bars from Assistance quests",
                        value="800", inline=False)
        embed.add_field(name="Resources", value="\n".join(
            splist[:len(splist)]), inline=False)
        embed.set_footer(
            text=f"Invoked by {ctx.author}", icon_url=ctx.author.avatar_url)
        await ctx.reply(embed=embed)

    @commands.command(aliases=["swb"])
    async def swampborder(self, ctx):
        color_main = color[random.randint(0, len(color)-1)]
        embed = discord.Embed(title='__**Swamp Border**__', color=color_main)
        embed.add_field(name="Resource level", value="6", inline=False)
        embed.add_field(name="Recommended Combat level",
                        value="61", inline=False)
        embed.add_field(name="Gold bars from Assistance quests",
                        value="800", inline=False)
        embed.add_field(name="Resources", value="\n".join(
            swblist[:len(swblist)]), inline=False)
        embed.set_footer(
            text=f"Invoked by {ctx.author}", icon_url=ctx.author.avatar_url)
        await ctx.reply(embed=embed)

    @commands.command(aliases = ["lb", "lawrence"])
    async def lawrencebay(self, ctx):
        color_main = color[random.randint(0,len(color)-1)]
        embed = discord.Embed(title='__**Lawrence Bay**__' ,color=color_main)
        embed.add_field(name="Resource level", value="6", inline=False)
        embed.add_field(name="Recommended Combat level", value="68", inline=False)
        embed.add_field(name="Gold bars from Assistance quests", value="800", inline=False)
        embed.add_field(name="Resources",value="\n".join(lblist[:len(lblist)]), inline=False)
        embed.set_footer(text=f"Invoked by {ctx.author}", icon_url=ctx.author.avatar_url)
        await ctx.reply(embed=embed)

    @commands.command(aliases = ["ma", "apparition"])
    async def mountapparition(self, ctx):
        color_main = color[random.randint(0,len(color)-1)]
        embed = discord.Embed(title='__**Mount Apparition**__' ,color=color_main)
        embed.add_field(name="Resource level", value="5", inline=False)
        embed.add_field(name="Recommended Combat level", value="51", inline=False)
        embed.add_field(name="Gold bars from Assistance quests", value="800", inline=False)
        embed.add_field(name="Resources",value="\n".join(malist[:len(malist)]), inline=False)
        embed.set_footer(text=f"Invoked by {ctx.author}", icon_url=ctx.author.avatar_url)
        await ctx.reply(embed=embed)

    @commands.command(aliases = ["lesp", "lesins"])
    async def lesinsport(self, ctx):
        color_main = color[random.randint(0,len(color)-1)]
        embed = discord.Embed(title='__**Lesins Port**__' ,color=color_main)
        embed.add_field(name="Resource level", value="3", inline=False)
        embed.add_field(name="Recommended Combat level", value="26", inline=False)
        embed.add_field(name="Gold bars from Assistance quests", value="750", inline=False)
        embed.add_field(name="Resources",value="\n".join(lesplist[:len(lesplist)]), inline=False)
        embed.set_footer(text=f"Invoked by {ctx.author}", icon_url=ctx.author.avatar_url)
        await ctx.reply(embed=embed)

    @commands.command(aliases=["twc", "twinways"])
    async def twinwayscity(self, ctx):
        color_main = color[random.randint(0, len(color)-1)]
        embed = discord.Embed(title='__**Twin Ways City**__', color=color_main)
        embed.add_field(name="Resource level", value="3", inline=False)
        embed.add_field(name="Recommended Combat level",
                        value="26", inline=False)
        embed.add_field(name="Gold bars from Assistance quests",
                        value="750", inline=False)
        embed.add_field(name="Resources", value="\n".join(
            twclist[:len(twclist)]), inline=False)
        embed.set_footer(
            text=f"Invoked by {ctx.author}", icon_url=ctx.author.avatar_url)
        await ctx.reply(embed=embed)

    @commands.command(aliases=["rwt", "redwood"])
    async def redwoodtown(self, ctx):
        color_main = color[random.randint(0, len(color)-1)]
        embed = discord.Embed(title='__**Redwood Town**__', color=color_main)
        embed.add_field(name="Resource level", value="5", inline=False)
        embed.add_field(name="Recommended Combat level",
                        value="53", inline=False)
        embed.add_field(name="Gold bars from Assistance quests",
                        value="800", inline=False)
        embed.add_field(name="Resources", value="\n".join(
            rwtlist[:len(rwtlist)]), inline=False)
        embed.set_footer(
            text=f"Invoked by {ctx.author}", icon_url=ctx.author.avatar_url)
        await ctx.reply(embed=embed)

    @commands.command(aliases = ["santo"])
    async def santopany(self, ctx):
        color_main = color[random.randint(0,len(color)-1)]
        embed = discord.Embed(title='__**Santopany**__' ,color=color_main)
        embed.add_field(name="Resource level", value="5", inline=False)
        embed.add_field(name="Recommended Combat level", value="56", inline=False)
        embed.add_field(name="Gold bars from Assistance quests", value="800", inline=False)
        embed.add_field(name="Resources",value="\n".join(santolist[:len(santolist)]), inline=False)
        embed.set_footer(text=f"Invoked by {ctx.author}", icon_url=ctx.author.avatar_url)
        await ctx.reply(embed=embed)

    @commands.command(aliases = ["riva", "river"])
    async def riverarea(self, ctx):
        color_main = color[random.randint(0,len(color)-1)]
        embed = discord.Embed(title='__**River Area**__' ,color=color_main)
        embed.add_field(name="Resource level", value="4", inline=False)
        embed.add_field(name="Recommended Combat level", value="38", inline=False)
        embed.add_field(name="Gold bars from Assistance quests", value="750", inline=False)
        embed.add_field(name="Resources",value="\n".join(rivalist[:len(rivalist)]), inline=False)
        embed.set_footer(text=f"Invoked by {ctx.author}", icon_url=ctx.author.avatar_url)
        await ctx.reply(embed=embed)

    @commands.command(aliases=["wolf", "wfh"])
    async def wolfhuntingfield(self, ctx):
        color_main = color[random.randint(0, len(color)-1)]
        embed = discord.Embed(title='__**Wolf-hunting Field**__', color=color_main)
        embed.add_field(name="Resource level", value="3", inline=False)
        embed.add_field(name="Recommended Combat level",
                        value="26", inline=False)
        embed.add_field(name="Gold bars from Assistance quests",
                        value="750", inline=False)
        embed.add_field(name="Resources", value="\n".join(
            wolflist[:len(wolflist)]), inline=False)
        embed.set_footer(
            text=f"Invoked by {ctx.author}", icon_url=ctx.author.avatar_url)
        await ctx.reply(embed=embed)

    @commands.command(aliases = ["bpa", "blackpearl"])
    async def blackpearlarea(self, ctx):
        color_main = color[random.randint(0,len(color)-1)]
        embed = discord.Embed(title='__**Black Pearl Area**__' ,color=color_main)
        embed.add_field(name="Resource level", value="3", inline=False)
        embed.add_field(name="Recommended Combat level", value="26", inline=False)
        embed.add_field(name="Gold bars from Assistance quests", value="750", inline=False)
        embed.add_field(name="Resources",value="\n".join(bpalist[:len(bpalist)]), inline=False)
        embed.set_footer(text=f"Invoked by {ctx.author}", icon_url=ctx.author.avatar_url)
        await ctx.reply(embed=embed)

    @commands.command(aliases = ["miska"])
    async def miskatown(self, ctx):
        color_main = color[random.randint(0,len(color)-1)]
        embed = discord.Embed(title='__**Miska Town**__' ,color=color_main)
        embed.add_field(name="Resource level", value="4", inline=False)
        embed.add_field(name="Recommended Combat level", value="38", inline=False)
        embed.add_field(name="Gold bars from Assistance quests", value="750", inline=False)
        embed.add_field(name="Resources",value="\n".join(miskalist[:len(miskalist)]), inline=False)
        embed.set_footer(text=f"Invoked by {ctx.author}", icon_url=ctx.author.avatar_url)
        await ctx.reply(embed=embed)

    @commands.command(aliases = ["rona"])
    async def strona(self, ctx):
        color_main = color[random.randint(0,len(color)-1)]
        embed = discord.Embed(title='__**St. Rona**__' ,color=color_main)
        embed.add_field(name="Resource level", value="8", inline=False)
        embed.add_field(name="Recommended Combat level", value="83", inline=False)
        embed.add_field(name="Gold bars from Assistance quests", value="800", inline=False)
        embed.add_field(name="Resources",value="\n".join(ronalist[:len(ronalist)]), inline=False)
        embed.set_footer(text=f"Invoked by {ctx.author}", icon_url=ctx.author.avatar_url)
        await ctx.reply(embed=embed)

    @commands.command(aliases = ["pt", "polar", "tjaele"])
    async def polartjaele(self, ctx):
        color_main = color[random.randint(0,len(color)-1)]
        embed = discord.Embed(title='__**Polar Tjaele**__' ,color=color_main)
        embed.add_field(name="Resource level", value="3", inline=False)
        embed.add_field(name="Recommended Combat level", value="26", inline=False)
        embed.add_field(name="Gold bars from Assistance quests", value="750", inline=False)
        embed.add_field(name="Resources",value="\n".join(ptlist[:len(ptlist)]), inline=False)
        embed.set_footer(text=f"Invoked by {ctx.author}", icon_url=ctx.author.avatar_url)
        await ctx.reply(embed=embed)

    @commands.command(aliases=["ff"])
    async def fallforest(self, ctx):
        color_main = color[random.randint(0, len(color)-1)]
        embed = discord.Embed(title='__**Fall Forest**__', color=color_main)
        embed.add_field(name="Resource level", value="1", inline=False)
        embed.add_field(name="Recommended Combat level",
                        value="3", inline=False)
        embed.add_field(name="Gold bars from Assistance quests",
                        value="700", inline=False)
        embed.add_field(name="Resources", value="\n".join(
            fflist[:len(fflist)]), inline=False)
        embed.set_footer(
            text=f"Invoked by {ctx.author}", icon_url=ctx.author.avatar_url)
        await ctx.reply(embed=embed)

    @commands.command(aliases=["swamp", "mswamp"])
    async def mouthswamp(self, ctx):
        color_main = color[random.randint(0, len(color)-1)]
        embed = discord.Embed(title='__**Mouth Swamp**__', color=color_main)
        embed.add_field(name="Resource level", value="6", inline=False)
        embed.add_field(name="Recommended Combat level",
                        value="63", inline=False)
        embed.add_field(name="Gold bars from Assistance quests",
                        value="800", inline=False)
        embed.add_field(name="Resources", value="\n".join(
            swamplist[:len(swamplist)]), inline=False)
        embed.set_footer(
            text=f"Invoked by {ctx.author}", icon_url=ctx.author.avatar_url)
        await ctx.reply(embed=embed)

    @commands.command(aliases=["mouth"])
    async def mouthtown(self, ctx):
        color_main = color[random.randint(0, len(color)-1)]
        embed = discord.Embed(title='__**Mount Snow**__', color=color_main)
        embed.add_field(name="Resource level", value="3", inline=False)
        embed.add_field(name="Recommended Combat level",
                        value="26", inline=False)
        embed.add_field(name="Gold bars from Assistance quests",
                        value="750", inline=False)
        embed.add_field(name="Resources", value="\n".join(
            mouthlist[:len(mouthlist)]), inline=False)
        embed.set_footer(
            text=f"Invoked by {ctx.author}", icon_url=ctx.author.avatar_url)
        await ctx.reply(embed=embed)

    @commands.command()
    async def res(self, ctx, *, query):
        found = []
        query = query.title()
        for i in range(0, len(total)):
            for key, value in total[i].items():
                if query in value:
                    found.append(key)
        color_main = color[random.randint(0, len(color)-1)]
        embed = discord.Embed(title=f'__**Location of {query}**__', color=color_main)
        embed.add_field(name="Locations:", value="\n".join(found[:len(found)]), inline=False)
        embed.set_footer(text=f"Invoked by {ctx.author}", icon_url=ctx.author.avatar_url)
        await ctx.reply(embed=embed)

def setup(bot):
    bot.add_cog(resources(bot))
