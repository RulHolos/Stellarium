# Stellarium
# Fait pour tourner en version 1.4.1 du module discord.

import discord, asyncio, datetime, json, random, time, os, requests, aiohttp
from discord.ext import commands, tasks
from discord.utils import get
from itertools import cycle
from discord import *
from discord.ext.commands import has_permissions
from termcolor import colored

from helpers.config import get_lang, get_prefix, get_default_prefix, get_bot_version, get_bot_owner
from helpers.errors import CmdCheckError, DebugCheckError
from helpers.checks import cmdcheck, debugcheck

client = commands.Bot(command_prefix=get_prefix)
client.remove_command('help')


# # # Variables # # #

LienInvitation = "https://discordapp.com/oauth2/authorize?client_id=746348869574459472&scope=bot&permissions=2012740695"
#status = cycle(['by Atae Kurri#6302 | ;help', f'{versionBot} | ;help', ';help for help'])
cmds = ["guildes", "infos", "roll", "setLang", "moderation", "prefixGestion", "danbooru",
        "SCP", "meteo", "broadcast", "template", "togglecmd", "help"]
os.system('color')
os.system('cls')

# # # Defs et classes # # #

#@tasks.loop(seconds=20)
#async def change_status():
#    await client.change_presence(activity=discord.Game(next(status)))

# # # console # # #

@client.command()
@debugcheck()
async def console(ctx):
    if ctx.message.author.id != get_bot_owner():
        raise commands.CheckFailure
    else:
        print(colored("Que voulez-vous faire ? (help pour la liste des commandes)", "yellow"))
        cmd = input("> ")
        if cmd.upper() == "HELP":
            print(colored("say, help, listservs, exit", "yellow"))
            await console(ctx)
        elif cmd.upper() == "SAY":
            print(colored("Quel serveur voulez-vous ?", "yellow"))
            for servs in list(client.guilds):
                print(f"{servs.name} -> {servs.id}")
            serv = int(input("> "))
            
            print(colored("Quel channel voulez-vous ?", "yellow"))
            get_serv = client.get_guild(serv)
            for chans in get_serv.text_channels:
                print(f"{chans.name} -> {chans.id}")
            chan = int(input("> "))

            get_chan = client.get_channel(chan)
            await console_send_msg(get_chan, ctx)

        elif cmd.upper() == "LISTSERVS":
            for servs in list(client.guilds):
                print(f"{servs.name} -> {servs.id}")
            await console(ctx)
        elif cmd.upper() == "EXIT":
            os.system('cls')
            on_ready_print()
        else:
            os.system('cls')
            on_ready_print()
            
async def console_send_msg(chan, ctx):
    print(colored("Que voulez-vous envoyer ? (S = stop)", "yellow"))
    msg = input("> ")
    if msg.upper() == "S":
        await console(ctx)
    else:
        await chan.send(msg)
        await console_send_msg(chan, ctx)


# # # Events # # #

def on_ready_print():
    print(colored('------', "red"))
    print(colored('Bot lancé sous', "green"))
    print(colored(client.user.name, "yellow"))
    print(colored(client.user.id, "green"))
    print(f'module discord en version {colored(discord.__version__, "green")}')
    print('Version actuelle du bot : ' + colored(f"{get_bot_version()}", "green"))
    print(f'Dans {len(list(client.guilds))} serveurs.')
    print(colored('------', "red"))
    print(f"Commandes : {', '.join(cmds)}")
    print(f'General Command Prefix : {colored(";", "yellow")}')
    print(colored('------', "red"))
    print(' ')

@client.event
async def on_ready():
    os.system('cls')
    on_ready_print()

    await client.change_presence(activity=discord.Game(f'{get_bot_version()} | ;help'))
    #change_status.start()

@client.event
async def on_guild_join(guild):
    conf = json.load(open("json/serverconfig.json", 'r'))
    Iguild = str(guild.id)
    conf[Iguild] = {}
    conf[Iguild]["lang"] = "en"
    conf[Iguild]["creator"] = guild.owner.id
    conf[Iguild]["prefix"] = get_default_prefix()
    conf[Iguild]["cmds"] = {}

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

    ### Custom errors (from helpers.errors) ###

    if isinstance(error, CmdCheckError): # Une commande n'est pas utilisable sur un serveur
        await ctx.send(get_lang(str(ctx.guild.id), "CmdCheckError"))

    if isinstance(error, DebugCheckError): # Le mode global debug est activé sur le bot
        await ctx.send(get_lang(str(ctx.guild.id), "Debug_Check"))

    if isinstance(error, RuntimeError):
        pass

    print(error)

# # # Commandes # # #

@client.command()
@cmdcheck("changelog")
async def changelog(ctx, version=""):
    if not version:
        version = get_bot_version()
    changelogs = json.load(open("json/changelogs.json", 'r'))
    c = json.load(open("json/serverconfig.json", 'r'))

    embed = discord.Embed(colour=ctx.author.top_role.colour.value)
    embed.set_author(name=f"Changelog Stellarium {version}")
    embed.set_thumbnail(url=client.get_user(746348869574459472).avatar_url)

    embed.add_field(name="+", value=changelogs[version][c[str(ctx.guild.id)]["lang"]]["+"], inline=False)
    embed.add_field(name="-", value=changelogs[version][c[str(ctx.guild.id)]["lang"]]["-"], inline=False)

    await ctx.send(embed=embed)


for cmd in cmds:
    client.load_extension(f"cogs.{cmd}")



client.run(open("token.txt", "r").read())
