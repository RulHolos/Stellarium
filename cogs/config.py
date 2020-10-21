import os, json, asyncio, aiohttp

### variables globales ###

debug_value = True
versionBot = "v0.0.4"
default_prefix = ";"

### Fonctions return ###

def debug():
    return debug_value

def get_bot_version():
    return versionBot

def get_default_prefix():
    return default_prefix

def get_bot_owner():
    return 130313080545607680 # Chance this value to the bot's owner discord id.

### Fonctions helpers ###

def get_lang(context, field):
    lang = json.load(open("json/lang.json", "r"))
    conf = json.load(open("json/serverconfig.json", "r"))
    return lang[conf[str(context)]["lang"]][field]

async def get_prefix(client, message):
    conf1 = json.load(open("json/serverconfig.json", 'r'))
    guild = message.guild
    if guild:
        return conf1[str(guild.id)]["prefix"]
    else:
        return get_default_prefix()
