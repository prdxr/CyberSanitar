import discord
from discord.ext import commands
from discord.embeds import Embed
from settings import ADMIN_ROLE_ID, MODERATOR_ROLE_ID


def check_admin():
    def predicate(ctx):
        return commands.check_any(commands.is_owner(), commands.has_role(ADMIN_ROLE_ID))
    print(predicate(None))
    return commands.check(predicate)


def check_mod():
    def predicate(ctx):
        return commands.check_any(commands.is_owner(),
                                  commands.has_role(ADMIN_ROLE_ID),
                                  commands.has_role(MODERATOR_ROLE_ID))
    return commands.check(predicate)


class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.guild_only()
    @check_admin()
    @commands.has_permissions(administrator=True)
    async def status(self, ctx, *args):
        embed = discord.Embed(description=f'**О сервере**', colour=discord.Color.dark_red())
        guild = ctx.guild

        embed.add_field(name='Сервер', value=guild.name, inline=False)
        embed.add_field(name='Участники', value=guild.member_count)
        embed.add_field(name='Бусты', value=guild.premium_subscription_count)
        embed.set_image(url=guild.icon)

        await ctx.send(embed=embed)

    @commands.command()
    @commands.guild_only()
    @check_admin()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, user: discord.User = None, reason: str = "No reason given", **kwargs):
        if not user:
            raise commands.BadArgument()
        else:
            await discord.Guild.ban(ctx.guild, user, reason=reason, **kwargs)

    @commands.command()
    @commands.guild_only()
    @check_admin()
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, user: discord.User = None, reason: str = "No reason given", **kwargs):
        if not user:
            raise commands.BadArgument()
        elif not await discord.Guild.fetch_ban(ctx.guild, user):
            raise commands.MemberNotFound(user.name)
        else:
            await discord.Guild.unban(ctx.guild, user, reason=reason)

    @commands.command()
    @commands.guild_only()
    @check_mod()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, user: discord.User = None, reason: str = "No reason given", **kwargs):
        if not user:
            raise commands.BadArgument()
        else:
            await discord.Guild.kick(ctx.guild, user, reason=reason)


async def setup(bot):
    await bot.add_cog(Admin(bot))
