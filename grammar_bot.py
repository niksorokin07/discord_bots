import asyncio
import discord
from discord.ext import commands
import logging
import pymorphy2

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

morph = pymorphy2.MorphAnalyzer()


class GrammarBot(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='shutdown')
    async def shutdown(self, ctx):
        exit(0)

    @commands.command(name='help_bot')
    async def help(self, ctx):
        await ctx.send(
            """Allowed commands: 
                !numerals - for arrangement with numerals
                !alive    - for defining alive or not
                !noun     - for noun case(nomn, gent, datv, accs, ablt, loct) and number state(singular, plural)
                !inf      - for infinitive state
                !morph    - for full morphological analysis""")

    @commands.command(name='numerals')
    async def numerals(self, ctx, word, num):
        try:
            word = morph.parse(word)[0]
            await ctx.send(word.make_agree_with_number(int(num)).word)
        except TypeError:
            await ctx.send("Only words are allowed.")
        except ValueError:
            await ctx.send("Something went wrong, please check you command.")

    @commands.command(name='alive')
    async def alive(self, ctx, word):
        try:
            word = morph.parse(word)[0]
            if "NOUN" in word.tag:
                if "anim" in word.tag:
                    await ctx.send("Yes, it is")
                else:
                    await ctx.send("No, it is not")
            else:
                await ctx.send("Alive is a property of nouns")
        except TypeError:
            await ctx.send("Only words are allowed.")
        except ValueError:
            await ctx.send("Something went wrong, please check you command.")

    @commands.command(name='noun')
    async def noun(self, ctx, word, *params):
        try:
            word = morph.parse(word)[0]
            if "NOUN" in word.tag and params is not None:
                await ctx.send(word.inflect({*params}).word)
            else:
                await ctx.send("Enter a noun and parameters according to pymorphy2")
        except TypeError:
            await ctx.send("Only words are allowed.")
        except ValueError:
            await ctx.send("Something went wrong, please check you command.")

    @commands.command(name='inf')
    async def inf(self, ctx, word):
        try:
            word = morph.parse(word)[0]
            await ctx.send(word.normal_form)
        except TypeError:
            await ctx.send("Only words are allowed.")
        except ValueError:
            await ctx.send("Something went wrong, please check you command.")

    @commands.command(name='morph')
    async def morph(self, ctx, word):
        try:
            word = morph.parse(word)
            await ctx.send(word[word.index(max(word, key=lambda x: int(x.score)))])
        except TypeError:
            await ctx.send("Only words are allowed.")
        except ValueError:
            await ctx.send("Something went wrong, please check you command.")


bot = commands.Bot(command_prefix='!', intents=intents)

TOKEN = "MTA5ODQ5NzIxMDIwNDgxNTQzMg.GRSsk7.jZSQ5h8rJzkMGjhgbC8_zcMwXWuTQ2rZHGujBU"


async def main():
    await bot.add_cog(GrammarBot(bot))
    await bot.start(TOKEN)


asyncio.run(main())
