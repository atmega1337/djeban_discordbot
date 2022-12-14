import disnake

from disnake.ext import commands
from disnake import FFmpegPCMAudio
from disnake.utils import get
from youtube_dl import YoutubeDL

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

def addqueue(url=''):
    YDL_OPTIONS = {
        'format': 'bestaudio/best',
        'outtmpl': 'downloads/%(extractor)s-%(id)s-%(title)s.%(ext)s',
        'restrictfilenames': True,
        'noplaylist': True,
        'nocheckcertificate': True,
        'ignoreerrors': False,
        'logtostderr': False,
        'quiet': True,
        'no_warnings': True,
        'default_search': 'auto',
        'source_address': '0.0.0.0'  # ipv6 addresses cause issues sometimes
    }
    with YoutubeDL(YDL_OPTIONS) as ydl:
        info = ydl.extract_info(url, download=False)
    newelement = [info['title'], info['url']]
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
    print(f'\n\nLogged in as: {bot.user.name} - {bot.user.id}')
    for guild in bot.guilds:
        print('Server {}. Member Count : {}'.format(guild.name,guild.member_count))

@bot.slash_command(description='????????')
async def ping(inter):
    await inter.response.send_message('pong')


@bot.slash_command(description='?????????????????????? ?? ???????? ????????')
async def join(inter, channel: disnake.VoiceChannel=None):
    msg= await join_to_voice(inter, channel)
    await inter.response.send_message(msg, delete_after=10)


@bot.slash_command(description='?????????? ???? ??????????')
async def leave(inter):
    print('Server {}. Author: {} Leave voice.'.format(inter.guild,inter.author))
    await inter.guild.voice_client.disconnect(force=True)
    await inter.response.send_message("Leave voice.", delete_after=10)


@bot.slash_command(description='???????????????? ?????????? ?? ??????????')
async def play(inter, url):
    print('Server {}. Author: {} play: {}'.format(inter.guild,inter.author,url))
    # ???????????????? ?????????????? ???????? ?? ??????????, ?? ???????????? ???????? ??????????????????
    await join_to_voice(inter)

    voice = get(bot.voice_clients, guild=inter.guild)
    if not voice.is_playing():
        addqueue(url)
        playqueue(voice)
    else:
        addqueue(url)
    await inter.response.send_message(playlistinfo(), delete_after=300)

@bot.slash_command(description='????????????????????')
async def resume(inter):
    voice = get(bot.voice_clients, guild=inter.guild)

    if not voice.is_playing():
        voice.resume()
        await inter.response.send_message("Bot is resuming", delete_after=10)


# command to pause voice if it is playing
@bot.slash_command(description='?????????????????? ???? ??????????')
async def pause(inter):
    voice = get(bot.voice_clients, guild=inter.guild)

    if voice.is_playing():
        voice.pause()
        await inter.response.send_message("Bot has been paused", delete_after=10)


# command to stop voice
@bot.slash_command(description='???????? ??????????, ???????? DJ ????????')
async def skip(inter):
    voice = get(bot.voice_clients, guild=inter.guild)

    if voice.is_playing():
        voice.stop()
        await inter.response.send_message(playlistinfo(), delete_after=10)

# command to stop voice
@bot.slash_command(description='????????')
async def stop(inter):
    voice = get(bot.voice_clients, guild=inter.guild)

    if voice.is_playing():
        song_queue.clear()
        voice.stop()
        await inter.response.send_message("Stopping...", delete_after=10)



@bot.slash_command(description='???????? + ?????????????? DJ, ?????? ???? ????????')
async def eban(inter):
    if not inter.guild.voice_client:
        await inter.author.voice.channel.connect()
        
    voice = get(bot.voice_clients, guild=inter.guild)
    song_queue.clear()
    addqueue("https://www.youtube.com/watch?v=aGob2BwZvmI")
    voice.stop()
    playqueue(voice)
    await inter.response.send_message("DJ ????????!!", delete_after=10)

file = open('token.txt', 'r')
token = file.read()
file.close()
bot.run(token)