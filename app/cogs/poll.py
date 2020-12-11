import discord
from discord.ext import commands

numbers = ['0️⃣', '1️⃣', '2️⃣', '3️⃣', '4️⃣']


class Poll(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def __simplePoll(self, ctx, question):
        embed = discord.Embed(title=f"📢📢\n{question}?",  colour=0xff4400)
        #embed.add_field(name=f"{question} ?", value="l")
        embed.set_footer(text="React to cast a vote!")
        message = await ctx.channel.send(embed=embed)
        await message.add_reaction('👍')
        await message.add_reaction('👎')

    async def __multiplePoll(self, ctx, question):
        tp = question.split(';')
        c = '\n'.join(
            [f'{numbers[ind]}  {elem}?' for ind, elem in enumerate(tp)])
        embed = discord.Embed(title=f"📢📢\n{c}",  colour=0xff4400)
        #embed.add_field(name=f"{question} ?", value="l")
        embed.set_footer(text="React to cast a vote!")
        message = await ctx.channel.send(embed=embed)
        for react in numbers[:len(tp)]:
            await message.add_reaction(react)

    @commands.command(name='poll', aliases=['polls'])
    async def poll(self, ctx, *, question):
        await ctx.message.delete()  # delete user msg
        if question.find(';') == -1:
            await self.__simplePoll(ctx, question)
        else:
            await self.__multiplePoll(ctx, question)


def setup(bot):
    bot.add_cog(Poll(bot))
