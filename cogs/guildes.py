import discord, json, random, uuid, asyncio, argparse
from datetime import date
from discord.ext import commands

from cogs.config import get_lang

class guildes(commands.Cog):
    def __init__(self, client):
        self.client = client


    @commands.command(aliases=["GuildInfo"])
    async def guildInfo(self, ctx, *, name=""):
        if name:
            guildjson = json.load(open("json/guilds.json", 'r'))
            if name in guildjson:
                embed = discord.Embed(colour=guildjson[name]["creatorRoleColor"])
                embed.set_author(name=f'{guildjson[name]["name"]}, LVL : {guildjson[name]["lvl"]}, EXP : {guildjson[name]["xp"]}')
                embed.set_footer(text="Stellarium Guild Module, v0.0.3 Alpha")
                embed.set_thumbnail(url=self.client.get_user(guildjson[name]["creator"]).avatar_url)

                embed.add_field(name="id", value=guildjson[name]["id"], inline=False)
                embed.add_field(name="members", value=len(guildjson[name]["members"]), inline=True)
                embed.add_field(name="Creator", value=self.client.get_user(guildjson[name]["creator"]).name, inline=True)
                embed.add_field(name="Private", value="Y" if guildjson[name]["private"] else "N", inline=True)
                embed.add_field(name="Slots", value=guildjson[name]["MaxSlots"], inline=True)
                embed.add_field(name=get_lang(ctx.guild.id, "UserCreatedAt"), value=guildjson[name]["created_at"], inline=True)

                embed.add_field(name="Description", value=guildjson[name]["desc"] or "None", inline=False)
                embed.add_field(name="Badges", value=' ; '.join([name for name in guildjson[name]["Badges"]]) or "None", inline=False)

                await ctx.send(embed=embed)
            else: await ctx.send(get_lang(ctx.guild.id, "incorrectGuildName"))
        else: await ctx.send(get_lang(ctx.guild.id, "argumentNeeded"))

    @commands.command(aliases=["createGuild", "createguild"])
    async def CreateGuild(self, ctx, *args):
        try:
            parser = argparse.ArgumentParser()
            parser.add_argument('name', type=str)
            parser.add_argument('-d', '--desc', type=str)
            parser.add_argument('-p', '--private', action='store_true')
            parse = parser.parse_args(args)
            name = parse.name
            if name:
                guildjson = json.load(open("json/guilds.json", 'r'))
                if not name in guildjson:
                    guildjson[name] = {}
                    guildjson[name]["name"] = name
                    guildjson[name]["id"] = str(uuid.uuid4())
                    guildjson[name]["desc"] = parse.desc or ""
                    guildjson[name]["members"] = {}
                    guildjson[name]["MaxSlots"] = 5
                    guildjson[name]["creator"] = ctx.message.author.id
                    guildjson[name]["creatorRoleColor"] = ctx.message.author.top_role.colour.value
                    guildjson[name]["members"][ctx.message.author.id] = ctx.message.author.id
                    guildjson[name]["lvl"] = 1
                    guildjson[name]["xp"] = 0
                    guildjson[name]["private"] = True if parse.private else False
                    guildjson[name]["InviteLinks"] = {}
                    guildjson[name]["Items"] = {}
                    guildjson[name]["Badges"] = {}
                    guildjson[name]["created_at"] = f"{date.today().strftime('%d/%m/%Y')} (d/m/y)"
                    with open("json/guilds.json", "w") as f:
                        json.dump(guildjson, f, indent=2)
                    await ctx.send(f'{get_lang(ctx.guild.id, "GuildCreated")} : {name}')
                else: await ctx.send(get_lang(ctx.guild.id, "GuildAlreadyExists"))
            else: await ctx.send(get_lang(ctx.guild.id, "argumentNeeded"))
        except: raise commands.BadArgument


    @commands.command(aliases=["editguilddesc", "editGuildDesc"])
    async def EditGuildDesc(self, ctx, *args):
        try:
            parser = argparse.ArgumentParser()
            parser.add_argument('name', type=str)
            parser.add_argument('desc', type=str)
            parse = parser.parse_args(args)
            name = parse.name
            desc = parse.desc

            guildjson = json.load(open("json/guilds.json", 'r'))
            if (name and desc):
                found = False
                for guilds in guildjson:
                    if name in guildjson[guilds]["name"]:
                        found = True
                        if ctx.message.author.id == guildjson[guilds]["creator"]:
                            guildjson[guilds]["desc"] = desc
                            with open("json/guilds.json", "w") as f:
                                json.dump(guildjson, f, indent=2)
                            await ctx.send(get_lang(ctx.guild.id, "GuildDescModified"))
                        else: await ctx.send(get_lang(ctx.guild.id, "CheckFailure"))
                if not found: await ctx.send(get_lang(ctx.guild.id, "GuildDontExists"))
            else: await ctx.send(get_lang(ctx.guild.id, "argumentNeeded"))
        except: raise commands.BadArgument

    @commands.command(aliases=["joinguild", "joinGuild", "Joinguild"])
    async def JoinGuild(self, ctx, name=""):
        guildjson = json.load(open("json/guilds.json", 'r'))
        if name:
            found = False
            for guilds in guildjson:

                if name in guildjson[guilds]["name"]:
                    found = True
                    if not guildjson[guilds]["private"]:
                        if not str(ctx.message.author.id) in guildjson[guilds]["members"]:
                            if not len(guildjson[guilds]["members"]) >= int(guildjson[guilds]["MaxSlots"]):
                                guildjson[guilds]["members"][ctx.message.author.id] = ctx.message.author.id
                                with open("json/guilds.json", "w") as f:
                                    json.dump(guildjson, f, indent=2)
                                await ctx.send(get_lang(ctx.guild.id, "GuildJoined"))
                            else: await ctx.send(get_lang(ctx.guild.id, "GuildFull"))
                        else: await ctx.send(get_lang(ctx.guild.id, "AlreadyInGuild"))
                    else: await ctx.send(get_lang(ctx.guild.id, "PrivateGuild"))

                elif name in guildjson[guilds]["InviteLinks"]:
                    found = True
                    guildjson[guilds]["members"][ctx.message.author.id] = ctx.message.author.id
                    guildjson[guilds]["InviteLinks"].pop(name)
                    with open("json/guilds.json", "w") as f:
                        json.dump(guildjson, f, indent=2)
                    await ctx.send(get_lang(ctx.guild.id, "GuildJoined"))

            if not found: await ctx.send(get_lang(ctx.guild.id, "GuildDontExists"))
        else: await ctx.send(get_lang(ctx.guild.id, "argumentNeeded"))

    @commands.command()
    async def LeaveGuild(self, ctx, name=""):
        """ Quitter une guilde dont fait parti une personne. """
        guildjson = json.load(open("json/guilds.json", 'r'))
        if name:
            found = False
            for guilds in guildjson:
                if name in guildjson[guilds]["name"]:
                    found = True
                    if str(ctx.message.author.id) in guildjson[guilds]["members"]:
                        guildjson[guilds]["members"].pop(str(ctx.message.author.id))
                        if len(guildjson[guilds]["members"]) == 0:
                            guildjson.pop(guilds)
                        with open("json/guilds.json", "w") as f:
                            json.dump(guildjson, f, indent=2)
                        await ctx.send(get_lang(ctx.guild.id, "GuildLeaved"))
                    else: await ctx.send(get_lang(ctx.guild.id, "CantLeaveGuildIfNotIn"))
            if not found: await ctx.send(get_lang(ctx.guild.id, "GuildDontExists"))
        else: await ctx.send(get_lang(ctx.guild.id, "argumentNeeded"))

    @commands.command()
    async def GuildLink(self, ctx, id=""):
        guildjson = json.load(open("json/guilds.json", 'r'))
        if id:
            for guilds in guildjson:
                if str(id) in guildjson[guilds]["id"]:
                    if ctx.message.author.id == guildjson[guilds]["creator"]:
                        if guildjson[guilds]["private"]:
                            link = str(guildjson[guilds]["id"]) + "--" + str(random.randint(0, 9999))
                            guildjson[guilds]["InviteLinks"][link] = "Exists"
                            with open("json/guilds.json", "w") as f:
                                json.dump(guildjson, f, indent=2)
                            await ctx.send(get_lang(ctx.guild.id, "SendedInDMs"))
                            await ctx.author.send(link)
                        else: await ctx.send(get_lang(ctx.guild.id, "CantLinkUnPrivateGuilds"))
                    else: await ctx.send(get_lang(ctx.guild.id, "CheckFailure"))
        else: await ctx.send(get_lang(ctx.guild.id, "argumentNeeded"))

    @commands.command()
    async def DeleteGuild(self, ctx, id=""):
        guildjson = json.load(open("json/guilds.json", 'r'))
        if id:
            found = False
            for guilds in guildjson:
                if str(id) in guildjson[guilds]["id"]:
                    found = True
                    if ctx.message.author.id == guildjson[guilds]["creator"]:
                        guildjson.pop(guilds)
                        with open("json/guilds.json", "w") as f:
                            json.dump(guildjson, f, indent=2)
                        await ctx.send(get_lang(ctx.guild.id, "GuildDeleted"))
                    else: await ctx.send(get_lang(ctx.guild.id, "CheckFailure"))
            if not found: await ctx.send(get_lang(ctx.guild.id, "GuildDontExists"))
        else: await ctx.send(get_lang(ctx.guild.id, "argumentNeeded"))

    @commands.command()
    async def TogglePrivate(self, ctx, id=""):
        guildjson = json.load(open("json/guilds.json", 'r'))
        if id:
            found = False
            for guilds in guildjson:
                if str(id) in guildjson[guilds]["id"]:
                    found = True
                    if ctx.message.author.id == guildjson[guilds]["creator"]:
                        guildjson[guilds]["private"] = not guildjson[guilds]["private"]
                        with open("json/guilds.json", "w") as f:
                            json.dump(guildjson, f, indent=2)
                        await ctx.send(f'{get_lang(ctx.guild.id, "PrivateToggled")} {"Y" if guildjson[guilds]["private"] else "N"}!')
                    else: await ctx.send(get_lang(ctx.guild.id, "CheckFailure"))
            if not found: await ctx.send(get_lang(ctx.guild.id, "GuildDontExists"))
        else: await ctx.send(get_lang(ctx.guild.id, "argumentNeeded"))

    @commands.command(aliases=["guildshop"])
    async def GuildShop(self, ctx, *, name=""):
        if name:
            guildjson = json.load(open("json/guilds.json", 'r'))
            def check(reaction, user):
                return user == ctx.message.author and str(reaction.emoji) in [u"\U0001F5F3", u"\U0001F525"]

            found = False
            GuildName = None
            for guilds in guildjson:
                if name in guildjson[guilds]["name"]:
                    found = True
                    GuildName = guilds

            if not found:
                await ctx.send(get_lang(ctx.guild.id, "GuildDontExists"))
            else:
                embed = discord.Embed(colour=ctx.message.author.top_role.colour.value)
                embed.set_author(name="Guild Shop")
                embed.set_thumbnail(url=ctx.message.author.avatar_url)
                embed.set_footer(text="React to buy something!")

                embed.add_field(name="Guild Slot :ballot_box:", value="4 guild LVLs for 5 slots.", inline=True)
                embed.add_field(name="Fire badge :fire:", value="30 levels for a useless badge", inline=True)

                msg = await ctx.send(embed=embed)
                ballot = u"\U0001F5F3"
                fire = u"\U0001F525"
                await msg.add_reaction(ballot)
                await msg.add_reaction(fire)

                emojis = [ballot, fire]
                while emojis:
                    try:
                        reaction, user = await self.client.wait_for('reaction_add', timeout=3600.0, check=check)
                    except asyncio.TimeoutError:
                        pass
                    else:
                        emojis = [e for e in emojis if e != reaction]
                        if reaction.emoji == ballot:
                            guildjson1 = json.load(open("json/guilds.json", 'r'))
                            await msg.remove_reaction(ballot, user)
                            if ctx.message.author.id == guildjson1[GuildName]["creator"]:
                                if guildjson1[GuildName]["lvl"] >= 4:
                                    guildjson1[GuildName]["lvl"] -= 4
                                    guildjson1[GuildName]["MaxSlots"] += 5
                                    with open("json/guilds.json", "w") as f:
                                        json.dump(guildjson1, f, indent=2)
                                    await ctx.send(get_lang(ctx.guild.id, "GuildShop_01"))
                                else: await ctx.send(get_lang(ctx.guild.id, "TooLowLevel"))
                            else: await ctx.send(get_lang(ctx.guild.id, "CheckFailure"))
                        if reaction.emoji == fire:
                            guildjson1 = json.load(open("json/guilds.json", 'r'))
                            await msg.remove_reaction(ballot, user)
                            if ctx.message.author.id == guildjson1[GuildName]["creator"]:
                                if guildjson1[GuildName]["lvl"] >= 30:
                                    guildjson1[GuildName]["lvl"] -= 30
                                    guildjson1[GuildName]["Badges"]["Wow, you paid 30 lvls for nothing"] = "Wow, you paid 30 lvls for nothing"
                                    with open("json/guilds.json", "w") as f:
                                        json.dump(guildjson1, f, indent=2)
                                    await ctx.send(get_lang(ctx.guild.id, "GuildShop_02"))
                                else: await ctx.send(get_lang(ctx.guild.id, "TooLowLevel"))
                            else: await ctx.send(get_lang(ctx.guild.id, "CheckFailure"))
        else: await ctx.send(get_lang(ctx.guild.id, "ProvideGuildName"))

    @commands.command(aliases=["Leaderboard"])
    async def leaderboard(self, ctx):
        guildjson = json.load(open("json/guilds.json", 'r'))
        sort = sorted(guildjson, key=lambda x: guildjson[x].get("xp", 0), reverse=True)
        leaderboardList = {}
        for guilds in range(0, 5):
            try:
                leaderboardList[guilds] = sort[guilds]
            except:
                leaderboardList[guilds] = "None"

        msg = f"""```Leaderboard {get_lang(ctx.guild.id, "for")} 5 guilds.

------------------------------

1. {guildjson[leaderboardList[0]]["name"]}. {len(guildjson[leaderboardList[0]]["members"])} {get_lang(ctx.guild.id, "Members")}.
LVL = {guildjson[leaderboardList[0]]["lvl"]}. EXP = {guildjson[leaderboardList[0]]["xp"]}.

------------------------------
2. {guildjson[leaderboardList[1]]["name"]}. {len(guildjson[leaderboardList[1]]["members"])} {get_lang(ctx.guild.id, "Members")}.
LVL = {guildjson[leaderboardList[1]]["lvl"]}. EXP = {guildjson[leaderboardList[1]]["xp"]}.
------------------------------
3. {guildjson[leaderboardList[2]]["name"]}. {len(guildjson[leaderboardList[2]]["members"])} {get_lang(ctx.guild.id, "Members")}.
LVL = {guildjson[leaderboardList[2]]["lvl"]}. EXP = {guildjson[leaderboardList[2]]["xp"]}.
------------------------------
4. {guildjson[leaderboardList[3]]["name"]}. {len(guildjson[leaderboardList[3]]["members"])} {get_lang(ctx.guild.id, "Members")}.
LVL = {guildjson[leaderboardList[3]]["lvl"]}. EXP = {guildjson[leaderboardList[3]]["xp"]}.
------------------------------
5. {guildjson[leaderboardList[4]]["name"]}. {len(guildjson[leaderboardList[4]]["members"])} {get_lang(ctx.guild.id, "Members")}.
LVL = {guildjson[leaderboardList[4]]["lvl"]}. EXP = {guildjson[leaderboardList[4]]["xp"]}.
------------------------------
```"""
        await ctx.send(msg)

        if not "At the top of the World" in guildjson[leaderboardList[0]]["Badges"]:
            guildjson[leaderboardList[0]]["Badges"]["**At the top of the World**"] = "**At the top of the World**"
            with open("json/guilds.json", "w") as f:
                json.dump(guildjson, f, indent=2)

    @commands.command(aliases=["Badges", "Badge", "badge"])
    async def badges(self, ctx, *, badge=""):
        """ Voir les différents badges existants avec leur description """
        if badge:
            await ctx.send("En dev.")
        else:
            c = json.load(open("json/serverconfig.json", 'r'))
            j = json.load(open("json/badges.json", "r"))
            embed = discord.Embed(colour=ctx.author.top_role.colour.value)
            embed.set_author(name="Badges")
            embed.set_thumbnail(url=self.client.get_user(746348869574459472).avatar_url)
            embed.set_footer(text="Page 1/1")

            for badges in j:
                embed.add_field(name=j[badges]["name"], value=f'{j[badges][c[str(ctx.guild.id)]["lang"]]} (ID : {j[badges]["id"]})', inline=True)

            await ctx.send(embed=embed)

    @commands.Cog.listener()
    async def on_message(self, message):
        """ Système de niveau inter-guildes """
        guildjson = json.load(open("json/guilds.json", 'r'))
        for guilds in guildjson:
            if str(message.author.id) in guildjson[guilds]["members"]:
                guildjson[guilds]["xp"] += 5
                with open("json/guilds.json", "w") as f:
                    json.dump(guildjson, f, indent=2)
                if guildjson[guilds]["lvl"] < int(guildjson[guilds]["xp"] ** (1/4)):
                    guildjson[guilds]["lvl"] += 1
                    with open("json/guilds.json", "w") as f:
                        json.dump(guildjson, f, indent=2)

def setup(client):
    client.add_cog(guildes(client))
