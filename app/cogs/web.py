import discord
from discord.ext import commands
import aiohttp
import json


class Web(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def cat1(self, ctx):
        async with aiohttp.ClientSession() as session:
            async with session.get('https://aws.random.cat/meow') as r:
                if r.status == 200:
                    js = await r.json()
                    print(js['file'])
                    embed = discord.Embed(title="cat1",  colour=0xff4400)
                    # embed.add_field(name=f"{question} ?", value="l")

                    embed.set_image(url=js['file'])
                    message = await ctx.channel.send(embed=embed)

    @commands.command()
    async def cat2(self, ctx):
        async with aiohttp.ClientSession() as session:
            async with session.get('https://api.thecatapi.com/v1/images/search') as r:
                if r.status == 200:
                    js = await r.json()
                    print(js[0]['url'])
                    embed = discord.Embed(title="cat2",  colour=0xff4400)
                    # embed.add_field(name=f"{question} ?", value="l")

                    embed.set_image(url=js[0]['url'])
                    message = await ctx.channel.send(embed=embed)

    @commands.command()
    async def dog(self, ctx):
        async with aiohttp.ClientSession() as session:
            async with session.get('https://random.dog/woof.json') as r:
                if r.status == 200:
                    js = await r.json()
                    print(js['url'])
                    embed = discord.Embed(title="dog",  colour=0xff4400)
                    # embed.add_field(name=f"{question} ?", value="l")

                    embed.set_image(url=js['url'])
                    message = await ctx.channel.send(embed=embed)

    @commands.command()
    async def advice(self, ctx):
        async with aiohttp.ClientSession() as session:
            async with session.get('https://api.adviceslip.com/advice') as r:
                if r.status == 200:
                    j = await r.read()
                    js = json.loads(j)
                    print(js['slip']['advice'])
                    await ctx.send(f"💡 {js['slip']['advice']}")

    @commands.command()
    async def dadjoke(self, ctx):
        headers = {'Accept': 'application/json'}
        async with aiohttp.ClientSession() as session:
            async with session.get('https://icanhazdadjoke.com/', headers=headers) as r:
                if r.status == 200:
                    js = await r.json()
                    print(js['joke'])
                    await ctx.send(f"{js['joke']} 🤦")

    @commands.command()
    async def insult(self, ctx):
        async with aiohttp.ClientSession() as session:
            async with session.get('https://evilinsult.com/generate_insult.php?lang=en&type=json') as r:
                if r.status == 200:
                    js = await r.json()
                    print(js['insult'])
                    await ctx.send(f"{js['insult']} 🔥🔥")


def setup(bot):
    bot.add_cog(Web(bot))
