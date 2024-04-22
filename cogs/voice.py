import asyncio
import os.path

import youtube_dl
import yt_dlp
import discord
import pyttsx3

from discord.ext import commands

from settings import DATA_DIR, ROOT_DIR, CREATE_VOICE_ID, VOICE_CAT_ID


class Voice(commands.Cog):
    active_voice: discord.VoiceClient = None
    ytdl = None
    ffmpeg_options = None
    engine = None
    voices = None

    def __init__(self, bot):
        self.bot = bot
        self.ffmpeg_options = {'options': '-vn'}

        self.engine = pyttsx3.init()

        yt_dl_options = {"format": "bestaudio/best"}
        self.ytdl = yt_dlp.YoutubeDL(yt_dl_options)

        self.voices = self.engine.getProperty('voices')
        for voice in self.voices:
            # debug voice list
            print('=======')
            print('name: %s' % voice.name)
            print('ID: %s' % voice.id)
            print('lang: %s' % voice.languages)
            print('sex: %s' % voice.gender)
            print('age: %s' % voice.age)
        self.change_lang('ru')

    @commands.command()
    @commands.guild_only()
    async def join(self, ctx):
        voice_state = ctx.author.voice
        if voice_state is None:
            await ctx.send('Вы не подключены к голосовому каналу. Зайдите в любой голосовой канал и попробуйте снова')
            return False

        await ctx.send(f'Зашёл в {voice_state.channel.name}')
        self.active_voice = await voice_state.channel.connect()
        return True

    @commands.command()
    @commands.guild_only()
    async def leave(self, ctx):
        if self.active_voice is None:
            await ctx.send('Я и так не подключён к голосовым каналам')
            return

        await ctx.send(f'Вышел из {self.active_voice.channel.name}')
        await self.active_voice.disconnect()
        self.active_voice = None

    @commands.command()
    @commands.guild_only()
    async def play(self, ctx, *, url):
        if self.active_voice is None:
            if not await self.join(ctx):
                return

        if self.active_voice.is_playing():
            await ctx.send('Я уже играю песню. Очереди пока нет =)')
            return

        try:
            ffmpeg_options = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
                              'options': '-vn -filter:a "volume=0.25"'}

            loop = asyncio.get_event_loop()
            data = await loop.run_in_executor(None, lambda: self.ytdl.extract_info(url, download=False))

            song = data['url']
            player = discord.FFmpegOpusAudio(song, **ffmpeg_options)

            self.active_voice.play(player)
        except Exception as e:
            print(e)

    @commands.command()
    @commands.guild_only()
    async def pause(self, ctx):
        if not self.active_voice.is_playing():
            await ctx.send('Музыки и так нет.')
            return

        self.active_voice.pause()
        await ctx.send('Поставил на паузу.')

    @commands.command()
    @commands.guild_only()
    async def resume(self, ctx):
        if self.active_voice.is_playing():
            await ctx.send('Музыка уже идёт.')
            return
        if self.active_voice.is_paused():
            self.active_voice.resume()
        await ctx.send('Снял с паузы.')

    @commands.command()
    @commands.guild_only()
    async def tts(self, ctx, *, message: str):
        if self.active_voice is None:
            if not await self.join(ctx):
                return
        message = f'{ctx.message.author} говорит: {message}'
        self.execute_tts(message)

        print(f'now playing TTS by {ctx.message.author}')
        self.active_voice.play(discord.FFmpegPCMAudio(os.path.join(DATA_DIR, "tts.mp3")))

    @commands.Cog.listener()
    async def on_voice_state_update(self, member: discord.Member, before, after):
        if member.bot:
            return

        await self.purge_garbage_pvc(member.guild)

        if after.channel is None:
            print(f'member {member} has left. Stopping create PVC')
            return

        if after.channel.id == CREATE_VOICE_ID:
            print(f'user {member.name} connected to {after.channel.name}')
            voice_category = member.guild.get_channel(VOICE_CAT_ID)
            pvc_name = f'「⌛」 канал {member.name}'
            pvc = await member.guild.create_voice_channel(pvc_name, category=voice_category)
            await member.move_to(pvc)

    async def purge_garbage_pvc(self, guild: discord.Guild):
        channels = guild.voice_channels

        for channel in channels:
            if channel.name.startswith('「⌛」') and len(channel.members) == 0:
                print(f'deleting channel {channel.name}')
                await channel.delete()

    def change_lang(self, lang):
        if lang == 'ru':
            print('setting to ru')
            for voice in self.voices:
                if voice.name == 'Artemiy':
                    self.engine.setProperty('voice', voice.id)
        elif lang == 'en':
            print('setting to en')
            for voice in self.voices:
                if voice.name == 'Alan':
                    self.engine.setProperty('voice', voice.id)

        self.engine.setProperty('rate', 150)     # setting up new voice rate

    def execute_tts(self, text, filename='tts'):
        print(f'TEXT: {text}, FILENAME: {filename}')
        self.engine.save_to_file(text, DATA_DIR + f'/{filename}.mp3')
        self.engine.runAndWait()


async def setup(bot):
    await bot.add_cog(Voice(bot))
