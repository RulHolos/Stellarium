import discord, json, secrets, random, re
from discord.ext import commands

class roll(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=["roll"])
    async def r(self, ctx, *args):
        try:
            value = ''.join(args)

            valueAvant = value[:value.find('d')]
            valueApres = value[value.find('d'):].strip('d')

            listJet = []
            for jets in range(0, int(valueAvant)):
                jet = random.randint(1, int(valueApres))
                listJet.append(jet)

            listeFinale = ' - '.join(str(jet) for jet in listJet)
            await ctx.send(f'```{listeFinale}```')
        except Exception as error:
            await ctx.send(get_lang("roll"))



def setup(client):
    client.add_cog(roll(client))
