import discord, re
from discord.ext import commands

from helpers.config import get_lang, get_bot_owner

class broadcast(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=["@b"])
    async def broadcast(self, ctx, *, msg=""):
        """Warning : This command serve the purpose of a multi-guild broadcast system.
        Any messages sent through this command will be sent to every guild the bot is on.
        This command is only usable by the bot's owner with the id set in config.py in the get_bot_owner() function"""

        if ctx.message.author.id != get_bot_owner():
            raise commands.CheckFailure
        else:
            for servs in list(self.client.guilds):
                get_serv = self.client.get_guild(servs.id)
                found = False
                for channels in list(get_serv.text_channels):
                    if not found:
                        try:
                            chan = self.client.get_channel(channels.id)
                            await chan.send(f"""***[GLOBAL BROADCAST]***
*Notice from the Stellarium team :*
```{msg}```""")
                            print(f"@b sent to {chan.name} in {servs.name}")
                            found = True
                        except discord.Forbidden:
                            pass


def setup(client):
    client.add_cog(broadcast(client))
