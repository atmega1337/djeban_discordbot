# DJEBAN
Музыкальный бот для discord. Пока поддерживется только YouTube.

# Команды
/play https://www.youtube.com/watch?v=  - включить воспроизведение

/stop - выключить, обнулить плейлист

/skip - пропустить песню.

/pause - поставить на паузу

/resume - продолжить

/join - добавить в войс чат

/leave - выйти из войс часа

# Создание бота и .env файла

1. [Создать бота](https://discord.com/developers/applications). 

В настройках включить: PRESENCE INTENT, SERVER MEMBERS INTENT, MESSAGE CONTENT INTENT


2. Пригласить бота на свой сервер

> Installation:
```
Guild install = ON

install Link:
Discord Provided Link

Default Install Settings:
Scopes: applications.commands, bot
Permissions: Administrator
```

Перейти по ссылке в install Link, добавить бота


3. Создать файл .env в корне с проектом
```
token=*You Token*
proxy=http://127.0.0.1:1080 (прокси, работает только под windows)
```

# Запуск в docker

Установить [docker and docker compose](https://docs.docker.com/engine/install/ubuntu/#install-using-the-repository)

Выполнить в папке с проектом:
```
docker compose up
```

# Запуск windows
1. Установить [python](https://www.python.org/downloads/)

2. Установить [ffmpeg](https://ffmpeg.org/download.html):

Скачать и закинуть в одну из дирректорий PATH (например C:/Windows) или создать свою.

3. Запустить start.bat

# Запуск linux
1. Установить python, python3-venv 

2. Установить ffmpeg и screen:


```
sudo apt install ffmpeg screen
chmod +x startscreen.sh
```

3. Запустить файл
```
./startscreen.sh
```

4. Для автоматического запуска и перезапуска внести в crontab (> **crontab -e**):
```
#@reboot cd /home/user/djeban; sh ./start.sh
#0 6 * * * cd /home/user/djeban; sh ./start.sh
```