# 2026-VK-EDU-Web-13-Zhukov-K

**Жуков К. П. Группа 4**  
**Домашнее задание №6**

## Описание проекта
Веб-сервис для вопросов и ответов (клон Reddit/StackOverflow) на Django. 

### Что добавлено в рамках ДЗ №6:
1.  **Real-time обновления**: При добавлении нового ответа все пользователи на странице вопроса видят его мгновенно без перезагрузки страницы (используется **Centrifugo** и **Websockets**).
2.  **Фоновые задачи (Celery)**: Тяжелые операции вынесены в фон:
    *   Отправка Email-уведомлений автору вопроса о новом ответе.
    *   Обновление счетчиков ответов и активности пользователей.
    *   Инвалидация и прогрев кэша популярных тегов и пользователей по расписанию (**Celery Beat**).
3.  **Полнотекстовый поиск (PostgreSQL FTS)**:
    *   Поиск по заголовкам и контенту вопросов с использованием GIN-индексов.
    *   Поисковые подсказки в шапке сайта с поддержкой тегов (через `#`) и поддержкой **Debounce** на фронтенде (снижение нагрузки на сервер).

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

## Вариант 1: Запуск через Docker Compose (Рекомендуемый)

Убедитесь, что у вас установлены Docker и Docker Compose.

### 1. Настройка окружения
Создайте файл `.env.docker` на основе шаблона:
```bash
cp .env.example .env.docker
```
*В Docker-конфигурации уже прописаны верные имена хостов для взаимодействия контейнеров.*

### 2. Запуск всех сервисов
```bash
docker-compose up --build -d
```
Эта команда поднимет:
- **web**: Django (порт 8000)
- **db**: PostgreSQL 15
- **redis**: Брокер задач и Кэш
- **centrifugo**: Real-time сервер (порт 8001)
- **celery/celery-beat**: Воркеры и планировщик задач
- **maildev**: Интерфейс для просмотра исходящих писем (порт 1080)

### 3. Базовая настройка (миграции и заполнение БД)
```bash
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py fill_db 100
```

Сайт будет доступен по адресу: `http://127.0.0.1:8000/`

---

## Вариант 2: Локальный запуск

### 1. Подготовка
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env.local
```

### 2. Запуск окружения
1.  **Postgres & Redis**: Должны быть запущены как службы (`sudo service ... start`).
2.  **Centrifugo**: 
    ```bash
    ./centrifugo --config=config.json
    ```
3.  **Celery Worker**:
    ```bash
    celery -A application worker -l INFO
    ```
4.  **Django**:
    ```bash
    python manage.py migrate
    python manage.py fill_db [ratio]    # См. Вариант 1
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