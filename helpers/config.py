import os, json, asyncio, aiohttp, discord, configparser, random
from discord.ext import commands, tasks
from discord.utils import get
from itertools import cycle
from discord import *
from discord.ext.commands import has_permissions
from datetime import datetime
from .afs_memory import afs_memory as afs

con = configparser.ConfigParser(converters={'list': lambda x: [i.strip() for i in x.split(',')]}, allow_no_value=True)
con.read("config.ini")

### variables globales ###

debug_value = con["variables"].getboolean('debug_value')
versionBot = con["variables"]["versionBot"]
default_prefix = con["variables"]["default_prefix"]
Togglable_cmds = con["variables"].getlist("Togglable_cmds")
owner_id = int(con["variables"]["owner_id"])
bot_id = int(con["variables"]["owner_id"])

### Fonctions return ###

def get_bot_version():
    return versionBot

def get_default_prefix():
    return default_prefix

def get_bot_owner():
    return owner_id

def get_bot_id():
    return bot_id

def get_t_cmd():
    return Togglable_cmds

### Fonctions helpers ###

def get_lang(context, field):
    """Get a string based on the language of the ctx server.

    Parameters
    ----------
    context: :class:`str` or :class:`int`
        The ctx guild. Normally, ctx.guild.id.
    field: :class:`str`
        The name of the field in :file:`json/lang.json`
    """
    lang = json.load(open("json/lang.json", "r"))
    #conf = json.load(open("json/serverconfig.json", "r"))
    c_f = afs("db.afs")
    conf = c_f.j_load
    return lang[conf["serverconfig"][str(context)]["lang"]][field]

def get_guild_lang(guild):
    """Get the language of the given ctx guild.

    Parameters
    ----------
    guild: :class:`discord.Guild`
        The guild id to return the language from

    Returns
    -------
    :str:`String Object`
        The language international code. (en/fr)"""

    #with open("json/serverconfig.json", 'r') as f:
    #    data = json.load(f)
    c_f = afs("db.afs")
    data = c_f.j_load
    return data["serverconfig"][str(guild)]["lang"]

async def get_prefix(client, message):
    """Get the guild's prefix

    Parameters
    ----------
    client: :class:`discord.client`
        ...Needed. Apparently.
    message:
        The message to get the ctx guild from.

    Returns
    -------
    String
        The guild's cmd prefix.
    """
    #conf1 = json.load(open("json/serverconfig.json", 'r'))
    c_f = afs("db.afs")
    conf1 = c_f.j_load
    guild = message.guild
    if guild:
        return conf1["serverconfig"][str(guild.id)]["prefix"]
    else:
        return get_default_prefix()

def store_activities(data):
    with open("json/activities.json", 'r') as f:
        act = json.load(f)

    data["date"] = datetime.now().strftime('%A %B at %H:%M')
    r = str(random.randint(0, 99999))
    while r in act:
        r = str(random.randint(0, 99999))
    act[r] = data
    with open("json/activities.json", 'w') as f:
        json.dump(act, f, indent=2)
    