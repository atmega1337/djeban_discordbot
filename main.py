import disnake
from disnake.ext import commands
from disnake import FFmpegPCMAudio
from disnake.utils import get
from youtube_dl import YoutubeDL

bot = commands.Bot(command_prefix='!', intents=disnake.Intents.all(), activity = disnake.Game('test', status = disnake.Status.online))

song_queue = []

def playlistinfo():
    infolist = "Playlist:\n"
    for n in range(len(song_queue)):
        infolist += str(n+1) + ') ' + song_queue[n][0] + "\n"
    print(infolist)
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
    if(song_queue):
        print(voice)
        FFMPEG_OPTIONS = {
            'before_options': '-nostdin',
            'options': '-vn'
        }
        
        voice.play(FFmpegPCMAudio(song_queue[0][1], **FFMPEG_OPTIONS), after=lambda e: playqueue(voice))
        voice.is_playing()
        song_queue.pop(0)


@bot.event  # check if bot is ready
async def on_ready():
    print(f'\n\nLogged in as: {bot.user.name} - {bot.user.id}')
    for guild in bot.guilds:
        print('Server {}. Member Count : {}'.format(guild.name,guild.member_count))



@bot.slash_command(description='Тест')
async def ping(inter):
    await inter.response.send_message('pong')



@bot.slash_command(description='Подключение к войс чату')
async def join(inter):
    print('Server {}. Author: {} Connect to voice: {}'.format(inter.guild,inter.author,inter.author.voice.channel))
    if (inter.author.voice):
        await inter.author.voice.channel.connect()
        await inter.response.send_message("Connected", delete_after=10)
    else:
        await inter.response.send_message("Please Join Voice channel to run this command", delete_after=10)

@bot.slash_command(description='Выйти из войса')
async def leave(inter):
    print('Server {}. Author: {} Leave voice.'.format(inter.guild,inter.author))
    await inter.guild.voice_client.disconnect(force=True)
    await inter.response.send_message("Leave voice.", delete_after=10)

@bot.slash_command(description='Включить говно с ютуба')
async def play(inter, url):
    # Проверка наличия бота в войсе, в случае чего добовляем
    if not inter.guild.voice_client:
        await inter.author.voice.channel.connect()

    voice = get(bot.voice_clients, guild=inter.guild)
    if not voice.is_playing():
        addqueue(url)
        playqueue(voice)
    else:
        addqueue(url)
    await inter.response.send_message(playlistinfo(), delete_after=300)

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
        await inter.response.send_message("playlistinfo()", delete_after=10)

# command to stop voice
@bot.slash_command(description='Стоп')
async def stop(inter):
    voice = get(bot.voice_clients, guild=inter.guild)

    if voice.is_playing():
        song_queue.clear()
        voice.stop()
        await inter.response.send_message("Stopping...", delete_after=10)



@bot.slash_command(description='Стоп + сказать DJ, что он ебан')
async def eban(inter):
    if not inter.guild.voice_client:
        await inter.author.voice.channel.connect()
        
    voice = get(bot.voice_clients, guild=inter.guild)
    song_queue.clear()
    addqueue("https://www.youtube.com/watch?v=aGob2BwZvmI")
    voice.stop()
    playqueue(voice)
    await inter.response.send_message("DJ ЕБАН!!", delete_after=10)

file = open('token.txt', 'r')
token = file.read()
file.close()
bot.run(token)