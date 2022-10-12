# DJEBAN
Музыкальный бот для discord. Пока поддерживется только YouTube.

Проект находится в альфа версии!


# Команды
/play - включить

/stop - выключить, обнулить плейлист

/skip - пропустить песню.


/pause - поставить на паузу

/resume - продолжить

/join - добавить в войс чат

/leave - выйти из войс часа


/eban - отключить воспроизведение и включить djeban

# Установка
1. Установить python 3.10

2. В директории выполнить:
pip install -r requirements.txt

3. Установить [ffmpeg](https://ffmpeg.org/download.html):
В windows: скачать и закинуть в одну из дирректорий PATH (например C:/Windows) или создать свою.
В linux: sudo apt install ffmpeg

4. Запустить main.py, будет создан файл config.ini

5. [Создать бота](https://discord.com/developers/applications) и его токен вписать в config.ini

6. Запустить бота