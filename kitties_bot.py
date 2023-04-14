import discord
import logging
import requests
from io import BytesIO

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)
TOKEN = "MTA5NjAzNjM5MTEyNjgyNzA3OA.GJdhAK.XrOGIFO7RemGjLJY5Rhjqf1N7j0FPRhr1Cnspo"


class YLBotClient(discord.Client):
    async def on_ready(self):
        logger.info(f'{self.user} has connected to Discord!')
        for guild in self.guilds:
            logger.info(
                f'{self.user} подключился к чату и готов показать случайного котика (или пёсика!)\n'
                f'{guild.name}(id: {guild.id})')

    async def on_message(self, message):
        if message.author == self.user:
            return
        if "кот" in message.content.lower():
            picture = discord.File(BytesIO(requests.get('https://api.thecatapi.com/v1/images/search').content))
            await message.channel.send(file=picture)
        elif "собак" in message.content.lower():
            picture = discord.File(BytesIO(requests.get('https://dog.ceo/api/breeds/image/random').content))
            await message.channel.send(file=picture)
        else:
            await message.channel.send("Котики или собачки?")


intents = discord.Intents.default()
intents.members = True
intents.message_content = True
client = YLBotClient(intents=intents)
client.run(TOKEN)
