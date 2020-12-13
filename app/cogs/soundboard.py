import discord
from discord.ext import commands

import asyncio
# from asyncio import sleep

from data import db


class SoundBoard(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def __stop(self):
        await self.voice.disconnect()

    @commands.command(name='playsound', aliases=['play', 'plays', 'sound'])
    async def playsound(self, ctx, key):
        await ctx.message.delete()
        if not ctx.message.author.voice:
            await ctx.send('You\'re not in a voice channel!')
            return
        else:
            if not discord.opus.is_loaded():
                discord.opus.load_opus('/usr/bin/opusenc')

            channel = ctx.message.author.voice.channel
            try:
                voice = await channel.connect()
                url = await db.getFrom(ctx.guild.id, 'soundboard', key)
                print(url)

                def my_after(error):
                    #coro = voice.disconnect()
                    print('Done', error)
                    fut = asyncio.run_coroutine_threadsafe(
                        voice.disconnect(), self.bot.loop)
                    try:
                        fut.result()
                    except:
                        # an error happened sending the message
                        pass
                # source = await discord.FFmpegOpusAudio.from_probe(url)
                voice.play(discord.FFmpegPCMAudio(url), after=my_after)
                # lambda e: print(f'Done {e}')

            except Exception as e:
                print(e)
    
    """ @commands.command(name='test', aliases=['t'])
    async def test(self, ctx):
        db.test() """

    @commands.command(name='addsound', aliases=['adds'])
    async def addsound(self, ctx, *, key):
        # p = await bot.get_message(ctx.message.channel, ctx.message.id)
        # await bot.delete_message(p)
        # await ctx.message.delete()  # delete user msg
        print(ctx.message.attachments)
        # print(ctx.message)
        # print(key.lower().replace(" ", "-"))
        keyname = key.lower().replace(" ", "-")
        whiteList = ['mp3', 'ogg', 'wav']

        att = ctx.message.attachments[0]
        url = att.url
        if att.filename.split('.')[-1] not in whiteList:
            await ctx.send(att.filename.split('.')[-1]+" is not a valid audio format")
        else:
            # await db.createDictionary('soundboard')
            await db.saveTo( ctx.guild.id, 'soundboard', (keyname, url))
            await ctx.send("☁☁ done")


def setup(bot):
    bot.add_cog(SoundBoard(bot))
