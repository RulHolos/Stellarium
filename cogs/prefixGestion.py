import discord, json
from discord.ext import commands
from discord.ext.commands import has_permissions

from helpers.config import get_lang

class prefixGestion(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=["setprefix", "SetPrefix", "Setprefix"])
    @has_permissions(administrator=True)
    async def setPrefix(self, ctx, prefix=""):
        conf = json.load(open("json/serverconfig.json", 'r'))

        if len(prefix) > 1:
            await ctx.send(get_lang(ctx.guild.id, "BadArgument"))
        else:
            conf[str(ctx.guild.id)]["prefix"] = prefix or ";"
            with open("json/serverconfig.json", "w") as f:
                json.dump(conf, f, indent=2)
            await ctx.send(f'{get_lang(ctx.guild.id, "PrefixEdited")} `{prefix or ";"}`')


def setup(client):
    client.add_cog(prefixGestion(client))
