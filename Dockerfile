FROM python:3.11-slim

WORKDIR /app

# Установка зависимостей
COPY requirements.txt .
RUN pip install -r requirements.txt -i https://mirrors.cloud.tencent.com/pypi/simple

# Копирование проекта
COPY . .

# Создание папки для медиа (если нет)
RUN mkdir -p /app/media

EXPOSE 8000