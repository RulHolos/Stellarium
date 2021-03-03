# Stellarium
# Fait pour tourner en version 1.4.1 du module discord.

import discord, asyncio, datetime, json, random, os, aiohttp, configparser
from discord.ext import commands, tasks
from discord.utils import get
from itertools import cycle
from discord import *
from discord.ext.commands import has_permissions
from termcolor import colored

# imports internes
from helpers.config import get_lang, get_prefix, get_default_prefix, get_bot_version, get_bot_owner, get_bot_id
from helpers.errors import CmdCheckError, DebugCheckError
from helpers.checks import cmdcheck, debugcheck
import helpers.afs_memory as afs

client = commands.AutoShardedBot(command_prefix=get_prefix)
client.remove_command('help')
con = configparser.ConfigParser(converters={'list': lambda x: [i.strip() for i in x.split(',')]}, allow_no_value=True)
con.read("config.ini")


# # # Variables # # #

LienInvitation = con["variables"]["LienInvitation"]
#status = cycle(['by Atae Kurri#6302 | ;help', f'{versionBot} | ;help', ';help for help'])
cmds = con["variables"].getlist("cmds")
os.system('color')
os.system('cls')

# # # Defs et classes # # #

#@tasks.loop(seconds=20)
#async def change_status():
#    await client.change_presence(activity=discord.Game(next(status)))

# # # console # # #

async def console_send_msg(chan, ctx):
    print(colored("Que voulez-vous envoyer ? (S = stop)", "yellow"))
    msg = input("> ")
    if msg.upper() == "S":
        await console(ctx)
    else:
        await chan.send(msg)
        await console_send_msg(chan, ctx)

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
        else:
            os.system('cls')
            on_ready_print()


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
    #conf = json.load(open("json/serverconfig.json", 'r'))
    c_f = afs.afs_memory("db.afs")
    conf = c_f.j_load
    Iguild = str(guild.id)
    conf["serverconfig"][Iguild] = {}
    conf["serverconfig"][Iguild]["lang"] = "en"
    conf["serverconfig"][Iguild]["creator"] = guild.owner.id
    conf["serverconfig"][Iguild]["prefix"] = get_default_prefix()
    conf["serverconfig"][Iguild]["cmds"] = {}

    c_f.write_json_to_afs(c_f.j_load, conf)

    #with open('json/serverconfig.json', 'w') as sConfSave:
    #    json.dump(conf, sConfSave, indent=2)

@client.event
async def on_guild_remove(guild):
    #conf = json.load(open("json/serverconfig.json", 'r'))
    #conf.pop(str(guild.id))
    c_f = afs.afs_memory("db.afs")
    c_f.delete_json_from_afs(c_f.j_load, f"serverconfig.{str(guild.id)}")

    #with open('json/serverconfig.json', 'w') as sConfSave:
    #    json.dump(conf, sConfSave, indent=2)

@client.event #Easter eggs
async def on_message(message):
    if "true administrator" in message.content.lower():
        await message.channel.send("Nani ?! Miko ?! O-O'")
    if "cute devil" in message.content.lower():
        await message.channel.send("Raep time!")
    await client.process_commands(message)

#@client.event
#async def on_command_error(ctx, error):
 #   """ Handling errors """

    #if isinstance(error, commands.CheckFailure): # Si une permission d'une has_permissions n'est pas remplie
     #   await ctx.send(get_lang(str(ctx.guild.id), "CheckFailure"))

    #if isinstance(error, commands.BadArgument): # Une commande a un mauvais argument.
     #   await ctx.send(get_lang(str(ctx.guild.id), "BadArgument"))

    #if isinstance(error, commands.CommandNotFound): # Une commande n'est pas trouvée.
     #   await ctx.send(f'{get_lang(str(ctx.guild.id), "CommandNotFound")} : `{ctx.message.content}`')

    ### Custom errors (from helpers.errors) ###

    #if isinstance(error, CmdCheckError): # Une commande n'est pas utilisable sur un serveur
     #   await ctx.send(get_lang(str(ctx.guild.id), "CmdCheckError"))

    #if isinstance(error, DebugCheckError): # Le mode global debug n'est pas activé sur le bot
     #   await ctx.send(get_lang(str(ctx.guild.id), "Debug_Check"))

    #if isinstance(error, RuntimeError):
     #   pass

    #print(error)

# # # Commandes # # #

@client.command()
@cmdcheck("changelog")
async def changelog(ctx, version=""):
    if not version:
        version = get_bot_version()
    changelogs = json.load(open("json/changelogs.json", 'r'))
    c_f = afs.afs_memory("db.afs")
    c = c_f.j_load
    #c = json.load(open("json/serverconfig.json", 'r'))

    embed = discord.Embed(colour=ctx.author.top_role.colour.value)
    embed.set_author(name=f"Changelog Stellarium {version}")
    embed.set_thumbnail(url=client.get_user(get_bot_id()).avatar_url) #l'id est celle du bot

    cl = changelogs[version][c["serverconfig"][str(ctx.guild.id)]["lang"]]
    embed.add_field(name="+", value=cl["+"], inline=False)
    embed.add_field(name="-", value=cl["-"], inline=False)

    await ctx.send(embed=embed)

for cmd in cmds:
    client.load_extension(f"cogs.{cmd}")


client.run(open("token.txt", "r").read())
