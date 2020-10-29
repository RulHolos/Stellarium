import os, json, asyncio, aiohttp, discord
from discord.ext import commands, tasks
from discord.utils import get
from itertools import cycle
from discord import *
from discord.ext.commands import has_permissions

from .errors import CmdCheckError, DebugCheckError

debug_value = True

def cmdcheck(cmd:str):
    def predicate_cmd(ctx):
        with open("json/serverconfig.json", 'r') as f:
            conf = json.load(f)
            # Si la commande voulue est présente dans le dict, alors on renvois true
        if cmd.lower() in conf[str(ctx.guild.id)]["cmds"]:
            raise CmdCheckError()
            #return False
        else:
            return True
    return commands.check(predicate_cmd)

def debugcheck():
    def predicate_debug(ctx):
        if not debug_value:
            raise DebugCheckError
        else:
            return True
    return commands.check(predicate_debug)