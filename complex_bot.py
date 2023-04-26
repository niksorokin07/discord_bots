import asyncio
import discord
from discord.ext import commands
import logging
from random import choices, choice

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix='/', intents=intents)

TOKEN = "MTA5OTMxNDI4NDY5NTEyNjA5Ng.GcggGU.DFWJ8Qw0zE9jMBj_y6QYBNlWI21IYKrgd5h6L4"

score_p = score_b = 0

emojis = """
😀 😁 😂 😃 😄 😅 😆 😇 😈 😉 😊 😋 😌 😍 😎 😏
😐 😑 😒 😓 😔 😕 😖 😗 😘 😙 😚 😛 😜 😝 😞 😟
😠 😡 😢 😣 😤 😥 😦 😧 😨 😩 😪 😫 😬 😭 😮 😯
😰 😱 😲 😳 😴 😵 😶 😷 😸 😹 😺 😻 😼 😽 😾 😿
🙀 🙁 🙂 🙃 🙄 🙅 🙆 🙇 🙈 🙉 🙊 🙋 🙌 🙍 🙎 🙏
👍 👎 ☀ ☁ ☂ ☃ ☄ ★ ☆ ☇ ☈ ☉ ☊ ☋ ☌ ☍ ☎ ☏
☐ ☑ ☒ ☓ ☔ ☕ ☖ ☗ ☘ ☙ ☚ ☛ ☜ ☝ ☞ ☟
☠ ☡ ☢ ☣ ☤ ☥ ☦ ☧ ☨ ☩ ☪ ☫ ☬ ☭ ☮ ☯
☰ ☱ ☲ ☳ ☴ ☵ ☶ ☷ ☸ ☹ ☺ ☻ ☼ ☽ ☾ ☿
♀ ♁ ♂ ♃ ♄ ♅ ♆ ♇ ♈ ♉ ♊ ♋ ♌ ♍ ♎ ♏
♐ ♑ ♒ ♓ ♔ ♕ ♖ ♗ ♘ ♙ ♚ ♛ ♜ ♝ ♞ ♟
♠ ♡ ♢ ♣ ♤ ♥ ♦ ♧ ♨ ♩ ♪ ♫ ♬ ♭ ♮ ♯
♰ ♱ ♲ ♳ ♴ ♵ ♶ ♷ ♸ ♹ ♺ ♻ ♼ ♽ ♾ ♿
⚀ ⚁ ⚂ ⚃ ⚄ ⚅ ⚆ ⚇ ⚈ ⚉ ⚊ ⚋ ⚌ ⚍ ⚎ ⚏
⚐ ⚑ ⚒ ⚓ ⚔ ⚕ ⚖ ⚗ ⚘ ⚙ ⚚ ⚛ ⚜ ⚝ ⚞ ⚟
⚠ ⚡ ⚢ ⚣ ⚤ ⚥ ⚦ ⚧ ⚨ ⚩ ⚪ ⚫ ⚬ ⚭ ⚮ ⚯
⚰ ⚱ ⚲ ⚳ ⚴ ⚵ ⚶ ⚷ ⚸ ⚹ ⚺ ⚻ ⚼ ⚽ ⚾ ⚿
⛀ ⛁ ⛂ ⛃ ⛄ ⛅ ⛆ ⛇ ⛈ ⛉ ⛊ ⛋ ⛌ ⛍ ⛎ ⛏
⛐ ⛑ ⛒ ⛓ ⛔ ⛕ ⛖ ⛗ ⛘ ⛙ ⛚ ⛛ ⛜ ⛝ ⛞ ⛟
⛠ ⛡ ⛢ ⛣ ⛤ ⛥ ⛦ ⛧ ⛨ ⛩ ⛪ ⛫ ⛬ ⛭ ⛮ ⛯
⛰ ⛱ ⛲ ⛳ ⛴ ⛵ ⛶ ⛷ ⛸ ⛹ ⛺ ⛻ ⛼ ⛽ ⛾ ⛿
""".split()


@bot.command(name='stop')
async def stop(ctx):
    global score_p, score_b, started
    score_p = score_b = 0
    started = False


@bot.command(name='start')
async def start(ctx):
    reserve = choices(emojis, k=31)
    ct = 0
    await ctx.send("The game has begun")
    global score_p, score_b, started
    score_p = score_b = 0
    started = True
    try:
        message = await bot.wait_for('message', timeout=10,
                                     check=lambda m: m.author == ctx.author and m.channel == ctx.channel)
        while started:
            if message.content == "/stop":
                score_p = score_b = 0
                started = False
                return
            elif message.content.isdigit():
                if ct < 30:
                    n = int(message.content) % len(reserve)
                    chosen = int(choice(list([i for i in range(n)] + [j for j in range(n + 1, len(reserve))])))
                    if ord(reserve[n]) > ord(reserve[chosen]):
                        score_p += 1
                    else:
                        score_b += 1
                    await ctx.send(f"""Your emoji: {reserve[n]}
Bot emoji: {reserve[chosen]}
Score: You {score_p} - Bot {score_b}""")
                    reserve.pop(n)
                    ct += 1
                    message = await bot.wait_for('message', timeout=10,
                                                 check=lambda m: m.author == ctx.author and m.channel == ctx.channel)
                else:
                    if score_p > score_b:
                        winner = "Bot"
                    elif score_p == score_b:
                        winner = "It's a tie, nobody"
                    else:
                        winner = "You"
                    await ctx.send(f"""Emoticons are over,
Score: You {score_p} - Bot {score_b}
{winner} won!""")
                    return
    except asyncio.TimeoutError:
        await ctx.send('You failed to respond in time, gotta be quicker! Type /start once again')
        return


bot.run(TOKEN)
