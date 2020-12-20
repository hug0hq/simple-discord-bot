import discord
from discord.ext import commands
from utils import http
from datetime import datetime


class Web(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def __error(self, ctx):
        await ctx.send("🔥🔥 API Error")

    @commands.command(name='cat')
    async def cat(self, ctx):
        """  Random cat """
        await ctx.message.delete()
        # alternative api https://aws.random.cat/meow
        js = await http.get('https://api.thecatapi.com/v1/images/search')
        if js == 'error':
            await self.__error(ctx)
            return
        embed = discord.Embed(title="🐱 Your random cat:",  colour=0xff4444)
        embed.set_footer(text=js[0]['url'])
        embed.set_image(url=js[0]['url'])
        await ctx.channel.send(embed=embed)

    @commands.command(name='dog')
    async def dog(self, ctx):
        """ Random dog """
        await ctx.message.delete()
        js = await http.get('https://random.dog/woof.json')
        if js == 'error':
            await self.__error(ctx)
            return
        embed = discord.Embed(
            title="🐶 Your random dog:",  colour=0xff4444)
        embed.set_footer(text=js['url'])
        embed.set_image(url=js['url'])
        await ctx.channel.send(embed=embed)

    @commands.command(name='advice', aliases=['a'])
    async def advice(self, ctx):
        """ Looking for advice """
        await ctx.message.delete()
        js = await http.get('https://api.adviceslip.com/advice', 'text')
        if js == 'error':
            await self.__error(ctx)
            return
        await ctx.send(f"💡  {js['slip']['advice']}")

    @commands.command(name='dadjoke', aliases=['joke', 'dj'])
    async def dadjoke(self, ctx):
        """ Random dad joke """
        await ctx.message.delete()
        js = await http.get('https://icanhazdadjoke.com/')
        if js == 'error':
            await self.__error(ctx)
            return
        await ctx.send(f"{js['joke']}  🤦")

    @commands.command(name='insult', aliases=['in'])
    async def insult(self, ctx, member: discord.Member = None):
        """ Evil insult generator """
        await ctx.message.delete()
        js = await http.get('https://evilinsult.com/generate_insult.php?lang=en&type=json')
        if js == 'error':
            await self.__error(ctx)
            return
        to = f"{member.mention}\n" if member else ""
        await ctx.send(f"{to}{js['insult']}  🔥🔥")

    @insult.error
    async def insult_error(self, ctx, error):
        await ctx.message.delete()
        if isinstance(error, commands.MemberNotFound):
            await ctx.send('I could not find that member 😥')

    @commands.command(name='btc')
    async def btc(self, ctx):
        """ BTC price """
        await ctx.message.delete()
        js = await http.get('https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=eur&include_24hr_change=true&include_last_updated_at=true')
        if js == 'error':
            await self.__error(ctx)
            return
        price = js['bitcoin']['eur']
        change = js['bitcoin']['eur_24h_change']
        time = datetime.fromtimestamp(js['bitcoin']['last_updated_at'])
        direction = '🟢📈🚀🌕' if change > 0 else '🔴📉🕯️‼'
        await ctx.send(f"💰💰  **1₿** = **{price}€**  {change:.2}% {direction}\n⌚{time.time()}")


def setup(bot):
    bot.add_cog(Web(bot))
