from discord.ext import commands


class General(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        print(f'User {ctx.author} raised error: "{error}" in command [{ctx.command}] '
              f'at {ctx.message.created_at.strftime("%d/%m/%Y %H:%M:%S")}')
        await ctx.send(f'**Ошибка во время выполнения команды**: ```{error}```')

    @commands.command()
    async def hello(self, ctx):
        await ctx.send(f'Hello {ctx.author.mention}')

    @commands.command()
    @commands.guild_only()
    async def invite(self, ctx):
        link = await ctx.channel.create_invite(max_uses=1, max_age=3600)
        await ctx.send(f'Вот одноразовое приглашение. Оно действует один час.\n{link}')


async def setup(bot):
    await bot.add_cog(General(bot))
