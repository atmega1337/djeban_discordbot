import yt_dlp
from urllib.parse import urlparse
from urllib.parse import parse_qs

# from youtube_dl import YoutubeDL

def get(url, playlistcount=10):
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
        'ignoreerrors': True,
        'logtostderr': False,
        'quiet': True,
        'no_warnings': True,
        'default_search': 'auto',
        'source_address': '0.0.0.0',
    }


    if 'list' in url:
        YDL_OPTIONS['noplaylist']=False
        if 'index' in url:
            for i in url.split("&"):
                if 'index=' in i:
                    index=int(i[6::])
            YDL_OPTIONS['playliststart']=index
            YDL_OPTIONS['playlistend']=index+playlistcount
        else:
            YDL_OPTIONS['playlistend']=playlistcount

    with yt_dlp.YoutubeDL(YDL_OPTIONS) as ydl:
        info = ydl.extract_info(url, download=False)
    data=[]
    if 'entries' in info:
        for video in info['entries']:
            if video == None:
                continue
            i={
                'title': video['title'],
                'url': video['url'],
                'img': video['thumbnail']
            }
            data.append(i)
    else:
        i={
            'title': info['title'],
            'url': info['url'],
            'img': info['thumbnail']
        }
        data.append(i)
    return data

if __name__ == "__main__": 

    test=get("https://www.youtube.com/watch?v=J85jV37CsYE&list=PLJWF8BCq8piTlxeOPvVYbAM0Of5YQGigu&index=2&ab_channel=SathButtons")
    print(test)

