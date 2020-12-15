import discord
from discord.ext import commands
import os
from discord.ext import commands

__author__ = "Hugo - hug0Hq"
__version__ = "1.2"


intents = discord.Intents(messages=True, guilds=True)
client = commands.Bot(command_prefix='-')


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
    # return ctx.guild is not None


@client.event
async def on_command_error(ctx, error):
    await ctx.message.delete()
    if isinstance(error, commands.CommandNotFound):
        # await ctx.message.delete()
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

# @bot.event
# async def on_message(message):
# await bot.delete_message(message)

# help info
""" @bot.command(pass_context=True)
async def info(ctx):
    p = await bot.get_message(ctx.message.channel, ctx.message.id)
    await bot.delete_message(p)

    em = discord.Embed(title="Bot info", description='made my Hugo Costa', color=0xff4400)
    em.add_field(name='Text message help', value='#listmsg')
    em.add_field(name='Soundboard help', value='#listsound')
    await bot.say(embed=em)

# add msg
@bot.command(pass_context=True)
async def addmsg(ctx, msg):
    p = await bot.get_message(ctx.message.channel, ctx.message.id)
    await bot.delete_message(p)

    with open('textmsg.json') as f:
        data = json.load(f)
        numb = data['text'][ len(data['text'])-1 ]['id'] + 1

        data['text'].append({
            'id': numb,
            'msg': msg
        })

    with open('textmsg.json', 'w') as outfile:
        json.dump(data, outfile)

    await bot.say("Done! ID: "+str(numb))

# send msg
@bot.command(pass_context=True) #pass_context=True
async def msg(ctx):
    p = await bot.get_message(ctx.message.channel, ctx.message.id)
    await bot.delete_message(p)

    ctxx = ctx.message.content
    msg = ctxx.split(" ")

    if len(msg) > 1:
        with open('textmsg.json') as f:
            data = json.load(f)
            el = data['text'][ int(msg[1])-1 ]['msg']

    if len(msg) == 3:
        await bot.say(msg[2]+" "+el)
    else:
        await bot.say(el)

# see msg
@bot.command(pass_context=True)
async def listmsg(ctx):
    p = await bot.get_message(ctx.message.channel, ctx.message.id)
    await bot.delete_message(p)

    em = discord.Embed(title="Text message list", description='usage: #add <"text"> | #msg: <id> <@mension>', color=0x00ff00)
    with open('textmsg.json') as f:
        data = json.load(f)

        for i in data['text']:
            em.add_field(name=i['id'], value=i['msg'])

    await bot.say(embed=em)

# see sound
@bot.command(pass_context=True)
async def listsound(ctx):
    p = await bot.get_message(ctx.message.channel, ctx.message.id)
    await bot.delete_message(p)

    em = discord.Embed(title="Soundboard list", description='usage: <add file> #addsound | #play: <id>', color=0x0077ff)
    for file in os.listdir("sounds/"):
        text = file.split(".")
        em.add_field(name=text[0], value=text[1])

    await bot.say(embed=em)

# add sound
@bot.command(pass_context=True)
async def addsound(ctx):
    p = await bot.get_message(ctx.message.channel, ctx.message.id)
    await bot.delete_message(p)

    whiteList = ['mp3','ogg','wav']
    try:
        for att in ctx.message.attachments:
            if att['filename'].split('.')[-1] not in whiteList:
                await bot.say(att['filename'].split('.')[-1]+" is not an audio format")
            else:
                with open('data.json') as f:
                    data = json.load(f)
                    numb = data['soundlastid']
                    numb += 1
                    data['soundlastid'] = numb

                with open('data.json', 'w') as outfile:
                    json.dump(data, outfile)

                url = att['proxy_url']
                filename = 'sounds/'+str(numb)+'.'+att['filename']

                r = requests.get(url, stream=True, headers={'User-agent': 'Mozilla/5.0'})
                if r.status_code == 200:
                    with open(filename, 'wb') as f:
                        r.raw.decode_content = True
                        shutil.copyfileobj(r.raw, f)
                await bot.say('Done! ID: '+str(numb))

    except Exception as e:
        fmt = 'An error occurred while processing this request: ```py\n{}: {}\n```'
        await bot.say(ctx.message.channel, fmt.format(type(e).__name__, e))

    # except:
    #    print('Unknown error')


    # print(attachments ["url"])
    # await client.send_file(client.get_server('321332957690331138').default_channel, '1.jpg')
    # await bot.say("Done! ID: ")

# sound play
@bot.command(pass_context=True)
async def play(ctx, soundid):
    p = await bot.get_message(ctx.message.channel, ctx.message.id)
    await bot.delete_message(p)

    author = ctx.message.author

    if author.voice_channel :

        if not discord.opus.is_loaded():
            discord.opus.load_opus()

        try:
            voice_channel = author.voice_channel

            voice = await bot.join_voice_channel(voice_channel)

            for file in os.listdir("sounds/"):
                text = file.split(".")
                if(text[0]==soundid):
                    url = 'sounds/'+file

            print(url)
            player = voice.create_ffmpeg_player(url, after = lambda: bot.loop.create_task(voice.disconnect()))
            player.start()

        except Exception as e:
            fmt = 'An error occurred while processing this request: ```py\n{}: {}\n```'
            await bot.say(ctx.message.channel, fmt.format(type(e).__name__, e))

    else:
        await bot.say('You\'re not in a voice channel!') """
