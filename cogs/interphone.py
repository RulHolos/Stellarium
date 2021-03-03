import discord, json, secrets, random, re, requests
from discord.ext import commands

from helpers.config import get_lang
from helpers.checks import cmdcheck
import helpers.afs_memory as afs

class interphone(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.connectes = []
        self.conn_pairs = []


    @commands.command()
    @cmdcheck("phone")
    async def interphone(self, ctx):
        if ctx.guild in self.connectes:
            await ctx.send(get_lang(ctx.guild.id, "phone_already_connected"))
        else:
            await ctx.send(get_lang(ctx.guild.id, "interphone_dial"))
            c_f = afs.afs_memory("db.afs")
            guildjson = c_f.j_load
            guilds = list(self.client.guilds)
            l = 0
            for guild in guilds:
                if guild.name == ctx.guild.name:
                    guilds.pop(l)
                l = l+1

            found = False
            new_guilds = []
            for guild in guilds:
                if guildjson["serverconfig"][str(guild.id)]["interphone"] == True:
                    if not guild in self.connectes:
                        found = True
                        new_guilds.append(guild)
            if not found:
                await ctx.send(get_lang(ctx.guild.id, "interphone_404"))
            else:
                conn = random.choice(new_guilds)
                conn_act = (conn, ctx.guild)
            
                phone_channels = []
                for guild in conn_act:
                    channels = await guild.fetch_channels()
                    found = False
                    for channel in channels:
                        if channel.name == "stellarium-phone":
                            phone_channels.append(channel)
                            found = True
                    if not found:
                        try:
                            phone_channel = await guild.create_text_channel('stellarium-phone')
                            phone_channels.append(phone_channel)
                        except:
                            await ctx.send("Need manage_channels permissions.")

                await phone_channels[0].send(f'{get_lang(conn_act[0].id, "phone_connected")} {conn_act[1]}')
                await phone_channels[1].send(f'{ctx.message.author.mention}, {get_lang(ctx.guild.id, "interphone_found")} {conn_act[0]}')

                # id de connexions : servers = conn_act, channels = phone_channels
                
                if not [conn_act[0], conn_act[1]] in self.conn_pairs:
                    self.conn_pairs.append([conn_act[0], conn_act[1]])
                else:
                    await ctx.send(get_lang(ctx.guild.id, "phone_already_connected"))
                for i in range(0,2):
                    self.connectes.append(conn_act[i])


    @commands.command()
    @cmdcheck("phone")
    async def phonetoggle(self, ctx):
        c_f = afs.afs_memory("db.afs")
        guildjson = c_f.j_load
        if guildjson["serverconfig"][str(ctx.guild.id)]["interphone"]:
            guildjson["serverconfig"][str(ctx.guild.id)]["interphone"] = False
        else:
            guildjson["serverconfig"][str(ctx.guild.id)]["interphone"] = True
        c_f.write_json_to_afs(c_f.j_load, guildjson)
        await ctx.send(get_lang(ctx.guild.id, "phonetoggle"))

    @commands.command()
    @cmdcheck("phone")
    async def hang_up(self, ctx):
        if not ctx.guild in self.connectes:
            await ctx.send(get_lang(ctx.guild.id, "phone_no_connexion_currently"))
        else:
            for conn in self.conn_pairs:
                if ctx.guild in conn:
                    if conn.index(ctx.guild) == 1:
                        other_server = conn[0]
                    else:
                        other_server = conn[1]
                    c = self.conn_pairs.index(conn)
            self.conn_pairs.pop(c)
            self.connectes.pop(self.connectes.index(ctx.guild))
            self.connectes.pop(self.connectes.index(other_server))
            await ctx.send(f'{get_lang(ctx.guild.id, "phone_hang_up")} {other_server.name}')
            channels = await other_server.fetch_channels()
            for channel in channels:
                if channel.name == "stellarium-phone":
                    await channel.send(f'{get_lang(ctx.guild.id, "phone_hang_up")} {ctx.guild.name}')

    @commands.Cog.listener()
    async def on_message(self, message):
        """ Ecoute des messages de l'interphone """
        pass


def setup(client):
    client.add_cog(interphone(client))
