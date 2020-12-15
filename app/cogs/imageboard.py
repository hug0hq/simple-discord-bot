import discord
from discord.ext import commands
from data import db


class ImageBoard(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def __stop(self):
        await self.voice.disconnect()

    @commands.group(name='img', aliases=['i'])
    async def img(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.message.delete()
            await ctx.send('You\'re missing an argument 😥\nSee `-help img`')

    @img.command(name='show', aliases=['s'])
    async def displayImg(self, ctx, name):
        await ctx.message.delete()
        url = db.getFrom(ctx.guild.id, 'imageboard', name)
        embed = discord.Embed(title="",  colour=0xff4444)
        embed.set_footer(text=f"Image board - {name}")
        embed.set_image(url=url)
        message = await ctx.channel.send(embed=embed)

    @displayImg.error
    async def displayImg_error(self, ctx, error):
        await ctx.message.delete()
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('You\'re missing an argument 😥\nSee `-help img show`')

    @img.command(name='add', aliases=['a'])
    async def addImg(self, ctx, *, name):
        keyname = name.lower().replace(" ", "-")
        whiteList = ['jpeg', 'jpg', 'webp', 'png', 'gif']

        att = ctx.message.attachments[0]
        url = att.url
        if att.filename.split('.')[-1] not in whiteList:
            await ctx.send(att.filename.split('.')[-1]+" is not a valid image format")
        else:
            db.saveTo(ctx.guild.id, 'imageboard', (keyname, url))
            await ctx.send("⬆ Don't delete the source image\n☁☁ Done!")

    @addImg.error
    async def addImg_error(self, ctx, error):
        await ctx.message.delete()
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('You\'re missing an argument 😥\nSee `-help img add`')

    @img.command(name='list', aliases=['l'])
    async def listImg(self, ctx):
        await ctx.message.delete()
        imglist = db.listKeysFrom(ctx.guild.id, 'imageboard')
        embed = discord.Embed(title="🖼 Image board list:",
                              description="-img show [name]", colour=0xff4444)
        for name in imglist:
            embed.add_field(name=name, value="\u200b")
        message = await ctx.channel.send(embed=embed)

    @img.command(name='remove', aliases=['rm'])
    async def removeImg(self, ctx, name):
        await ctx.message.delete()
        db.delKey(ctx.guild.id, 'imageboard', name)
        await ctx.send('🧯 Done!')

    @removeImg.error
    async def removeImg_error(self, ctx, error):
        await ctx.message.delete()
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('You\'re missing an argument 😥\nSee `-help img remove`')


def setup(bot):
    bot.add_cog(ImageBoard(bot))
