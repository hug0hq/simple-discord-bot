import discord
from discord.ext import commands
from utils import permissions
import random

class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # @commands.check(permissions.hasRole)
    @commands.command(name='kick', aliases=['k'])
    async def randomDisconnect(self, ctx, member: discord.Member):
        await ctx.message.delete()
        """ if not ctx.member.hasPermission("o_o"):
            return await ctx.send('❌') """

        print(ctx)
        await ctx.send('🎲🎁 By ')
        # message = await ctx.channel.send(embed=embed)

    @commands.command(aliases=['flip', 'coin'])
    async def dice(self, ctx):
        await ctx.send(f"🎲🎲 **{ctx.author.nick}** got **{random.randint(1, 6)}**!")

    @commands.command()
    async def f(self, ctx, *, text: commands.clean_content = None):
        reason = f"to **{text}** " if text else ""
        await ctx.send(f"⚰️ **{ctx.author.nick}** has paid their respect {reason} ❤")


def setup(bot):
    bot.add_cog(Fun(bot))
