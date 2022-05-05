import discord
from requests import get
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

    @commands.command(name="join")
    async def joi(self, ctx):
        if ctx.author.voice is None:
            await ctx.send("Вы должны находится в голосовом канале")
        channel = ctx.author.voice.channel
        vc = ctx.voice_client
        if vc is None:
            await channel.connect()
        else:
            await vc.move_to(channel)

    @commands.command(name="p")
    async def play(self, ctx, *query):
        global vc
        query = " ".join(query)
        ffmpeg_format = {
            "before_options": "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5",
            "options": "-vn"}
        ydl_format = {'format': 'worstaudio/best',
                      'noplaylist': 'True', 'simulate': 'True', 'preferredquality': '192',
                      'preferredcodec': 'mp3', 'key': 'FFmpegExtractAudio'}
        if ctx.author.voice is None:
            await ctx.send("Вы должны находится в голосовом канале")
        channel = ctx.author.voice.channel
        vc = ctx.voice_client
        if vc is None:
            await channel.connect()
        else:
            await vc.move_to(channel)
        vc = ctx.voice_client
        await ctx.send("YES")
        with YoutubeDL(ydl_format) as ydl:
            try:
                get(query)
            except:
                URL = ydl.extract_info(f"ytsearch:{query}", download=False)['entries'][0]
            else:
                URL = ydl.extract_info(query, download=False)
        print(URL)
        URL = URL['formats'][0]['url']
        vc.play(discord.FFmpegPCMAudio(source=URL, **ffmpeg_format))


bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())
bot.add_cog(DJ_func(bot))
bot.run(TOKEN)

client = YLBotClient(intents=intents)
client.run(TOKEN)
