import discord
from discord.ext import commands

from data import db

class ImageBoard(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def __stop(self):       
        await self.voice.disconnect() 

    @commands.command(name='img', aliases=['pic'])
    async def displayImg(self, ctx, key):
        await ctx.message.delete()     
        url = await db.getFrom(ctx.guild.id, 'imageboard', key)                
        embed = discord.Embed(title="",  colour=0xff4444)
        #embed.add_field(name=f"{question} ?", value="l")
        embed.set_footer(text=f"{key}")
        embed.set_image(url=url)
        message = await ctx.channel.send(embed=embed)
       

    @commands.command(name='addimg', aliases=['addi', 'addp'])
    async def addimg(self, ctx, *, key):
        # p = await bot.get_message(ctx.message.channel, ctx.message.id)
        # await bot.delete_message(p)
        # await ctx.message.delete()  # delete user msg
        print(ctx.message.attachments)
        # print(ctx.message)
        #print(key.lower().replace(" ", "-"))
        keyname = key.lower().replace(" ", "-")
        whiteList = ['jpeg', 'jpg', 'webp', 'png', 'gif']

        att = ctx.message.attachments[0]
        url = att.url
        if att.filename.split('.')[-1] not in whiteList:
            await ctx.send(att.filename.split('.')[-1]+" is not a valid image format")
        else:
            #await db.createDictionary('imageboard')
            await db.saveTo(ctx.guild.id, 'imageboard', (keyname, url))
            await ctx.send("☁☁ done")

def setup(bot):
    bot.add_cog(ImageBoard(bot))
