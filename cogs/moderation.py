import discord, json
from discord.ext import commands
from discord.ext.commands import has_permissions
from discord.utils import get

class moderation(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.lang = json.load(open("json/lang.json", 'r'))
        self.conf = json.load(open("json/serverconfig.json", 'r'))

    def get_lang(self, context, field):
        """ contexte doit toujours être la valeur id de la guild """
        return self.lang[self.conf[str(context)]["lang"]][field]

    @commands.command()
    @has_permissions(ban_members=True)
    async def ban(self, ctx, user: discord.Member = None, *args):
        if user:
            if user.bot:
                await ctx.send(self.get_lang(ctx.guild.id, "banUserIsBot"))
            else:
                try:
                    await ctx.guild.ban(user, reason=' '.join(args), delete_message_days=0)
                    await ctx.send(self.get_lang(ctx.guild.id, "userBanned"))
                except discord.Forbidden:
                    await ctx.send(self.get_lang(ctx.guild.id, "banError_01"))
                except discord.HTTPException:
                    await ctx.send(self.get_lang(ctx.guild.id, "UnexpectedError"))
        else:
            await ctx.send(self.get_lang(ctx.guild.id, "MentionUser"))

    @commands.command()
    @has_permissions(kick_members=True)
    async def kick(self, ctx, user: discord.Member = None, *args):
        if user:
            if user.bot:
                await ctx.send(self.get_lang(ctx.guild.id, "kickIsBot"))
            else:
                try:
                    await ctx.guild.kick(user, reason=' '.join(args))
                    await ctx.send(self.get_lang(ctx.guild.id, "userKicked"))
                except discord.Forbidden:
                    await ctx.send(self.get_lang(ctx.guild.id, "kickError_01"))
                except discord.HTTPException:
                    await ctx.send(self.get_lang(ctx.guild.id, "UnexpectedError"))
        else:
            await ctx.send(self.get_lang(ctx.guild.id, "MentionUser"))


def setup(client):
    client.add_cog(moderation(client))
