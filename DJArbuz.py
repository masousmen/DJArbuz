import discord
from discord.utils import get
from discord.ext import commands
import logging
import random
from youtube_dl import YoutubeDL
import asyncio

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)
intents = discord.Intents.default()
intents.members = True

TOKEN = "OTcwOTYwNzQ0NTY2ODkwNTQ2.YnDjqQ.G09oxVgdM_ofZW9vNv_bAy8erII"


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

    @commands.command(name='roll')
    async def my_randint(self, ctx, min_int, max_int):
        num = random.randint(int(min_int), int(max_int))
        await ctx.send(num)

    @commands.command(name="p")
    async def play(self, ctx, query):
        global voice
        channel = ctx.message.author.voice.channel
        voice = get(self.bot.voice_clients, guild=ctx.guild)
        if voice and voice.is_connected():
            await voice.move_to(channel)
        else:
            await channel.connect(reconnect=True, timeout=300)
        await ctx.send("YES")

        with YoutubeDL({'outtmpl': '%(id)s.%(ext)s'}) as ydl:
            result = ydl.extract_info(
                query,
                download=False  # We just want to extract the info
            )

        if 'entries' in result:
            # Can be a playlist or a list of videos
            info = result['entries'][0]
        else:
            # Just a video
            info = result

        print(info)
        video_url = info['url']
        print(video_url)
        await ctx.send(URL)
        voice.play(discord.FFmpegPCMAudio(source=URL, executable="ffmpeg.exe"),
                   **{'format': 'worstaudio/best',
                      'noplaylist': 'True', 'simulate': 'True', 'preferredquality': '192', 'preferredcodec': 'mp3',
                      'key': 'FFmpegExtractAudio'})

        while voice.is_playing():
            await asyncio.sleep(1)
        if not voice.is_paused():
            await voice.disconnect()


bot = commands.Bot(command_prefix='!', intents=intents)
bot.add_cog(DJ_func(bot))
bot.run(TOKEN)

client = YLBotClient(intents=intents)
client.run(TOKEN)
