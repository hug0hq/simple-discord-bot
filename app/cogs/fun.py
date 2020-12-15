import discord
from discord.ext import commands
from utils import permissions
import random


class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='dice', aliases=['d'])
    async def dice(self, ctx):
        """ Roll a dice """
        await ctx.message.delete()
        await ctx.send(f"🎲🎲   **{ctx.author.mention}** got **{random.randint(1, 6)}**!")

    @commands.command(name='pray', aliases=['f'])
    async def pray(self, ctx, member: discord.Member = None):
        """ Pray respect """
        await ctx.message.delete()
        reason = f"to {member.mention}" if member else ""
        await ctx.send(f"⚰️⚰️   {ctx.author.mention} has paid their respect {reason}")

    @pray.error
    async def pray_error(self, ctx, error):
        await ctx.message.delete()
        if isinstance(error, commands.MemberNotFound):
            await ctx.send('I could not find that member 😥')

    @commands.command(name='gift', aliases=['g'])
    async def gift(self, ctx, member: discord.Member):
        """ Offers a gift """
        await ctx.message.delete()
        gifts = ['🎈', '💊', '👟', '🏆', '☂️', '🍌',
                 '🍆', '🥕', '⚽️', '🎷', '🧻', '💩']
        await ctx.send(f'🎲🎁   {ctx.author.mention} offered a {random.choice(gifts)} to {member.mention}')

    @gift.error
    async def gift_error(self, ctx, error):
        await ctx.message.delete()
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('You\'re missing an argument 😥\nSee `-help gift`')
        elif isinstance(error, commands.MemberNotFound):
            await ctx.send('I could not find that member 😥')


def setup(bot):
    bot.add_cog(Fun(bot))
