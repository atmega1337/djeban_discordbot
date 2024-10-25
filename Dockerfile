FROM python:3.9
WORKDIR /app
COPY . .
RUN apt-get update && apt install ffmpeg -y
RUN pip install --upgrade pip
RUN pip install --no-cache-dir --upgrade -r requirements.txt

CMD ["python", "main.py"]