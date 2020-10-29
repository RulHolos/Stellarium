import discord, json, secrets, random, re, uuid
from discord.ext import commands

from helpers.checks import cmdcheck

class danbooru(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    @cmdcheck("danbooru")
    async def danbooru(self, ctx, *, tag=""):
        from pybooru import Danbooru
        dan = Danbooru('danbooru')
        found = False
        while not found:
            try:
                posts = dan.post_list(limit=2, random=True, tags=str(tag or "Hololive"))
                lst = []
                for post in posts:
                    lst.append(post['file_url'])

                found = True
                await ctx.send(str(lst[0]))
            except:
                pass

def setup(client):
    client.add_cog(danbooru(client))
