import discord, json, secrets, random, re
from discord.ext import commands

from cogs.config import get_lang

class roll(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=["roll", 'R', 'Roll', 'ROLL'])
    async def r(self, ctx, jet=""):
        if jet:
            if jet.upper() == "MOL":
                await ctx.send(f'```{random.randint(1, 60221407600000000000000)}```')
            else:
                try:
                    jet = jet.upper()
                    vAvant = jet[:jet.find('D')]
                    vApres = jet[jet.find('D'):].strip('D')
                    await ctx.send(f'```{" ; ".join(str(jet) for jet in [random.randint(1, int(vApres)) for jets in range(0, int(vAvant or 1))]) or "Wtf ?"}```')
                except Exception as e:
                    raise commands.BadArgument
        else: await ctx.send(get_lang(ctx.guild.id, "roll"))



def setup(client):
    client.add_cog(roll(client))
