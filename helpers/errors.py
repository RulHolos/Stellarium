import os, json, asyncio, aiohttp, discord
from discord.ext import commands, tasks
from discord.utils import get
from itertools import cycle
from discord import *
from discord.ext.commands import has_permissions

class CmdCheckError(commands.CommandError):
    """Exception raised by cmdcheck() custom check"""
    pass

class DebugCheckError(commands.CommandError):
    """Exception raised by debugcheck() custom check"""
    pass