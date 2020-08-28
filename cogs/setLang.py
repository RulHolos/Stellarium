import discord, json
from discord.ext import commands

class setLang(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def setLang(self, ctx, *, language=""):
        with open("json/lang.json", 'r') as langF:
            lang = json.load(langF)
        with open("json/serverconfig.json", 'r') as sConf:
            conf = json.load(sConf)

        guild = f"{ctx.guild.id}"
        error = False

        if language:
            if (language != "en" and language != "fr"):
                await ctx.send(f'{lang[conf[guild]["lang"]]["InvalidLanguage"]} : `{language}`')
                error = True
        if not error:
            conf[guild]["lang"] = language or "en"
            with open('json/serverconfig.json', 'w') as sConfSave:
                json.dump(conf, sConfSave, indent=2)
            await ctx.send(f'{lang[conf[guild]["lang"]]["SetLangSuccess"]} `{language or "en"}`!')

def setup(client):
    client.add_cog(setLang(client))
