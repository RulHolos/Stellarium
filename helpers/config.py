import os, json, asyncio, aiohttp, discord
from discord.ext import commands, tasks
from discord.utils import get
from itertools import cycle
from discord import *
from discord.ext.commands import has_permissions

### variables globales ###

debug_value = True
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
    """
    Lists the available commands to toggle.
    
    Returns
    -------
    List[:class:`str`]
        The list of available cmds to be toggled.
    """
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
    conf = json.load(open("json/serverconfig.json", "r"))
    return lang[conf[str(context)]["lang"]][field]

def get_guild_lang(guild):
    """Get the language of the given ctx guild.
    
    Parameters
    ----------
    guild: :class:`discord.Guild`
        The guild id to return the language from
        
    Returns
    -------
    :str:`String Object`
        The language international code."""
    
    with open("json/serverconfig.json", 'r') as f:
        data = json.load(f)
    return data[str(guild)]["lang"]

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
    conf1 = json.load(open("json/serverconfig.json", 'r'))
    guild = message.guild
    if guild:
        return conf1[str(guild.id)]["prefix"]
    else:
        return get_default_prefix()
