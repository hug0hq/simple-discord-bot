import discord
from discord.ext import commands
import os
from discord.ext import commands

__author__ = "Hugo - hug0Hq"
__version__ = "1.2"


intents = discord.Intents.default()
intents.typing = False
intents.members = True

client = commands.Bot(command_prefix='-', intents=intents)


@client.event
async def on_connect():
    print(f'Connected as {client.user.id}')


@client.event
async def on_resumed():
    print(f'Connection resumed as {client.user.id}')


@client.event
async def on_disconnect():
    print('Bye!')


@client.event
async def on_ready():
    print(f'We have logged in as {client.user} [ready]')
    await client.change_presence(activity=discord.Game(name=os.environ['ACTIVITY_MSG']))


@client.check
async def globally_block_dms(ctx):
    if ctx.guild is None:
        await ctx.send('Please do not send me DMs 😐')
        return False
    return True


@client.event
async def on_command_error(ctx, error):
    await ctx.message.delete()
    if isinstance(error, commands.CommandNotFound):
        return await ctx.send('Command 404 😥\nSee `-help`')
    elif isinstance(error, commands.CheckFailure):
        return await ctx.send('Permission denied 🚨🚨') 
    elif isinstance(error, commands.MissingRequiredArgument):
        #handled in cogs
        return
    elif isinstance(error, commands.MemberNotFound):
        #handled in cogs
        return
    else:
        raise error


@client.event
async def on_member_join(member):
    channel = member.guild.system_channel
    if channel is not None:
        await channel.send(f'Hi, {member.mention}  😘😎')


@client.command()
async def ping(ctx):
    await ctx.message.delete()
    await ctx.send(f'🏓 Pong! {round(client.latency, 2)} 🏓')


@client.command()
async def source(ctx):
    await ctx.message.delete()
    await ctx.send(f"**{ctx.bot.user}**\nhttps://github.com/hug0Hq/simple-discord-bot")


@client.command()
async def licence(ctx):
    await ctx.message.delete()
    await ctx.send(f"**{ctx.bot.user}**\nhttps://github.com/hug0Hq/simple-discord-bot/blob/master/LICENSE")


for file in os.listdir("cogs"):
    if file.endswith(".py"):
        name = file[:-3]
        client.load_extension(f"cogs.{name}")

client.run(os.environ['API_KEY'])
