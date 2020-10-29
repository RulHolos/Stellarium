import os, json, asyncio, aiohttp, discord
from discord.ext import commands, tasks
from discord.utils import get
from itertools import cycle
from discord import *
from discord.ext.commands import has_permissions

### variables globales ###

versionBot = "v0.0.4"
default_prefix = ";"
Togglable_cmds = ["changelog", "scp", "danbooru", "userinfo", "serverinfo", "infos", "meteo", "roll", "guild"]

### Fonctions return ###

def get_bot_version():
    return versionBot

def get_default_prefix():
    return default_prefix

def get_bot_owner():
    return 130313080545607680 # Change this value to the bot's owner discord id.

def get_t_cmd():
    """Returns the list of toggleable cmds (not supported by all cmds)"""
    return Togglable_cmds

### Fonctions helpers ###

def get_lang(context, field):
    """Get the language of a certain field content"""
    lang = json.load(open("json/lang.json", "r"))
    conf = json.load(open("json/serverconfig.json", "r"))
    return lang[conf[str(context)]["lang"]][field]

async def get_prefix(client, message):
    """Get the guild's prefix"""
    conf1 = json.load(open("json/serverconfig.json", 'r'))
    guild = message.guild
    if guild:
        return conf1[str(guild.id)]["prefix"]
    else:
        return get_default_prefix()
