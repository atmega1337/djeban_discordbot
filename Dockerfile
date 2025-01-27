#FROM python:slim
FROM python:alpine
WORKDIR /app
RUN mkdir -p logs/chats
#RUN apt-get update && apt install ffmpeg -y
RUN apk update && apk add --no-cache ffmpeg opus

COPY . .
RUN chmod +x startdocker.sh
CMD ["./startdocker.sh"]