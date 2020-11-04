import discord, json, secrets, random, re, requests
from discord.ext import commands

from helpers.config import get_lang
from helpers.checks import cmdcheck

class meteo(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=["météo", "weather"])
    @cmdcheck("meteo")
    async def meteo(self, ctx, *, ville=""):
        try:
            meteo = requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={ville}&appid=1bddba383a9e908290b5482be115a4ca&units=metric")

            weather = json.loads(meteo.text)
            embed = discord.Embed(colour=ctx.author.top_role.colour.value)
            embed.set_author(name=f'{ville}, {weather["sys"]["country"]}')

            embed.add_field(name=get_lang(ctx.guild.id, "general"), value=f'{weather["weather"][0]["description"]}', inline=True)
            embed.add_field(name=get_lang(ctx.guild.id, "temperature"), value=f'{float(weather["main"]["temp"])}°C', inline=True)
            embed.add_field(name=get_lang(ctx.guild.id, "wind"), value=f'{weather["wind"]["speed"]} km/h ; {weather["wind"]["deg"]} deg', inline=True)
            embed.add_field(name=get_lang(ctx.guild.id, "pressure"), value=f'{weather["main"]["pressure"]} hPa', inline=True)

            await ctx.send(embed=embed)
        except KeyError:
            raise commands.BadArgument


def setup(client):
    client.add_cog(meteo(client))
