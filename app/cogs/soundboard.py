import discord
from discord.ext import commands
import asyncio
from data import db
import re
from utils import permissions, http


class SoundBoard(commands.Cog, name='Sound Board'):
    def __init__(self, bot):
        self.bot = bot

    async def __stop(self):
        await self.voice.disconnect()

    @commands.group(name='sound', aliases=['s'])
    async def sound(self, ctx):
        """ Sound Board """
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
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('You\'re missing an argument 😥\nSee `-help sound play`')

    @sound.command(name='add', aliases=['a'], description='Use on a file upload or pass a <url> after:')
    @commands.check(permissions.hasManagerRole)
    async def addSound(self, ctx, *, name):
        whiteList = ['.mp3', '.ogg', '.oga', '.wav']
        filename = re.sub(
            r'http\S+', '', name).strip().lower().replace(" ", "-")
        url = re.search("(?P<url>https?://[^\s]+)", name)
        if url:
            await ctx.message.delete()
            error = http.fileIsType(url.group("url"), whiteList)
            if error:
                return await ctx.send(f"**{error}** is not a valid type")
            saveerror = db.saveTo(ctx.guild.id, 'soundboard',
                                  filename, url.group("url"))
            if saveerror:
                return await ctx.send(f"**{filename}** already exists 🤔")
            await ctx.send("☁☁ Done!")
        elif ctx.message.attachments:
            url = ctx.message.attachments[0].url
            error = http.fileIsType(url, whiteList)
            if error:
                await ctx.message.delete()
                return await ctx.send(f"**{error}** is not a valid type")
            saveerror = db.saveTo(ctx.guild.id, 'soundboard', filename, url)
            if saveerror:
                await ctx.message.delete()
                return await ctx.send(f"**{filename}** already exists 🤔")
            await ctx.send("⬆ Don't delete the source sound\n☁☁ Done!")
        else:
            await ctx.message.delete()
            await ctx.send("No URL or file 👎")

    @addSound.error
    async def addSound_error(self, ctx, error):
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
    @commands.check(permissions.hasManagerRole)
    async def removeSound(self, ctx, name):
        await ctx.message.delete()
        db.delKey(ctx.guild.id, 'soundboard', name)
        await ctx.send('🧯 Done!')

    @removeSound.error
    async def removeSound_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('You\'re missing an argument 😥\nSee `-help sound remove`')


def setup(bot):
    bot.add_cog(SoundBoard(bot))
