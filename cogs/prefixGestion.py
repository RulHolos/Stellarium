import discord, json
from discord.ext import commands
from discord.ext.commands import has_permissions

class prefixGestion(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.lang = json.load(open("json/lang.json", 'r'))
        self.conf = json.load(open("json/serverconfig.json", 'r'))

    def get_lang(self, context, field):
        """ contexte doit toujours être la valeur id de la guild """
        return self.lang[self.conf[str(context)]["lang"]][field]

    @commands.command(aliases=["setprefix", "SetPrefix", "Setprefix"])
    @has_permissions(administrator=True)
    async def setPrefix(self, ctx, prefix=""):
        with open("json/serverconfig.json", 'r') as sConf1: conf1 = json.load(sConf1)

        if len(prefix) > 1:
            await ctx.send(self.get_lang(ctx.guild.id, "BadArgument"))
        else:
            conf1[str(ctx.guild.id)]["prefix"] = prefix or ";"
            with open("json/serverconfig.json", "w") as f:
                json.dump(conf1, f, indent=2)
            await ctx.send(f'{self.get_lang(ctx.guild.id, "PrefixEdited")} `{prefix or ";"}`')


def setup(client):
    client.add_cog(prefixGestion(client))
