import discord, json, argparse, re
from discord.ext import commands
from discord.ext.commands import has_permissions
from discord.utils import get

from cogs.config import get_lang

class moderation(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    @has_permissions(ban_members=True)
    async def ban(self, ctx, user: discord.Member = None, *args):
        if user:
            if user.bot:
                await ctx.send(get_lang(ctx.guild.id, "banUserIsBot"))
            else:
                try:
                    await ctx.guild.ban(user, reason=' '.join(args), delete_message_days=0)
                    await ctx.send(get_lang(ctx.guild.id, "userBanned"))
                except discord.Forbidden:
                    await ctx.send(get_lang(ctx.guild.id, "banError_01"))
                except discord.HTTPException:
                    await ctx.send(get_lang(ctx.guild.id, "UnexpectedError"))
        else:
            await ctx.send(get_lang(ctx.guild.id, "MentionUser"))

    @commands.command()
    @has_permissions(kick_members=True)
    async def kick(self, ctx, user: discord.Member = None, *args):
        if user:
            if user.bot:
                await ctx.send(get_lang(ctx.guild.id, "kickIsBot"))
            else:
                try:
                    await ctx.guild.kick(user, reason=' '.join(args))
                    await ctx.send(get_lang(ctx.guild.id, "userKicked"))
                except discord.Forbidden:
                    await ctx.send(get_lang(ctx.guild.id, "kickError_01"))
                except discord.HTTPException:
                    await ctx.send(get_lang(ctx.guild.id, "UnexpectedError"))
        else:
            await ctx.send(get_lang(ctx.guild.id, "MentionUser"))


def setup(client):
    client.add_cog(moderation(client))
