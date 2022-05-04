import discord
from discord.ext import commands
import logging
import random
import youtube_dl

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

    @commands.command(name="play")
    async def play(self, ctx, query):


bot = commands.Bot(command_prefix='!', intents=intents)
bot.add_cog(DJ_func(bot))
bot.run(TOKEN)

client = YLBotClient(intents=intents)
client.run(TOKEN)
