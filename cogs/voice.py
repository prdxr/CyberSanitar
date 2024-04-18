from discord.ext import commands


class Voice(commands.Cog):
    active_voice = None

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.guild_only()
    async def join(self, ctx):
        voice_state = ctx.author.voice
        if voice_state is None:
            await ctx.send('Вы не подключены к голосовому каналу. Зайдите в любой голосовой канал и попробуйте снова')
            return

        await ctx.send(f'Зашёл в {voice_state.channel.name}')
        self.active_voice = await voice_state.channel.connect()

    @commands.command()
    @commands.guild_only()
    async def leave(self, ctx):
        if self.active_voice is None:
            await ctx.send('Я и так не подключён к голосовым каналам')
            return

        await ctx.send(f'Вышел из {self.active_voice.channel.name}')
        await self.active_voice.disconnect()
        self.active_voice = None


async def setup(bot):
    await bot.add_cog(Voice(bot))
