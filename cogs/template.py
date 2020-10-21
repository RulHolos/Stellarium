import discord, re, json
from discord import File
from discord.ext import commands
from discord.ext.commands import has_permissions

from cogs.config import get_lang

class template(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    @has_permissions(administrator=True)
    async def create_template(self, ctx, *, name=""):
        """Créer une template des salons de votre serveur (doit être admin)
        Ainsi que les propriété de configuration du serveur"""
        if not name:
            name = ctx.guild.name
        name = name.replace(" ", "_").lower()
        with open(f"templates/{name}.afs", "w") as f:
            f.write("{}")

        with open(f"templates/{name}.afs", "r") as f:
            data = json.load(f)
        g = ctx.guild
        data[name] = {}
        data[name]["Channels"] = {}
        data[name]["Roles"] = {}
        data[name]["Params_guild"] = {}
        # Channels
        for channel in g.channels:
            data[name]["Channels"][channel.name] = {}
            data[name]["Channels"][channel.name]["name"] = channel.name
            data[name]["Channels"][channel.name]["type"] = channel.type
            data[name]["Channels"][channel.name]["position"] = channel.position
            data[name]["Channels"][channel.name]["overwrites"] = {}
            for x, y in channel.overwrites.items():
                if isinstance(x, discord.Member):
                    pass
                else:
                    data[name]["Channels"][channel.name]["overwrites"][x.name] = x.name
                    data[name]["Channels"][channel.name]["overwrites"][f"pair_{x.name}"] = (y.pair()[0].value, y.pair()[1].value)
            if channel.category:
                data[name]["Channels"][channel.name]["category"] = channel.category.name
            else:
                data[name]["Channels"][channel.name]["category"] = None
            if isinstance(channel, discord.TextChannel):
                data[name]["Channels"][channel.name]["topic"] = channel.topic
            if isinstance(channel, discord.VoiceChannel):
                data[name]["Channels"][channel.name]["user_limit"] = channel.user_limit

        # Roles
        for role in g.roles:
            data[name]["Roles"][role.name] = {}
            data[name]["Roles"][role.name]["hoist"] = role.hoist
            data[name]["Roles"][role.name]["position"] = role.position
            data[name]["Roles"][role.name]["mentionable"] = role.mentionable
            data[name]["Roles"][role.name]["permissions_value"] = role.permissions.value
            data[name]["Roles"][role.name]["color"] = role.color.value

        # Paramètres guild
        data[name]["Params_guild"]["description"] = g.description
                
        with open(f"templates/{name}.afs", "w") as f:
            json.dump(data, f, indent=2)
        
        await ctx.send(
            get_lang(str(ctx.guild.id), "template_create_send"),
            file=File(f'templates/{name}.afs')
            )


def setup(client):
    client.add_cog(template(client))
