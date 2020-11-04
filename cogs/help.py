import discord, re, json
from discord.ext import commands

from helpers.config import get_lang, get_prefix, get_guild_lang

class help(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=["aide", "Aide", "Help"])
    async def help(self, ctx, page=""):
        hpage = page or "1"
        guild = str(ctx.guild.id)
        embed = discord.Embed(colour=ctx.author.top_role.colour.value)
        embed.set_footer(text=f"help page {hpage}/2")
        c = json.load(open("json/serverconfig.json", 'r'))
        p = c[str(ctx.guild.id)]["prefix"]

        if hpage == "1":
            embed.add_field(name=f'{p}setPrefix <prefix>', value="Change prefix", inline=True)
            embed.add_field(name=f"{p}userinfo", value=f'{get_lang(guild, "help_01")}', inline=True)
            embed.add_field(name=f"{p}roll <valeur>d<valeur>", value=f'{get_lang(guild, "help_02")}', inline=True)
            embed.add_field(name=f"{p}setLang <prefix>", value=f'{get_lang(guild, "help_03")}', inline=True)
            embed.add_field(name=f"{p}serverinfo", value=get_lang(guild, "help_04"), inline=True)
            embed.add_field(name=f"{p}ban/{p}kick <user>", value=get_lang(guild, "help_05"), inline=True)
            embed.add_field(name=f'{p}CreateGuild "name" [-d "Description"] [-p]', value=get_lang(guild, "help_06"), inline=True)
            embed.add_field(name=f"{p}GuildInfo <name>", value=get_lang(guild, "help_07"), inline=True)
            embed.add_field(name=f'{p}EditGuildDesc "name" "description"', value=get_lang(guild, "help_08"), inline=True)
            embed.add_field(name=f"{p}JoinGuild/{p}LeaveGuild <guild>", value=get_lang(guild, "help_09"), inline=True)
            embed.add_field(name=f"{p}DeleteGuild <GuildID>", value=get_lang(guild, "help_10"), inline=True)
            embed.add_field(name=f"{p}GuildLink <GuildID>", value=get_lang(guild, "help_11"), inline=True)
            embed.add_field(name=f"{p}TogglePrivate <GuildID>", value=get_lang(guild, "help_12"), inline=True)
            embed.add_field(name=f"{p}leaderboard", value=get_lang(guild, "help_13"), inline=True)
            embed.add_field(name=f"{p}GuildShop <name>", value=get_lang(guild, "help_14"), inline=True)
            embed.add_field(name=f"{p}SCP <[1234567890]>", value=get_lang(guild, "help_15"), inline=True)
            embed.add_field(name=f"{p}weather city", value=get_lang(guild, "help_16"), inline=True)
            await ctx.send(embed=embed)
        elif hpage == "2":
            embed.add_field(name=f'{p}create_template [name]', value=get_lang(guild, "help_17"), inline=True)
            embed.add_field(name=f'{p}ToggleCmd [cmd]', value=get_lang(guild, "help_18"), inline=True)
            embed.add_field(name=f'{p}nocmd', value=get_lang(guild, "help_19"), inline=True)
            embed.add_field(name=f'{p}ahelp <cmd>', value=get_lang(guild, "help_20"), inline=True)
            embed.add_field(name=f'{p}anime <anime>', value=get_lang(guild, "help_21"), inline=True)
            await ctx.send(embed=embed)
        else:
            await ctx.send(get_lang(guild, "PageDontExists"))

    @commands.command(aliases=["aaide", "AAide", "AHelp"])
    async def ahelp(self, ctx, cmdn=""):
        if cmdn:
            guild = ctx.guild.id
            embed = discord.Embed(colour=ctx.author.top_role.colour.value)
            embed.set_footer(text=f"help for {cmdn}")
            p = await get_prefix(self.client, ctx.message)
            lang = get_guild_lang(ctx.guild.id)
            with open("json/ahelp.json", 'r') as f:
                ahelp = json.load(f)
            
            found = False
            for cmd in ahelp[lang]:
                if cmdn in ahelp[lang]:
                    found = True
                    embed.add_field(name='Aliases', value=ahelp[lang][cmdn]["aliases"], inline=False)
                    embed.add_field(name='Description', value=ahelp[lang][cmdn]["purpose"], inline=False)
                    embed.add_field(name='Permissions', value=ahelp[lang][cmdn]["permissions"], inline=True)
                    embed.add_field(name='Restrictions', value=ahelp[lang][cmdn]["restrictions"], inline=True)
                    embed.add_field(name='Usage', value=f'{p}{ahelp[lang][cmdn]["usage"]}', inline=False)
                    await ctx.send(embed=embed)
                if found:
                    break

            if not found:
                await ctx.send(get_lang(guild, "CmdDontExists"))
        else:
            await ctx.send(get_lang(ctx.guild.id, "argumentNeeded"))


def setup(client):
    client.add_cog(help(client))
