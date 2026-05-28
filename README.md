# 2026-VK-EDU-Web-13-Zhukov-K

**Жуков К. П. Группа 4**  
**Домашнее задание №7**

## Описание проекта
Веб-сервис для вопросов и ответов (клон Reddit/StackOverflow) на Django. 

### Что добавлено в рамках ДЗ №7:
1.  **Gunicorn**: Приложение запускается через WSGI-сервер Gunicorn (используется 2 воркера, таймаут 120с).
2.  **Nginx как Reverse Proxy**: 
    *   Проксирование динамических запросов на Gunicorn (с балансировкой нагрузки между инстансами).
    *   **Отдача статики и медиа**: Настроена эффективная раздача файлов по расширениям и префиксам (gzip, кэширование).
    *   **Proxy Cache**: Настроено кэширование ответов бэкенда, что кратно увеличивает производительность.
3.  **Автономный WSGI**: Реализован легковесный WSGI-скрипт (`mywsgi.py`) для демонстрации работы протокола без Django.
4.  **Нагрузочное тестирование**: Проведено сравнение производительности Nginx и Gunicorn с помощью `ab`.

**Отчет нагрузочного тестирования приведен в [файле](PerformanceReport.md).**

---

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

## Запуск через Docker Compose

Убедитесь, что у вас установлены Docker и Docker Compose.

### 1. Настройка окружения
Создайте файл `.env.docker` на основе шаблона:
```bash
cp .env.example .env.docker
cp config.json.example config.json
```
*В Docker-конфигурации уже прописаны верные имена хостов для взаимодействия контейнеров. В файле config.json содержатся настройки неймспейсов и доступов для Centrifugo.*

### 2. Запуск всех сервисов
```bash
docker-compose up --build -d
```
*Команда автоматически соберет статику, применит миграции (если настроен entrypoint) и поднимет Nginx, Gunicorn, Postgres, Redis, Celery и Centrifugo.*

### 3. Базовая настройка (миграции и заполнение БД)
```bash
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py fill_db 100
```

Сайт будет доступен по адресу: `http://127.0.0.1/`

---

## Структура проекта

```text
.
├── conf/
│   ├── nginx_docker.conf # Конфиг Nginx для контейнера
|   └── gunicorn.py       # Конфигурация Gunicorn (workers=2, timeout=120)
├── application/          # Настройки
├── core/                 # Приложение пользователей (auth, profile)
├── questions/            # Приложение Q&A (models, views, managers, tasks)
├── mywsgi.py             # Автономный WSGI-скрипт
├── docker-compose.yml    # Описание всей инфраструктуры (web, db, redis, nginx...)
└── Dockerfile            # Сборка на базе python:3-14
```

---

## Зависимости

```text
aiohappyeyeballs==2.6.2
aiohttp==3.13.5
aiosignal==1.4.0
amqp==5.3.1
annotated-types==0.7.0
asgiref==3.11.1
attrs==26.1.0
beautifulsoup4==4.14.3
billiard==4.2.4
celery==5.6.3
celery-redbeat==2.3.3
cent==5.2.0
certifi==2026.4.22
cffi==2.0.0
charset-normalizer==3.4.7
click==8.4.1
click-didyoumean==0.3.1
click-plugins==1.1.1.2
click-repl==0.3.0
cryptography==48.0.0
Django==6.0.5
django-bootstrap5==26.2
django-debug-toolbar==6.3.0
django-environ==0.13.0
Faker==40.15.0
frozenlist==1.8.0
gunicorn==26.0.0
hiredis==3.3.1
idna==3.13
kombu==5.6.2
multidict==6.7.1
packaging==26.2
pillow==12.2.0
prompt_toolkit==3.0.52
propcache==0.5.2
psycopg2-binary==2.9.12
pycparser==3.0
pydantic==2.13.4
pydantic_core==2.46.4
PyJWT==2.13.0
python-dateutil==2.9.0.post0
python-decouple==3.8
redis==7.4.0
requests==2.33.1
six==1.17.0
soupsieve==2.8.3
sqlparse==0.5.5
tenacity==9.1.4
types-requests==2.33.0.20260518
typing-inspection==0.4.2
typing_extensions==4.15.0
tzdata==2026.1
tzlocal==5.3.1
urllib3==2.6.3
vine==5.1.0
vsixget==0.1.0
wcwidth==0.7.0
yarl==1.24.2
```