import discord, re
from discord.ext import commands

from helpers.config import get_lang
from helpers.checks import cmdcheck

class internetThings(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=["nautiljon", "Anime"])
    @cmdcheck("anime")
    async def anime(self, ctx, *, anime=""):
        if anime:
            anime = anime.split()
            await ctx.send(f"https://www.nautiljon.com/animes/{'+'.join(anime)}.html")
        else: await ctx.send(get_lang(ctx.guild.id, "argumentNeeded"))

    @commands.command(aliases=["scp"])
    @cmdcheck("scp")
    async def SCP(self, ctx, scp=""):
        if scp:
            scpIn = scp.upper()
            scpOut = re.findall("[0-9]", scpIn)
            if scpOut:
                await ctx.send(f"http://www.scpwiki.com/scp-{''.join(scpOut)}")
            else: await ctx.send(get_lang(str(ctx.guild.id), "BadArgument"))
        else: await ctx.send(get_lang(ctx.guild.id, "argumentNeeded"))


def setup(client):
    client.add_cog(internetThings(client))
