FROM python:3.14-slim

WORKDIR /app

# Установка зависимостей
COPY requirements.txt .
RUN pip install -r requirements.txt -i https://mirrors.cloud.tencent.com/pypi/simple

# Копирование проекта
COPY . .

EXPOSE 8000
