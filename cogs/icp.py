from discord.ext import commands, ipc
import json

class IpcRoutes(commands.Cog):
    def __init__(self, client):
        self.client = client

    @ipc.server.route()
    async def test(self):
        pass

def setup(client):
    client.add_cog(IpcRoutes(client))