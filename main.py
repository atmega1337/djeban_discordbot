from platform import platform
import discord
import os
import asyncio
import sys

from discord.ext import commands
from discord.utils import get
from discord import FFmpegPCMAudio
from discord import TextChannel
from youtube_dl import YoutubeDL

# Файл конфига
configfile=os.path.join(os.path.dirname(sys.argv[0]), 'config.ini')

intents = discord.Intents.default() # Подключаем "Разрешения"
intents.message_content = True
bot = commands.Bot(command_prefix='/', intents=intents) 

song_queue = []

def createfile(path, lines):
    with open(path, "w", encoding='utf-8') as file:
        for  line in lines:
            file.write(line + '\n')
    file.close()

def create_config(path):
    print ('Create config file.')
    lines = ['# Discord bot token', 'token = 12345']
    createfile(path,lines)

# Чтение конфига
def read_config(path, parm):
    # Проверяем наличия файла, если нету - создаем
    if not os.path.isfile(path):
        print('Config file not found. Create new file.')
        create_config(configfile)
        print('Config file parameters error, default config creation. Restart required. Press any button to exit.')
        input()
        sys.exit()
    #Открываем файл
    file = open(path, "r", encoding='utf-8')
    #Перебираем значения
    findcvars = False
    for i in file.read().splitlines():
        if i.startswith(parm):
            cvar = i.lstrip(parm).lstrip().lstrip('=').lstrip() #Удаляем название квара, пробел, знак равно, пробел
            findcvars = True
    # Если нужного квара нету, пересоздаем конфиг
    if not findcvars:
        create_config(path)
        print('Config file parameters error, default config creation. Restart required. Press any button to exit.')
        input()
        sys.exit()
    # закрываем файл
    file.close()
    return cvar


def playlistinfo():
    infolist = "Playlist:\n"
    for n in range(len(song_queue)):
        infolist += str(n+1) + ') ' + song_queue[n][0] + "\n"
    print(infolist)
    return(infolist)

def addqueue(url=''):
    YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist': 'True'}
    with YoutubeDL(YDL_OPTIONS) as ydl:
        info = ydl.extract_info(url, download=False)
    newelement = [info['title'], info['url']]
    song_queue.append(newelement)


def playqueue(voice):
    if(song_queue):
        print(voice)
        FFMPEG_OPTIONS = {
            'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
        voice.play(FFmpegPCMAudio(song_queue[0][1], **FFMPEG_OPTIONS), after=lambda e: playqueue(voice))
        voice.is_playing()
        song_queue.pop(0)
    


@bot.event  # check if bot is ready
async def on_ready():
    print('Bot online')


# С помощью декоратора создаём первую команду
@bot.command()
async def ping(ctx):
    await ctx.send('pong')


# С помощью декоратора создаём первую команду
@bot.command()
async def test(ctx):
    server = ctx.message.guild
    print(server)
    voice_client = server.voice_client
    print(voice_client)
    addqueue("https://www.youtube.com/watch?v=JAB3OJMLb4I")
    chenal=ctx.author.voice.channel
    print(chenal)

@bot.command()
async def eban(ctx):
    if not ctx.message.guild.voice_client:
        await ctx.author.voice.channel.connect()
    
    voice = get(bot.voice_clients, guild=ctx.guild)
    song_queue.clear()
    addqueue("https://www.youtube.com/watch?v=EqB72SBN1F8")
    voice.stop()
    playqueue(voice)


@bot.command(pass_context = True)
async def join(ctx):
    if (ctx.author.voice):
        print('Server:', ctx.message.guild, 'Author:',ctx.author, 'Connect to voice:', ctx.author.voice.channel)
        await ctx.author.voice.channel.connect()
    else:
        await ctx.send("Please Join Voice channel to run this command")

@bot.command()
async def leave(ctx):
    print('Server:', ctx.message.guild, 'Author:',ctx.author, 'Leave voice.')
    await ctx.voice_client.disconnect()


# @bot.command()
# async def add(ctx, url):
#     YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist': 'True'}
#     FFMPEG_OPTIONS = {
#         'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
#     voice = get(bot.voice_clients, guild=ctx.guild)

#     if not voice.is_playing():
#         with YoutubeDL(YDL_OPTIONS) as ydl:
#             info = ydl.extract_info(url, download=False)
#         URL = info['url']
#         voice.play(FFmpegPCMAudio(URL, **FFMPEG_OPTIONS))
#         voice.is_playing()
#         await ctx.send('Bot is playing')

# command to play sound from a youtube URL
@bot.command()
async def play(ctx, url):

    # Проверка наличия бота в войсе
    if not ctx.message.guild.voice_client:
        await ctx.author.voice.channel.connect()

    voice = get(bot.voice_clients, guild=ctx.guild)
    if not voice.is_playing():
        addqueue(url)
        playqueue(voice)
    else:
        addqueue(url)
    await ctx.send(playlistinfo())
#     YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist': 'True'}
#     FFMPEG_OPTIONS = {
#         'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
#     voice = get(bot.voice_clients, guild=ctx.guild)
#     if not voice.is_playing():
#         with YoutubeDL(YDL_OPTIONS) as ydl:
#             info = ydl.extract_info(url, download=False)
#         URL = info['url']
#         voice.play(FFmpegPCMAudio(URL, **FFMPEG_OPTIONS), after=lambda e: playqueue(voice))
#         voice.is_playing()
#         await ctx.send('Bot is playing')

# # check if the bot is already playing
#     else:
#         await ctx.send("Bot is already playing")
#         return


# command to resume voice if it is paused
@bot.command()
async def resume(ctx):
    voice = get(bot.voice_clients, guild=ctx.guild)

    if not voice.is_playing():
        voice.resume()
        await ctx.send('Bot is resuming')


# command to pause voice if it is playing
@bot.command()
async def pause(ctx):
    voice = get(bot.voice_clients, guild=ctx.guild)

    if voice.is_playing():
        voice.pause()
        await ctx.send('Bot has been paused')


# command to stop voice
@bot.command()
async def skip(ctx):
    voice = get(bot.voice_clients, guild=ctx.guild)

    if voice.is_playing():
        voice.stop()
        await ctx.send('Skiping...')
        await ctx.send(playlistinfo())

# command to stop voice
@bot.command()
async def stop(ctx):
    voice = get(bot.voice_clients, guild=ctx.guild)

    if voice.is_playing():
        song_queue.clear()
        voice.stop()
        await ctx.send('Stopping...')

# command to clear channel messages
@bot.command()
async def clear(ctx, amount=5):
    await ctx.channel.purge(limit=amount)
    await ctx.send("Messages have been cleared")


token = read_config(configfile, 'token')
bot.run(token)




