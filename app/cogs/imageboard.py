import discord
from discord.ext import commands
from data import db
import re
from utils import permissions, http


class ImageBoard(commands.Cog, name='Image Board'):
    def __init__(self, bot):
        self.bot = bot

    async def __stop(self):
        await self.voice.disconnect()

    @commands.group(name='img', aliases=['i'])
    async def img(self, ctx):
        """ Image Board """
        if ctx.invoked_subcommand is None:
            await ctx.message.delete()
            await ctx.send('You\'re missing an argument 😥\nSee `-help img`')

    @img.command(name='show', aliases=['s'])
    async def displayImg(self, ctx, name):
        await ctx.message.delete()
        url = db.getFrom(ctx.guild.id, 'imageboard', name)
        if url == '404':
            return await ctx.send('Invalid key name 😥\nSee `-help img list`')
        embed = discord.Embed(title="",  colour=0xff4444)
        embed.set_footer(text=f"Image board - {name}")
        embed.set_image(url=url)
        message = await ctx.channel.send(embed=embed)

    @displayImg.error
    async def displayImg_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('You\'re missing an argument 😥\nSee `-help img show`')

    @img.command(name='add', aliases=['a'], description='Use on a file upload or pass a <url> after:')
    @commands.check(permissions.hasManagerRole)
    async def addImg(self, ctx, *, name):
        whiteList = ['.jpeg', '.jpg', '.webp', '.png', '.gif']
        filename = re.sub(
            r'http\S+', '', name).strip().lower().replace(" ", "-")
        url = re.search("(?P<url>https?://[^\s]+)", name)
        if url:
            await ctx.message.delete()
            error = http.fileIsType(url.group("url"), whiteList)
            if error:
                return await ctx.send(f"**{error}** is not a valid type")
            saveerror = db.saveTo(ctx.guild.id, 'imageboard',
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
            saveerror = db.saveTo(ctx.guild.id, 'imageboard', filename, url)
            if saveerror:
                await ctx.message.delete()
                return await ctx.send(f"**{filename}** already exists 🤔")
            await ctx.send("⬆ Don't delete the source image\n☁☁ Done!")
        else:
            await ctx.message.delete()
            await ctx.send("No URL or file 👎")

    @ addImg.error
    async def addImg_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('You\'re missing an argument 😥\nSee `-help img add`')

    @ img.command(name='list', aliases=['l'])
    async def listImg(self, ctx):
        await ctx.message.delete()
        imglist = db.listKeysFrom(ctx.guild.id, 'imageboard')
        embed = discord.Embed(title="🖼 Image board list:",
                              description="-img show [name]", colour=0xff4444)
        for name in imglist:
            embed.add_field(name=name, value="\u200b")
        message = await ctx.channel.send(embed=embed)

    @ img.command(name='remove', aliases=['rm'])
    @ commands.check(permissions.hasManagerRole)
    async def removeImg(self, ctx, name):
        await ctx.message.delete()
        db.delKey(ctx.guild.id, 'imageboard', name)
        await ctx.send('🧯 Done!')

    @ removeImg.error
    async def removeImg_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('You\'re missing an argument 😥\nSee `-help img remove`')


def setup(bot):
    bot.add_cog(ImageBoard(bot))
