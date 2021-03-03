import discord, re, json
from discord.ext import commands
from discord.ext.commands import has_permissions

from helpers.config import get_lang, get_t_cmd
from helpers.checks import cmdcheck
import helpers.afs_memory as afs

class ToggleCmd(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=["Togglecmd", "togglecmd"])
    @has_permissions(administrator=True)
    async def ToggleCmd(self, ctx, cmd=""):
        """Activate/Desactivate a given bot cmd in the ctx guild"""
        if cmd:
            if cmd.lower() in get_t_cmd():
                #with open("json/serverconfig.json", 'r') as f:
                #    conf = json.load(f)
                c_f = afs.afs_memory("db.afs")
                conf = c_f.j_load

                if cmd in conf["serverconfig"][str(ctx.guild.id)]["cmds"]:
                    # Retirer la cmd du dict
                    #conf["serverconfig"][str(ctx.guild.id)]["cmds"].pop(cmd)
                    c_f.delete_json_from_afs(conf, f"serverconfig.{str(ctx.guild.id)}.cmds.{cmd}")
                    #with open("json/serverconfig.json", 'w') as f:
                    #    json.dump(conf, f, indent=2)
                    await ctx.send(get_lang(str(ctx.guild.id), "ToggleCmdUpdated"))

                else:
                    # Ajouter la cmd au dict
                    conf["serverconfig"][str(ctx.guild.id)]["cmds"][cmd] = cmd
                    c_f.write_json_to_afs(c_f.j_load, conf)
                    #with open("json/serverconfig.json", 'w') as f:
                    #    json.dump(conf, f, indent=2)
                    await ctx.send(get_lang(str(ctx.guild.id), "ToggleCmdUpdated"))

            else:
                await ctx.send(get_lang(str(ctx.guild.id), "ToggleCmdNotSupported"))
        else:
            await ctx.send(", ".join(get_t_cmd()))

    @commands.command()
    async def nocmd(self, ctx):
        """See the list of non-available cmds on the ctx guild"""
        #with open("json/serverconfig.json", 'r') as f:
        #    conf = json.load(f)
        c_f = afs.afs_memory("db.afs")
        conf = c_f.j_load
        lstcmd = []
        for key, value in conf["serverconfig"][str(ctx.guild.id)]["cmds"].items():
            lstcmd.append(key)
        await ctx.send(", ".join(lstcmd) or "N/A")


def setup(client):
    client.add_cog(ToggleCmd(client))
