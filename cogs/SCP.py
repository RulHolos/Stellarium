import discord, json, secrets, random, re
from discord.ext import commands

from cogs.config import get_lang

class SCP(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=["scp"])
    async def SCP(self, ctx, scp=""):
        if scp:
            scpIn = scp.upper()
            scpOut = re.findall("[1234567890]", scpIn)
            if scpOut:
                await ctx.send(f"http://www.scpwiki.com/scp-{''.join(scpOut)}")
            else: await ctx.send(get_lang(str(ctx.guild.id), "BadArgument"))
        else: await ctx.send(get_lang(ctx.guild.id, "argumentNeeded"))


def setup(client):
    client.add_cog(SCP(client))
