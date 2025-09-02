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

Перейти по ссылке в install Link, добавить бота на сервер

# Запуск в docker compose (готовый образ)

Установить [docker and docker compose](https://docs.docker.com/engine/install/ubuntu/#install-using-the-repository)

Создайте папку logs

Создать compose.yaml файл с содержимым
```
services:
  app:
    image: ghcr.io/atmega1337/djeban_discordbot:master
    restart: unless-stopped
    volumes:
      - /logs/:/app/logs/
    env_file:
      - .env
```

Создать файл .env в папке, где расположен compose.yaml
```
token=*You Token*
```

Выполнить в папке с compose.yaml:
```
docker compose up
```

# Запуск в docker compose (сборка)

Установить [docker and docker compose](https://docs.docker.com/engine/install/ubuntu/#install-using-the-repository)

Создать файл .env в корне с проектом
```
token=*You Token*
```

Выполнить в папке с проектом:
```
docker compose up
```

# Запуск windows
1. Установить [python](https://www.python.org/downloads/)

2. Установить [ffmpeg](https://ffmpeg.org/download.html):

Скачать и закинуть в одну из дирректорий PATH (например C:/Windows) или создать свою.

3. Создайте файл .env с токеном
```
token=*You Token*
```

4. Запустить start.bat

# Запуск linux
1. Установить python, python3-venv 

2. Установить ffmpeg и screen:


```
sudo apt install ffmpeg screen
chmod +x startscreen.sh
```

3. Создайте файл .env с токеном

```
token=*You Token*
```

4. Запустить файл
```
./startscreen.sh
```

5. Для автоматического запуска и перезапуска внести в crontab (**crontab -e**):
```
#@reboot cd /home/user/djeban; sh ./start.sh
#0 6 * * * cd /home/user/djeban; sh ./start.sh
```