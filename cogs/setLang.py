import discord, json
from discord.ext import commands

from cogs.config import get_lang

class setLang(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def setLang(self, ctx, *, language=""):
        conf = json.load(open("json/serverconfig.json", 'r'))

        guild = str(ctx.guild.id)
        error = False

        if language:
            if (language != "en" and language != "fr"):
                await ctx.send(f'{get_lang(guild, "InvalidLanguage")} : `{language}`')
                error = True
        if not error:
            conf[guild]["lang"] = language or "en"
            with open('json/serverconfig.json', 'w') as sConfSave:
                json.dump(conf, sConfSave, indent=2)
            await ctx.send(f'{get_lang(guild, "SetLangSuccess")} `{language or "en"}`!')

def setup(client):
    client.add_cog(setLang(client))
