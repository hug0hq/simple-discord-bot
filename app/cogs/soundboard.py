import discord
from discord.ext import commands
import asyncio
from data import db


class SoundBoard(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def __stop(self):
        await self.voice.disconnect()

    @commands.group(name='sound', aliases=['s'])
    async def sound(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.message.delete()
            await ctx.send('You\'re missing an argument 😥\nSee `-help sound`')

    @sound.command(name='play', aliases=['p'])
    async def playSound(self, ctx, name):
        await ctx.message.delete()
        if not ctx.message.author.voice:
            await ctx.send('You\'re not in a voice channel!  🔔🔊')
            return
        else:
            if not discord.opus.is_loaded():
                discord.opus.load_opus('/usr/bin/opusenc')
            channel = ctx.message.author.voice.channel
            try:
                voice = await channel.connect()
                url = db.getFrom(ctx.guild.id, 'soundboard', name)

                def my_after(error):
                    print('Sound! - error:', error)
                    fut = asyncio.run_coroutine_threadsafe(
                        voice.disconnect(), self.bot.loop)
                    try:
                        fut.result()
                    except:
                        # an error happened sending the message
                        pass

                voice.play(discord.FFmpegPCMAudio(url), after=my_after)
            except Exception as e:
                print(e)

    @playSound.error
    async def playSound_error(self, ctx, error):
        await ctx.message.delete()
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('You\'re missing an argument 😥\nSee `-help sound play`')

    @sound.command(name='add', aliases=['a'])
    async def addSound(self, ctx, *, name):
        keyname = name.lower().replace(" ", "-")
        whiteList = ['mp3', 'ogg', 'wav']

        att = ctx.message.attachments[0]
        url = att.url
        if att.filename.split('.')[-1] not in whiteList:
            await ctx.send(att.filename.split('.')[-1]+" is not a valid audio format")
        else:
            db.saveTo(ctx.guild.id, 'soundboard', (keyname, url))
            await ctx.send("⬆ Don't delete the source sound\n☁☁ Done!")

    @addSound.error
    async def addSound_error(self, ctx, error):
        await ctx.message.delete()
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('You\'re missing an argument 😥\nSee `-help sound add`')

    @sound.command(name='list', aliases=['l'])
    async def listSound(self, ctx):
        await ctx.message.delete()
        imglist = db.listKeysFrom(ctx.guild.id, 'soundboard')
        embed = discord.Embed(title="🔊 Sound board list:",
                              description="-sound play [name]", colour=0xff4444)
        for name in imglist:
            embed.add_field(name=name, value="\u200b")
        message = await ctx.channel.send(embed=embed)

    @sound.command(name='remove', aliases=['rm'])
    async def removeSound(self, ctx, name):
        await ctx.message.delete()
        db.delKey(ctx.guild.id, 'soundboard', name)
        await ctx.send('🧯 Done!')

    @removeSound.error
    async def removeSound_error(self, ctx, error):
        await ctx.message.delete()
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('You\'re missing an argument 😥\nSee `-help sound remove`')


def setup(bot):
    bot.add_cog(SoundBoard(bot))
