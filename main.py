import os
import sys
import disnake
import datetime
import asyncio
import urlyoutube

from disnake.ext import commands
from disnake import FFmpegPCMAudio
from disnake.utils import get

# server, [name:'', url:'', img:'', customer: '']
song_queue = {} 

bot = commands.Bot(command_prefix='!', intents=disnake.Intents.all(), activity = disnake.Streaming(name='YouTube', url='https://www.youtube.com/watch?v='))

# Не работает mp3
# FFMPEG_OPTIONS = {
#     'before_options': '-nostdin  -reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
#     'options': '-vn'
# }
FFMPEG_OPTIONS = {
    'before_options': '-nostdin',
    'options': '-vn'
}


def playlistinfo(idserver):
    infolist = "Playlist: \n"
    if song_queue[idserver]:
        for n in range(len(song_queue[idserver])):
            infolist += "{}) {} (Customer: {})\n".format(str(n+1), song_queue[idserver][n]['name'], song_queue[idserver][n]['customer'])
    return(infolist)

def addqueue(idserver,name,url,img='',customer=''):
    newelement = {
        'name':name,
        'url':url,
        'img':img,
        'customer': customer
    }
    if not idserver in song_queue:
        song_queue[idserver] = []
    song_queue[idserver].append(newelement)

#Сам плеер
def player(inter):
    voice = get(bot.voice_clients, guild=inter.guild)
    # Если есть очередь и не играет
    if song_queue[inter.guild_id]:
        voice.play(FFmpegPCMAudio(song_queue[inter.guild_id][0]['url'], **FFMPEG_OPTIONS), after=lambda e: afterplay(inter))
# Действия после воспроизведения
def afterplay(inter):
    #Удалить то, что играло
    if song_queue[inter.guild_id]:
        song_queue[inter.guild_id].pop(0)
    #Eсли есть очередь - запустить
    if song_queue[inter.guild_id]:
        player(inter)

async def join_to_voice(inter, channel=None):
    """
    Connecting to voice chennal
    """
    if not channel:
        try:
            channel = inter.author.voice.channel
        except AttributeError:
            msg='Sign in voice channel before sending a command'
    
    vc = inter.guild.voice_client

    if vc:
        if vc.channel.id == channel.id:
            return
        await vc.move_to(channel)
        msg="Move to channel: {}".format(channel)
    else:
        await channel.connect()
        msg="Join to channel: {}".format(channel)
    print('Server {}. Author: {} Connect to voice: {}'.format(inter.guild,inter.author,channel))
    return msg
   

@bot.slash_command(description='Подключение к войс чату')
async def join(inter, channel: disnake.VoiceChannel=None):
    msg= await join_to_voice(inter, channel)
    await inter.response.send_message(msg, delete_after=10)
    

@bot.slash_command(description='Выйти из войса')
async def leave(inter):
    print('Server {}. Author: {} Leave voice.'.format(inter.guild,inter.author))
    await inter.guild.voice_client.disconnect(force=True)
    await inter.response.send_message("Leave voice.", delete_after=10)


@bot.slash_command(description='Включить говно с ютуба')
async def play(inter, url):
    print('Server {}. Author: {} play: {}'.format(inter.guild,inter.author,url))
    await inter.response.send_message('Author: {} play: {}'.format(inter.author,url), delete_after=10)
    # Добавляем в войс
    await join_to_voice(inter)

    # Конвертируем ссылку с ютуба
    if (('youtube.com/watch?v=' in url) or ("youtu.be/" in url)):
        data=urlyoutube.get(url)
    else:
        await inter.send("Link not supported", delete_after=10)
        return

    # Добавляем в очередь
    addqueue(inter.guild_id, data['title'], data['url'], data['img'], inter.author.name)
    
    # Запускаем плеер
    voice = get(bot.voice_clients, guild=inter.guild)
    if not voice.is_playing():
        player(inter)
    await inter.send(playlistinfo(inter.guild_id), delete_after=300)

@bot.slash_command(description='Продолжить')
async def resume(inter):
    voice = get(bot.voice_clients, guild=inter.guild)

    if not voice.is_playing():
        voice.resume()
        await inter.response.send_message("Bot is resuming", delete_after=10)


@bot.slash_command(description='Поставить на паузу')
async def pause(inter):
    voice = get(bot.voice_clients, guild=inter.guild)

    if voice.is_playing():
        voice.pause()
        await inter.response.send_message("Bot has been paused", delete_after=10)


@bot.slash_command(description='Скип говна, если DJ ебан')
async def skip(inter):
    voice = get(bot.voice_clients, guild=inter.guild)

    if voice.is_playing():
        voice.stop()
        await asyncio.sleep(1)
        await inter.response.send_message(playlistinfo(inter.guild_id), delete_after=10)


@bot.slash_command(description='Стоп')
async def stop(inter):
    voice = get(bot.voice_clients, guild=inter.guild)

    if voice.is_playing():
        song_queue[inter.guild_id].clear()
        voice.stop()
        await inter.response.send_message("Stopping...", delete_after=10)


dirmp3=os.path.join(os.path.dirname(sys.argv[0]),'mp3')
listmp3 = os.listdir(dirmp3)

@bot.slash_command(description='Мемы ебать')
async def meme(inter, mp3: commands.option_enum(listmp3)):
    await inter.response.send_message(mp3, delete_after=10)   
    # Добавляем в войс
    await join_to_voice(inter)
    # song_queue[inter.guild_id].insert()
    # newelement = [mp3, os.path.join(dirmp3, mp3)]
    # song_queue.append(newelement)

    newelement = {
        'name':mp3,
        'url':os.path.join(dirmp3, mp3),
        'img':'',
        'customer': inter.author.name
    }
    if not inter.guild_id in song_queue:
        song_queue[inter.guild_id] = []
    
    if song_queue[inter.guild_id]:
        song_queue[inter.guild_id].insert(0, newelement)
    song_queue[inter.guild_id].insert(0, newelement)
    voice = get(bot.voice_clients, guild=inter.guild)
    if not voice.is_playing():
        player(inter)
    else:
        voice.stop()


# Отображение после запуска
@bot.event  # check if bot is ready
async def on_ready():
    print('\n[{}] Logged in as: {} - {}'.format(datetime.datetime.today(),bot.user.name,bot.user.id))
    for guild in bot.guilds:
        print('Server {}. Member Count : {}'.format(guild.name,guild.member_count))
        # for member in guild.members:
        #     print (member)


# Logger
@bot.event
async def on_message(message):
    text="{},{},{}: {} {}".format(datetime.datetime.today(),message.channel,message.author,message.content,message.attachments)
    with open('{}.txt'.format(message.guild),'ab') as f:
        f.write(text.encode() + '\n'.encode())


# Дисконект если войс пустой
@bot.event
async def on_voice_state_update(member, before, after):
    voice = get(bot.voice_clients, guild=member.guild)
    if voice:
        if (len(voice.channel.members) == 1):
            await asyncio.sleep(300)
            if (len(voice.channel.members) == 1 & voice.is_connected()):
                print("Leave from {}, empty channel".format(member.guild))
                await voice.disconnect()


# Отправка команды только админам
# @bot.slash_command(default_member_permissions=disnake.Permissions(manage_guild=True, moderate_members=True))
# async def test(inter: disnake.ApplicationCommandInteraction):
#     print("1234")


# Тестовая команда
# @bot.slash_command(description='Тест')
# async def ping(inter, member: disnake.Member):
#     await inter.response.send_message('Pong', delete_after=1)
#     # if inter.user.id==213704988784984064:
#     #     await member.edit(mute=True)
#     print(inter.channel)


file = open('token.txt', 'r')
token = file.read()
file.close()
bot.run(token)