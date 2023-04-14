import asyncio
import discord
from discord.ext import commands
import logging

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

intents = discord.Intents.default()
intents.members = True
intents.message_content = True


class TimerBot(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='shutdown')
    async def shutdown(self, ctx):
        await ctx.send("Timer was stopped")
        exit(0)

    @commands.command(name='set_timer', past_context=True)
    async def set_timer(self, ctx, *msg):
        s = m = h = 0
        if len(msg) == 1 and msg[0].isdigit():
            s = int(msg[0])
        else:
            if "hours" in msg:
                h = int(msg[msg.index("hours") - 1])
                if "minutes" in msg:
                    m = int(msg[msg.index("minutes") - 1])
                    if "seconds" in msg:
                        s = int(msg[msg.index("seconds") - 1])
        try:
            time = s + m * 60 + h * 3600
            print(time)
            if time < 0:
                await ctx.send('Number cant be a negative')
            else:
                message = await ctx.send(time)
                while time:
                    time -= 1
                    await message.edit(content=time)
                    await asyncio.sleep(0.95)
                await message.edit(content='Time X has come!!!')

        except ValueError:
            await ctx.send(
                "you can set a timer with command with !set_timer x hours y minutes z seconds "
                "or just !set_timer N - a number of seconds")
            await ctx.send('Time was not a number')


bot = commands.Bot(command_prefix='!', intents=intents)

TOKEN = "MTA5NjA2MDA1MjkyNzk1MDg0OA.GXYo5d.Ua_b4cCKHy72Z5GDOdXGAOIevGbtFkW_UhiE74"


async def main():
    await bot.add_cog(TimerBot(bot))
    await bot.start(TOKEN)


asyncio.run(main())
