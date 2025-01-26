FROM python:3.9
WORKDIR /app
RUN mkdir -p logs/chats
RUN apt-get update && apt install ffmpeg -y

COPY . .
RUN chmod +x startdocker.sh
CMD ["./startdocker.sh"]