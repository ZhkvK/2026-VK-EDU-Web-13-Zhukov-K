# syntax=docker/dockerfile:1
FROM python:3.14-slim

WORKDIR /app

# Установка зависимостей
COPY requirements.txt .
RUN pip install -r requirements.txt

EXPOSE 8000
