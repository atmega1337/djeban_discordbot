# DJEBAN
Музыкальный бот для discord. Пока поддерживется только YouTube.

Проект находится в альфа версии!


# Команды
/play https://www.youtube.com/watch?v=  - включить воспроизведение

/stop - выключить, обнулить плейлист

/skip - пропустить песню.

/pause - поставить на паузу

/resume - продолжить

/join - добавить в войс чат

/leave - выйти из войс часа

/meme ** - Воспроизведение mp3 из папки

# Установка
1. Установить python 3.10


2. В директории выполнить:
pip install -r requirements.txt


3. Установить [ffmpeg](https://ffmpeg.org/download.html):

В windows: скачать и закинуть в одну из дирректорий PATH (например C:/Windows) или создать свою.

В linux: sudo apt install ffmpeg


4. [Создать бота](https://discord.com/developers/applications). 

В настройках включить: PRESENCE INTENT, SERVER MEMBERS INTENT, MESSAGE CONTENT INTENT


5. Пригласить бота на свой сервер

OAuth2 > URL Generator

SCOPES = bot

Выдать права (для теста можно administrator)

Перейти по ссылке, добавить бота


5. Создать папку mp3 (туда можно закидывать файлы), файл token.txt и вписать туда токен бота. 


6. Запустить бота
