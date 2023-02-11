import os
import sys
import disnake
import datetime
import asyncio
import urlyoutube

from disnake.ext import commands
from disnake import FFmpegPCMAudio
from disnake.utils import get

played = ""
song_queue = []

bot = commands.Bot(command_prefix='!', intents=disnake.Intents.all(), activity = disnake.Streaming(name='YouTube', url='https://www.youtube.com/watch?v='))



def playlistinfo():
    infolist = "Track: " 
    infolist += played 
    if song_queue:
        infolist += "\nPlaylist:\n"
        for n in range(len(song_queue)):
            infolist += str(n+1) + ') ' + song_queue[n][0] + "\n"
    return(infolist)

def addqueue(url='', author=''):
    data=urlyoutube.get(url)
    newelement = [data['title'], data['url'], author]
    song_queue.append(newelement)


def playqueue(voice):
    global played
    if(song_queue):
        FFMPEG_OPTIONS = {
            'before_options': '-nostdin',
            'options': '-vn'
        }
        
        voice.play(FFmpegPCMAudio(song_queue[0][1], **FFMPEG_OPTIONS), after=lambda e: playqueue(voice))
        voice.is_playing()
        played = song_queue[0][0]
        song_queue.pop(0)

async def join_to_voice(inter, channel=None):
    if not channel:
        try:
            channel = inter.author.voice.channel
        except AttributeError:
            msg='Please call `,join` from a voice channel.'
    
    vc = inter.guild.voice_client

    if vc:
        if vc.channel.id == channel.id:
            return
        await vc.move_to(channel)
        msg="Move to channel: **{}**".format(channel)
    else:
        await channel.connect()
        msg="Join to channel: **{}**".format(channel)
    print('Server {}. Author: {} Connect to voice: {}'.format(inter.guild,inter.author,channel))
    return msg

@bot.event  # check if bot is ready
async def on_ready():
    print('\n[{}] Logged in as: {} - {}'.format(datetime.datetime.today(),bot.user.name,bot.user.id))
    for guild in bot.guilds:
        print('Server {}. Member Count : {}'.format(guild.name,guild.member_count))
        # for member in guild.members:
        #     print (member)

@bot.slash_command(description='Тест')
async def ping(inter, member: disnake.Member):
    await inter.response.send_message('Pong', delete_after=1)
    # if inter.user.id==213704988784984064:
    #     await member.edit(mute=True)
    print(inter.channel)
    


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
    await inter.response.send_message('Author: {} play: {}'.format(inter.author,url), delete_after=30)
    # Добавляем в войс
    await join_to_voice(inter)

    voice = get(bot.voice_clients, guild=inter.guild)
    addqueue(url)
    if not voice.is_playing():
        playqueue(voice)
    await inter.send(playlistinfo(), delete_after=900)

@bot.slash_command(description='Продолжить')
async def resume(inter):
    voice = get(bot.voice_clients, guild=inter.guild)

    if not voice.is_playing():
        voice.resume()
        await inter.response.send_message("Bot is resuming", delete_after=10)


# command to pause voice if it is playing
@bot.slash_command(description='Поставить на паузу')
async def pause(inter):
    voice = get(bot.voice_clients, guild=inter.guild)

    if voice.is_playing():
        voice.pause()
        await inter.response.send_message("Bot has been paused", delete_after=10)


# command to stop voice
@bot.slash_command(description='Скип говна, если DJ ебан')
async def skip(inter):
    voice = get(bot.voice_clients, guild=inter.guild)

    if voice.is_playing():
        voice.stop()
        await inter.response.send_message(playlistinfo(), delete_after=10)

# command to stop voice
@bot.slash_command(description='Стоп')
async def stop(inter):
    voice = get(bot.voice_clients, guild=inter.guild)

    if voice.is_playing():
        song_queue.clear()
        voice.stop()
        await inter.response.send_message("Stopping...", delete_after=10)

dirmp3=os.path.join(os.path.dirname(sys.argv[0]),'mp3')
listmp3 = os.listdir(dirmp3)
print(listmp3)

@bot.slash_command(description='Мемы ебать')
async def meme(inter, mp3: commands.option_enum(listmp3)):
    # Добавляем в войс
    await join_to_voice(inter)

    song_queue.clear()
    newelement = [mp3, os.path.join(dirmp3, mp3)]
    song_queue.append(newelement)

    voice = get(bot.voice_clients, guild=inter.guild)
    voice.stop()
    playqueue(voice)
    await inter.response.send_message(mp3, delete_after=10)

# Logger
@bot.event
async def on_message(message):
    text="{},{},{}: {} {}".format(datetime.datetime.today(),message.channel,message.author,message.content,message.attachments)
    with open('{}.txt'.format(message.guild),'ab') as f:
        f.write(text.encode() + '\n'.encode())

@bot.event
async def on_voice_state_update(member, before, after):
    voice = get(bot.voice_clients, guild=member.guild)
    if voice:
        if (len(voice.channel.members) == 1):
            await asyncio.sleep(10)
            if (len(voice.channel.members) == 1 & voice.is_connected()):
                await voice.disconnect()

file = open('token.txt', 'r')
token = file.read()
file.close()
bot.run(token)