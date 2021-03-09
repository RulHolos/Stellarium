import discord, json
from discord.ext import commands
from discord.ext.commands import has_permissions

from helpers.config import get_lang, store_activities
import helpers.afs_memory as afs

class setLang(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    @has_permissions(administrator=True)
    async def setLang(self, ctx, *, language=""):
        #conf = json.load(open("json/serverconfig.json", 'r'))
        c_f = afs.afs_memory("db.afs")
        conf = c_f.j_load

        guild = str(ctx.guild.id)
        error = False

        if language:
            if (language != "en" and language != "fr"):
                await ctx.send(f'{get_lang(guild, "InvalidLanguage")} : `{language}`')
                error = True
        if not error:
            conf["serverconfig"][guild]["lang"] = language or "en"
            #with open('json/serverconfig.json', 'w') as sConfSave:
            #    json.dump(conf, sConfSave, indent=2)
            c_f.write_json_to_afs(c_f.j_load, conf)
            await ctx.send(f'{get_lang(guild, "SetLangSuccess")} `{language or "en"}`!')

        store_activities({
            "g_name": ctx.guild.name,
            "cmd": "setLang",
            "desc": f"Langue changée pour {language}"
        })

def setup(client):
    client.add_cog(setLang(client))
