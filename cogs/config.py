import os, json, asyncio, aiohttp

debug_value = True

def debug():
    return debug_value

def get_default_prefix():
    return ";"

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
