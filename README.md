# 2026-VK-EDU-Web-13-Zhukov-K

**Жуков К. П. Группа 4**  
**Домашнее задание №5**

## Описание проекта
Веб-сервис для вопросов и ответов (клон Reddit/StackOverflow) на Django. 
В рамках пятого ДЗ добавлены AJAX-запросы с валидацией и проверкой CSRF-токенов для лайков/дизлайков, чекбоксов правильного ответа и для подгрузки комментариев к ответу. Так же была добавлена работа с картинками (аватарами) -- загрузка с валидацией по размеру и типу файла, изменение названия с сохранением в MEDIA_ROOT/avatars/user_id/ и корректное отображение через url картинки.



## Список страниц

| Страница | Файл шаблона | URL |
|----------|--------------|-----|
| Главная (список вопросов) | `questions/index.html` | `/` |
| Горячие вопросы | `questions/hot.html` | `/hot/` |
| Страница вопроса | `questions/question.html` | `/question/<int:question_id>/` |
| Создание вопроса | `questions/ask.html` | `/ask/` |
| Вход | `core/login.html` | `/auth/login/` |
| Регистрация | `core/signup.html` | `/auth/signup/` |
| Профиль пользователя | `core/profile.html` | `/auth/profile/` |
| Поиск по тегу | `questions/tag.html` | `/tag/<str:tag_name>/` |

---

## Вариант 1: Запуск через Docker Compose (Рекомендуемый)

Это самый простой способ запуска, включающий в себя настроенную БД PostgreSQL.

### 1. Настройка окружения
Создайте файл `.env.docker` на основе примера. Впишите туда свои логины и пароли.
```bash
# Для Linux/macOS
cp .env.example .env.docker

# Для Windows
Copy-Item .env.example -Destination .env.docker
```

### 2. Сборка и запуск контейнеров
```bash
docker-compose up --build -d
```

### 3. Применение миграций
```bash
docker-compose exec web python manage.py migrate
```

### 4. Генерация тестовых данных (опционально)
Заполнение БД происходит через кастомную команду. Параметр ratio — это коэффициент генерации. После применения команды в базу должно быть добавлено:
- пользователей — равное ratio;
- вопросов — ratio * 10;
- ответы — ratio * 100;
- тэгов - ratio;
- оценок пользователей - ratio * 200;
```bash
docker-compose exec web python manage.py fill_db 100
```

Сайт будет доступен по адресу: `http://127.0.0.1:8000/`

---

## Вариант 2: Локальный запуск (Для разработки)

*Внимание: для локального запуска у вас должен быть установлен и запущен PostgreSQL на порту 5432.*

### 1. Виртуальное окружение и зависимости
```bash
python -m venv venv
# Активация: 
venv\Scripts\activate       # (Win)
source venv/bin/activate    # (Mac/Linux)
pip install -r requirements.txt
```

### 2. Настройка окружения
Создайте файл `.env.local` и укажите данные для подключения к вашей локальной БД Postgres.
```bash
cp .env.example .env.local
```
*(В файле `.env.local` убедитесь, что `DB_HOST=127.0.0.1`)*

### 3. Миграции и заполнение БД
```bash
python manage.py migrate
python manage.py fill_db [ratio]    # См. Вариант 1
```

### 4. Запуск сервера
```bash
python manage.py runserver
```
---

## Структура проекта

```text
.
├── application/          # Главный проект Django (settings, urls)
├── core/                 # Приложение пользователей (auth, profile)
├── questions/            # Приложение Q&A (models, views, managers)
│   └── management/       
│       └── commands/     
│           └── fill_db.py # Скрипт генерации данных
├── media/                # Пользовательские файлы (аватары)
├── requirements.txt      # Зависимости Python
├── docker-compose.yml    # Конфигурация Docker Compose (web + db)
├── Dockerfile            # Инструкция сборки web-контейнера
└── .env.example          # Шаблон переменных окружения
```

## Зависимости

```text
asgiref==3.11.1
beautifulsoup4==4.14.3
certifi==2026.4.22
charset-normalizer==3.4.7
Django==4.2.30
django-bootstrap-v5==1.0.11
django-bootstrap5==26.2
django-debug-toolbar==6.3.0
django-environ==0.13.0
Faker==40.15.0
idna==3.13
packaging==26.2
pillow==12.2.0
psycopg2-binary==2.9.12
python-decouple==3.8
requests==2.33.1
soupsieve==2.8.3
sqlparse==0.5.5
typing_extensions==4.15.0
tzdata==2026.1
urllib3==2.6.3
vsixget==0.1.0
```