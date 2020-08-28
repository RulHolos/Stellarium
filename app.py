# Stellarium
# Fait pour tourner en version 1.4.1 du module discord.
versionBot = "v0.0.3"

import discord, asyncio, logging, datetime, json, random, time, os, requests, aiohttp
from discord.ext import commands, tasks
from discord.utils import get
from itertools import cycle
from discord import *
from discord.ext.commands import has_permissions

from cogs.config import get_lang, get_prefix

default_prefix = ";"

client = commands.Bot(command_prefix=get_prefix)
client.remove_command('help')
logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename=(f'logs\{datetime.date.today()}.log'), encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

# # # Variables # # #

LienInvitation = "https://discordapp.com/oauth2/authorize?client_id=746348869574459472&scope=bot&permissions=2012740695"
#status = cycle(['by Atae Kurri#6302 | ;help', f'{versionBot} | ;help', ';help for help'])
cmds = ["guildes", "infos", "roll", "setLang", "moderation", "prefixGestion", "danbooru"]

# # # Defs et classes # # #

#@tasks.loop(seconds=20)
#async def change_status():
#    await client.change_presence(activity=discord.Game(next(status)))

# # # Events # # #

@client.event
async def on_ready():
    print('------')
    print('Bot lancé sous')
    print(client.user.name)
    print(client.user.id)
    print('module discord en version {}'.format(discord.__version__))
    print('Version actuelle du bot : {}'.format(versionBot))
    print(f'Dans {len(list(client.guilds))} serveurs.')
    print('------')
    print(f'Commandes : {[cmd for cmd in cmds]}')
    print('Command Prefix : ;')
    print('------')
    print(' ')

    await client.change_presence(activity=discord.Game(f'{versionBot} | ;help'))
    #change_status.start()

@client.event
async def on_guild_join(guild):
    conf = json.load(open("json/serverconfig.json", 'r'))
    Iguild = str(guild.id)
    conf[Iguild] = {}
    conf[Iguild]["lang"] = "en"
    conf[Iguild]["creator"] = guild.owner.id
    conf[Iguild]["prefix"] = ";"

    with open('json/serverconfig.json', 'w') as sConfSave:
        json.dump(conf, sConfSave, indent=2)

@client.event
async def on_guild_remove(guild):
    conf = json.load(open("json/serverconfig.json", 'r'))
    conf.pop(str(guild.id))

    with open('json/serverconfig.json', 'w') as sConfSave:
        json.dump(conf, sConfSave, indent=2)

@client.event #Easter eggs
async def on_message(message):
    if "True Administrator" in message.content:
        await message.channel.send("Nani ?! Miko ?! O-O'")
    if "Cute Devil" in message.content:
        await message.channel.send("Raep time incomming!")
    await client.process_commands(message)

@client.event
async def on_command_error(ctx, error):
    """ Handling errors """

    if isinstance(error, commands.CheckFailure): # Si une permission d'une has_permissions n'est pas remplie
        await ctx.send(get_lang(str(ctx.guild.id), "CheckFailure"))
    if isinstance(error, commands.BadArgument): # Une commande a un mauvais argument.
        await ctx.send(get_lang(str(ctx.guild.id), "BadArgument"))
    if isinstance(error, commands.CommandNotFound): # Une commande n'est pas trouvée.
        await ctx.send(f'{get_lang(str(ctx.guild.id), "CommandNotFound")} : `{ctx.message.content}`')
    if isinstance(error, RuntimeError):
        pass
    print(error)

# # # Commandes # # #

@client.command(aliases=["aide"])
async def help(ctx):
    guild = str(ctx.guild.id)
    embed = discord.Embed(colour=ctx.author.top_role.colour.value)
    embed.set_footer(text="help page 1/1")
    c = json.load(open("json/serverconfig.json", 'r'))
    p = c[str(ctx.guild.id)]["prefix"]

    embed.add_field(name=f'{p}setPrefix <prefix>', value="Change prefix", inline=True)
    embed.add_field(name=f"{p}userinfo", value=f'{get_lang(guild, "help_01")}', inline=True)
    embed.add_field(name=f"{p}roll <valeur>d<valeur>", value=f'{get_lang(guild, "help_02")}', inline=True)
    embed.add_field(name=f"{p}setLang <prefix>", value=f'{get_lang(guild, "help_03")}', inline=True)
    embed.add_field(name=f"{p}serverinfo", value=get_lang(guild, "help_04"), inline=True)
    embed.add_field(name=f"{p}ban/{p}kick <user>", value=get_lang(guild, "help_05"), inline=True)
    embed.add_field(name=f"{p}CreateGuild <name>", value=get_lang(guild, "help_06"), inline=True)
    embed.add_field(name=f"{p}GuildInfo <name>", value=get_lang(guild, "help_07"), inline=True)
    embed.add_field(name=f'{p}EditGuildDesc <id> "<description>"', value=get_lang(guild, "help_08"), inline=True)
    embed.add_field(name=f"{p}JoinGuild/{p}LeaveGuild <guild>", value=get_lang(guild, "help_09"), inline=True)
    embed.add_field(name=f"{p}DeleteGuild <GuildID>", value=get_lang(guild, "help_10"), inline=True)
    embed.add_field(name=f"{p}GuildLink <GuildID>", value=get_lang(guild, "help_11"), inline=True)
    embed.add_field(name=f"{p}TogglePrivate <GuildID>", value=get_lang(guild, "help_12"), inline=True)
    embed.add_field(name=f"{p}leaderboard", value=get_lang(guild, "help_13"), inline=True)
    embed.add_field(name=f"{p}GuildShop <name>", value=get_lang(guild, "help_14"), inline=True)

    await ctx.send(embed=embed)

@client.command()
async def changelog(ctx, version=""):
    if not version:
        version = versionBot
    changelogs = json.load(open("json/changelogs.json", 'r'))
    c = json.load(open("json/serverconfig.json", 'r'))
    #lang[conf[context]["lang"]][field]

    embed = discord.Embed(colour=ctx.author.top_role.colour.value)
    embed.set_author(name=f"Changelog Stellarium {version}")
    embed.set_thumbnail(url=client.get_user(746348869574459472).avatar_url)

    embed.add_field(name="+", value=changelogs[version][c[str(ctx.guild.id)]["lang"]]["+"], inline=False)
    embed.add_field(name="-", value=changelogs[version][c[str(ctx.guild.id)]["lang"]]["-"], inline=False)

    await ctx.send(embed=embed)


for cmd in cmds:
    client.load_extension(f"cogs.{cmd}")



client.run(open("token.txt", "r").read())
