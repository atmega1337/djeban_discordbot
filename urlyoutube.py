import yt_dlp


# from youtube_dl import YoutubeDL

def get(url):
    """
    Get youtube link and return title, url mp3, img
    """
    YDL_OPTIONS = {
        'format': 'bestaudio/best',
        'extractaudio': True,
        'audioformat': 'mp3',
        'outtmpl': 'downloads/%(extractor)s-%(id)s-%(title)s.%(ext)s',
        'restrictfilenames': True,
        'noplaylist': True,
        'nocheckcertificate': True,
        'ignoreerrors': False,
        'logtostderr': False,
        'quiet': True,
        'no_warnings': True,
        'default_search': 'auto',
        'source_address': '0.0.0.0',
    }
    with yt_dlp.YoutubeDL(YDL_OPTIONS) as ydl:
        info = ydl.extract_info(url, download=False)
    data={'title': info['title'], 'url': info['url'], 'img': info['thumbnail']}
    return data

if __name__ == "__main__": 
    test=get("https://www.youtube.com/watch?v=MV_3Dpw-BRY")
    print(test)
