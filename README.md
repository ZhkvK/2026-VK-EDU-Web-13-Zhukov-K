# 2026-VK-EDU-Web-13-Zhukov-K

**Жуков К. П. Группа 4**  
**Домашнее задание №2**

## Описание проекта

Веб-сервис для вопросов и ответов на Django.

## Список страниц

| Страница | Файл шаблона | URL |
|----------|--------------|-----|
| Главная (список вопросов) | `questions/index.html` | `/` |
| Страница вопроса | `questions/question.html` | `/question/<int:id>/` |
| Создание вопроса | `questions/ask.html` | `/ask/` |
| Вход | `core/login.html` | `/auth/login/` |
| Регистрация | `core/signup.html` | `/auth/signup/` |
| Профиль | `core/profile.html` | `/auth/profile/` |
| Поиск по тегу | `questions/tag.html` | `/tag/<str:tag>/` |

---

## Вариант 1: Локальный запуск

### 1. Создание виртуального окружения

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 2. Установка зависимостей

```bash
pip install -r requirements.txt
```

### 3. Настройка переменных окружения
Проект использует переменные окружения. Создайте файл `.env` на основе примера:
```bash
# Для Linux/macOS
cp .env.example .env

# Для Windows (в PowerShell)
Copy-Item .env.example -Destination .env
```

### 4. Запуск сервера

```bash
python manage.py runserver
```

### 5. Открыть в браузере
`http://127.0.0.1:8000/`

---

## Вариант 2: Запуск через Docker Compose

### 1. Требования

- Установленный Docker
- Установленный Docker Compose

### 2. Сборка и запуск контейнера

```bash
docker compose up --build
```

### 3. Открыть в браузере


`http://127.0.0.1:8000/


---

## Структура проекта

```
.
├── application/          # Главный проект Django (settings, urls)
├── core/                 # Приложение авторизации (login, signup, profile)
├── questions/            # Приложение вопросов и ответов
├── media/                # Загруженные файлы
├── static/               # Статические файлы
├── manage.py             # Утилита управления Django
├── requirements.txt      # Зависимости Python
├── Dockerfile            # Конфигурация Docker
└── docker-compose.yaml   # Конфигурация Docker Compose
```

---

## Зависимости

См. файл `requirements.txt`:

```
asgiref==3.11.1
Django==6.0.3
python-decouple==3.8
sqlparse==0.5.5
```
