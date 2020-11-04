import os, json, asyncio, aiohttp, discord
from discord.ext import commands, tasks
from discord.utils import get
from itertools import cycle
from discord import *
from discord.ext.commands import has_permissions

from .errors import CmdCheckError, DebugCheckError
from .config import debug_value

def cmdcheck(cmd:str):
    """
    Checking the state of a cmd in the ctx server
    
    Parameters
    ----------
    cmd: :class:`str`
        the name of the command to check.

    Returns
    -------
    :bool:`True`
        The command is available.

    Raises
    ------
    helpers.error.CmdCheckError
        The check fails.
    """
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
    """Checking the state of the global debug mode.

    Returns
    -------
    :bool:`True`
        The debug mod is bot-wide active.
    
    Raises
    ------
    helpers.error.DebugCheckError
        The check fails."""
    def predicate_debug(ctx):
        if not debug_value:
            raise DebugCheckError
        else:
            return True
    return commands.check(predicate_debug)