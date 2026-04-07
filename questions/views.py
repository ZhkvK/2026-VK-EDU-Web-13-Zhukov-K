from django.shortcuts import render
from django.http import HttpResponse
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

QUESTIONS = [
    {
        'id': i,
        'title': f"Вопрос {i}",
        'text': f"Текст для вопроса {i}",
        'answers': 3,
        'update': "3 минуты",
        'tags': ["tag1", "tag2", "tag3", "tag4"],
        'votes': [12, 2]
    }
    for i in range (1, 30)
]

# Заглушка для текущего пользователя (для шапки)
CURRENT_USER = {
    'username': 'Username',
    'is_authenticated': True,
}

# Заглушка для вопроса
QUESTION = {
    'id': 1,
    'title': 'Как настроить favicon в Bootstrap?',
    'text': '''This is a wider card with supporting text below as a natural lead-in to additional content. This content is a little bit longer.
    
Можно использовать несколько абзацев для детального описания проблемы.''',
    'author': {'username': 'Username'},
    'created_at': '3 часа назад',
    'tags': ['python', 'django', 'html'],
    'votes': [50, 0],
    'answers_count': 3,
    # Права доступа (для отображения кнопок Редактировать/Удалить)
    'can_edit': True,
    'can_delete': True,
}

# Заглушка для ответов с вложенными комментариями
ANSWERS = [
    {
        'id': 1,
        'text': 'This is a wider card with supporting text below as a natural lead-in to additional content. This content is a little bit longer.',
        'author': {'username': 'User1'},
        'updated_at': 'Обновлен 3 минуты назад',
        'votes': [50, 0],
        'is_correct': False,
        'comments': [
            {
                'id': 101,
                'author': {'username': 'User2'},
                'created_at': '1 час назад',
                'text': 'Спасибо за ответ! Это помогло.',
                'votes': [50, 0],
            },
            {
                'id': 102,
                'author': {'username': 'User1'},
                'created_at': '30 мин назад',
                'text': 'Рад, что помогло! Обращайтесь.',
                'votes': [50, 0],
            },
            {
                'id': 103,
                'author': {'username': 'User3'},
                'created_at': '10 мин назад',
                'text': 'А можно пример кода?',
                'votes': [50, 0],
            },
        ],
    },
    {
        'id': 2,
        'text': 'This is a wider card with supporting text below as a natural lead-in to additional content. This content is a little bit longer.',
        'author': {'username': 'User2'},
        'updated_at': 'Обновлен 3 минуты назад',
        'votes': [50, 0],
        'is_correct': False,
        'comments': [
            {
                'id': 201,
                'author': {'username': 'User2'},
                'created_at': '1 час назад',
                'text': 'Спасибо за ответ! Это помогло.',
                'votes': [50, 0],
            },
            {
                'id': 202,
                'author': {'username': 'User1'},
                'created_at': '30 мин назад',
                'text': 'Рад, что помогло! Обращайтесь.',
                'votes': [50, 0],
            },
            {
                'id': 203,
                'author': {'username': 'User3'},
                'created_at': '10 мин назад',
                'text': 'А можно пример кода?',
                'votes': [50, 0],
            },
        ],
    },
]

# Заглушка для боковой панели (теги и пользователи)
POPULAR_TAGS = ['python', 'javascript', 'html', 'css', 'bootstrap', 'django', 'react', 'sql']

TOP_USERS = [
    {'username': 'User1', 'reputation': 1234},
    {'username': 'User2', 'reputation': 987},
    {'username': 'User3', 'reputation': 756},
]

def paginate(objects_list, request, per_page=10):
    page_number = request.GET.get('page')
    paginator = Paginator(objects_list, per_page)
    try:
        page = paginator.page(page_number)
    except PageNotAnInteger:
        page = paginator.page(1)
    except EmptyPage:
        page = paginator.page(paginator.num_pages)
    return page

# Create your views here.
def index(request):
    page_obj = paginate(QUESTIONS, request)
    return render(request, 'questions/index.html', context={'questions': page_obj.object_list, 'page_obj': page_obj, 'popular_tags': POPULAR_TAGS, 'top_users': TOP_USERS})

def hot(request):
    page_obj = paginate(QUESTIONS, request)
    return render(request, 'questions/hot.html', context={'questions': page_obj.object_list, 'page_obj': page_obj, 'popular_tags': POPULAR_TAGS, 'top_users': TOP_USERS})

def ask(request):
    return render(request, 'questions/ask.html', context={'popular_tags': POPULAR_TAGS, 'top_users': TOP_USERS})

def question(request):
    page_obj = paginate(ANSWERS, request)
    return render(request, 'questions/question.html', context={'question': QUESTION, 'answers': page_obj.object_list, 'page_obj': page_obj, 'popular_tags': POPULAR_TAGS, 'top_users': TOP_USERS})

