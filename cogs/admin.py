import discord
from discord.ext import commands
from discord.embeds import Embed


class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.guild_only()
    async def status(self, ctx, *args):
        embed = discord.Embed(description=f'**О сервере**', colour=discord.Color.dark_red())
        guild = ctx.guild

        embed.add_field(name='Сервер', value=guild.name, inline=False)
        embed.add_field(name='Участники', value=guild.member_count)
        embed.add_field(name='Бусты', value=guild.premium_subscription_count)
        embed.set_image(url=guild.icon)

        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Admin(bot))
