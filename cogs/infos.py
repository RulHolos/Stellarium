import discord, json
from discord.ext import commands

from cogs.config import get_lang

class infos(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def userinfo(self, ctx, *, user: discord.Member = None):
        user = user or ctx.author
        guild = str(ctx.guild.id)

        show_roles = ', '.join(
            [f"<@&{x.id}>" for x in sorted(user.roles, key=lambda x: x.position, reverse=True) if x.id != ctx.guild.default_role.id]
        ) if len(user.roles) > 1 else 'None'

        embed = discord.Embed(colour=user.top_role.colour.value)
        embed.set_thumbnail(url=user.avatar_url)

        embed.add_field(name=get_lang(guild, "username"), value=user, inline=True)
        embed.add_field(name=get_lang(guild, "nickname"), value=user.nick if hasattr(user, "nick") else "None", inline=True)
        embed.add_field(name=get_lang(guild, "UserCreatedAt"), value=user.created_at, inline=True)
        embed.add_field(name=get_lang(guild, "UserJoinAt"), value=user.joined_at, inline=True)

        embed.add_field(
            name="Roles",
            value=show_roles,
            inline=False
        )

        await ctx.send(content=f"Informations de **{user.id}**", embed=embed)

    @commands.command()
    async def serverinfo(self, ctx):
        conf = json.load(open("json/serverconfig.json", 'r'))
        user = ctx.author
        guild = ctx.guild
        gId = str(ctx.guild.id)

        embed = discord.Embed(colour=user.top_role.colour.value)
        embed.set_thumbnail(url=guild.icon_url)
        embed.set_author(name=guild.name)

        embed.add_field(name=get_lang(gId, "Creator"), value=self.client.get_user(conf[gId]["creator"]).name, inline=False)
        embed.add_field(name=get_lang(gId, "Members"), value=len(guild.members), inline=True)
        embed.add_field(name="Roles", value=len(guild.roles), inline=True)

        await ctx.send(embed=embed)

    @commands.command()
    async def infos(self, ctx):
        gId = ctx.guild.id
        bot = self.client.get_user(746348869574459472)

        embed = discord.Embed(colour=ctx.author.top_role.colour.value)
        embed.set_thumbnail(url=bot.avatar_url)
        embed.set_author(name="Stellarium")

        embed.add_field(name="Par/By", value="Guild : Ruby For Aneha", inline=False)
        embed.add_field(name=get_lang(gId, "UserCreatedAt"), value=bot.created_at, inline=False)

        await ctx.send(embed=embed)

def setup(client):
    client.add_cog(infos(client))
