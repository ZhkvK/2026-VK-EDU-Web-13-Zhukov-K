from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, Http404
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

QUESTIONS = [
    {
        'id': i,
        'title': f"Вопрос {i}",
        'text': f"Текст для вопроса {i}",
        'answers': 3,
        'update': "3 минуты",
        'tags': ['python', 'javascript', 'html', 'css', 'bootstrap', 'django', 'react', 'sql'],
        'votes': [12, 2]
    }
    for i in range (1, 30)
]

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
        'is_correct': True,
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
    {
        'id': 3,
        'text': 'This is a wider card with supporting text below as a natural lead-in to additional content. This content is a little bit longer.',
        'author': {'username': 'User3'},
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

USER_UNAUTHORIZED = {
    'username': "Dr.Pepper",
    'email': "dr.pepper@example.com",
    'avatar_image': "questions/img/Logo.png",
    'about': "Привет! Я увлекаюсь программированием и технологиями.",
    'is_Authorized': False
}

def paginate(objects_list, request, per_page=2):
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
    return render(request, 'questions/index.html', context={
        'questions': page_obj.object_list,
        'page_obj': page_obj,
        'popular_tags': POPULAR_TAGS,
        'top_users': TOP_USERS,
        'user': USER_UNAUTHORIZED
        })

def hot(request):
    page_obj = paginate(QUESTIONS[::-1], request)
    return render(request, 'questions/hot.html', context={
        'questions': page_obj.object_list,
        'page_obj': page_obj,
        'popular_tags': POPULAR_TAGS,
        'top_users': TOP_USERS,
        'user': USER_UNAUTHORIZED
        })

def ask(request):
    return render(request, 'questions/ask.html', context={
        'popular_tags': POPULAR_TAGS,
        'top_users': TOP_USERS,
        'user': USER_UNAUTHORIZED
        })

def question(request, question_id):
    question_data = None
    for q in QUESTIONS:
        # Убеждаемся, что такой ответ существует и дальше передаем его в контекст, 
        # но сейчас подставлена заглушка QUESTION на любой существующий id
        if q['id'] == question_id:
            question_data = q
            break
    if not question_data:
        raise Http404("Вопрос не найден")
    page_obj = paginate(ANSWERS, request)
    return render(request, 'questions/question.html', context={
        'question': QUESTION,
        'answers': page_obj.object_list,
        'page_obj': page_obj,
        'popular_tags': POPULAR_TAGS,
        'top_users': TOP_USERS,
        'user': USER_UNAUTHORIZED
        })

def search(request):
    tag = request.GET.get('tag', '').strip()
    if tag:
        return redirect('questions:tag', tag)
    return redirect('questions:index')

def tag(request, tag):
    found_questions = [q for q in QUESTIONS if tag in q.get('tags', [])]
    page_obj = paginate(found_questions, request)
    return render(request, 'questions/tag.html', context={
        'search_query': tag,
        'questions': page_obj.object_list,
        'page_obj': page_obj,
        'popular_tags': POPULAR_TAGS,
        'top_users': TOP_USERS,
        'user': USER_UNAUTHORIZED
        })
            
    