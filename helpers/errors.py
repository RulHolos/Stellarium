import discord
from discord.ext import commands
from discord import *

class StellariumError(commands.CommandError):
    """Base error of Stellarium.

    All Stellarium Exceptions must be subclasses of this class.

    This Exception must never be raised directly.
    ---------------------------------------------
    
    Subclass of :exc:`commands.CommandError`
    """
    pass

class CmdCheckError(StellariumError):
    """Exception raised by cmdcheck() custom check.
    
    Subclass of :exc:`StellariumError`
    """
    pass

class DebugCheckError(StellariumError):
    """Exception raised by debugcheck() custom check.
    
    Subclass of :exc:`StellariumError`
    """
    pass