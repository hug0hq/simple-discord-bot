import discord
from discord.ext import commands


class Poll(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def __simplePoll(self, ctx, question):
        embed = discord.Embed(title=f"📢📢\n{question}?",  colour=0xff4444)
        embed.set_footer(text="React to cast a vote!")
        message = await ctx.channel.send(embed=embed)
        await message.add_reaction('👍')
        await message.add_reaction('👎')

    async def __multiplePoll(self, ctx, question):
        numbers = ['0️⃣', '1️⃣', '2️⃣', '3️⃣', '4️⃣']
        q = [elem.strip() for elem in question.split(';')]
        qclean = [elem for ind, elem in enumerate(
            q) if elem != '' and ind < 5]
        c = '\n'.join(
            [f'{numbers[ind]}  {elem}?' for ind, elem in enumerate(qclean)])
        embed = discord.Embed(title=f"📢📢\n{c}",  colour=0xff4444)
        embed.set_footer(text="React to cast a vote!")
        message = await ctx.channel.send(embed=embed)
        for react in numbers[:len(qclean)]:
            await message.add_reaction(react)

    @commands.command(name='poll', aliases=['p'], description='Multiple questions: <question>; <question>')
    async def poll(self, ctx, *, question):
        """ Create a poll """
        await ctx.message.delete()
        if question.find(';') == -1:
            await self.__simplePoll(ctx, question)
        else:
            await self.__multiplePoll(ctx, question)

    @poll.error
    async def poll_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            return await ctx.send('You\'re missing an argument 😥\nSee `-help poll`')


def setup(bot):
    bot.add_cog(Poll(bot))
