import discord
from requests import get
from discord.ext import commands
import logging
import random
from youtube_dl import YoutubeDL
from collections import deque
import asyncio



class YLBotClient(discord.Client):
    async def on_ready(self):
        print(f'{self.user} has connected to Discord!')
        for guild in self.guilds:
            print(
                f'{self.user} подключились к чату:\n'
                f'{guild.name}(id: {guild.id})')

    async def on_member_join(self, member):
        await member.create_dm()
        await member.dm_channel.send(
            f'Привет, {member.name}!'
        )

    async def on_message(self, message):
        if message.author == self.user:
            return
        if "привет" in message.content.lower():
            await message.channel.send("И тебе привет")
        else:
            await message.channel.send("Спасибо за сообщение")


class DJ_func(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.ffmpeg_format = {
            "before_options": "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5",
            "options": "-vn"}
        self.ydl_format = {'format': 'worstaudio/best',
                           'noplaylist': 'True', 'simulate': 'True', 'preferredquality': '192',
                           'preferredcodec': 'mp3', 'key': 'FFmpegExtractAudio'}
        global vc
        self.playlist = deque()
        self.cnt = 0
        vc = None

    @commands.command(name='roll')
    async def my_randint(self, ctx, min_int, max_int):
        num = random.randint(int(min_int), int(max_int))
        await ctx.send(num)

    async def start_playing(self, ctx):
        global vc
        while self.playlist:
            query = self.playlist[0]
            await ctx.send(f"**🎵 Searching 🔎 **`{query}`")
            with YoutubeDL(self.ydl_format) as ydl:
                try:
                    get(query)
                except:
                    URL = ydl.extract_info(f"ytsearch:{query}", download=False)['entries'][0]
                else:
                    URL = ydl.extract_info(query, download=False)
            print(URL)
            duration = URL['duration']
            await ctx.send(f"**Playing 🎶 **`{URL['title']}`")
            URL = URL['formats'][0]['url']
            try:
                vc.play(discord.FFmpegPCMAudio(source=URL, **self.ffmpeg_format))
                await asyncio.sleep(duration)
            except:
                pass
            self.playlist.popleft()

    @commands.command(name="join")
    async def joi(self, ctx):
        global vc
        if ctx.author.voice is None:
            await ctx.send("Вы должны находится в голосовом канале")
        self.channel = ctx.author.voice.channel
        if vc is None:
            vc = await self.channel.connect()
        else:
            vc = await vc.move_to(self.channel)
        await ctx.send(f":thumbsup: **Joined** {self.channel}")

    @commands.command(name="p")
    async def play(self, ctx, *query):
        global vc
        query = " ".join(query)
        if vc is None:
            await self.joi(ctx)
        if not self.playlist:
            self.playlist.append(query)
            await self.start_playing(ctx)
        else:
            self.playlist.append(query)

    @commands.command(name="stop")
    async def stop(self, ctx):
        global vc
        if vc.is_playing():
            if "DJ" in ctx.author.roles:
                vc.stop()
            else:
                await ctx.send("У вас нет для этого необходимой роли")
        else:
            await ctx.send("Бот и так отдыхает")

    @commands.command(name="s")
    async def skip(self, ctx):
        global vc
        if vc.is_playing:
            if self.channel == ctx.author.voice.channel:
                self.need = len(ctx.author.voice.channel.members)
                self.cnt += 1
                await ctx.send(f"skip vote: {self.cnt}/{self.need - 1}")
                if self.cnt + 1 >= self.need:
                    self.cnt = 0
                    vc.stop()
                    await ctx.send("**⏩ Skipped 👍**")
            else:
                await ctx.send("Вы должны находится в нужном голосовом канале")
        else:
            await ctx.send("Бот не играет")

    @commands.command(name="ds")
    async def disconnect(self, ctx):
        global vc
        await vc.disconnect()


def main():
    logger = logging.getLogger('discord')
    logger.setLevel(logging.DEBUG)
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
    logger.addHandler(handler)
    intents = discord.Intents.default()
    intents.members = True
    with open('token.txt', 'r') as file:
        TOKEN = file.readlines()[0]

    bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())
    bot.add_cog(DJ_func(bot))
    bot.run(TOKEN)

    client = YLBotClient(intents=intents)
    client.run(TOKEN)


if __name__ == '__main__':
    main()
