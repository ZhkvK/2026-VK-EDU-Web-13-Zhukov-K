from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, Http404, JsonResponse
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.views.generic import TemplateView, RedirectView
from django.urls import reverse

from questions.models import Question, Tag, Answer, Comment


# QUESTIONS = [
#     {
#         'id': i,
#         'title': f"Вопрос {i}",
#         'text': f"Текст для вопроса {i}",
#         'answers': 3,
#         'update': "3 минуты",
#         'tags': ['python', 'javascript', 'html', 'css', 'bootstrap', 'django', 'react', 'sql'],
#         'votes': [12, 2]
#     }
#     for i in range (1, 30)
# ]

# Заглушка для вопроса
# QUESTION = {
#     'id': 1,
#     'title': 'Как настроить favicon в Bootstrap?',
#     'text': '''This is a wider card with supporting text below as a natural lead-in to additional content. This content is a little bit longer.
    
# Можно использовать несколько абзацев для детального описания проблемы.''',
#     'author': {'username': 'Username'},
#     'created_at': '3 часа назад',
#     'tags': ['python', 'django', 'html'],
#     'votes': [50, 0],
#     'answers_count': 3,
#     # Права доступа (для отображения кнопок Редактировать/Удалить)
#     'can_edit': True,
#     'can_delete': True,
# }

# Заглушка для ответов с вложенными комментариями
# ANSWERS = [
#     {
#         'id': 1,
#         'text': 'This is a wider card with supporting text below as a natural lead-in to additional content. This content is a little bit longer.',
#         'author': {'username': 'User1'},
#         'updated_at': 'Обновлен 3 минуты назад',
#         'votes': [50, 0],
#         'is_correct': True,
#         'comments': [
#             {
#                 'id': 101,
#                 'author': {'username': 'User2'},
#                 'created_at': '1 час назад',
#                 'text': 'Спасибо за ответ! Это помогло.',
#                 'votes': [50, 0],
#             },
#             {
#                 'id': 102,
#                 'author': {'username': 'User1'},
#                 'created_at': '30 мин назад',
#                 'text': 'Рад, что помогло! Обращайтесь.',
#                 'votes': [50, 0],
#             },
#             {
#                 'id': 103,
#                 'author': {'username': 'User3'},
#                 'created_at': '10 мин назад',
#                 'text': 'А можно пример кода?',
#                 'votes': [50, 0],
#             },
#         ],
#     },
#     {
#         'id': 2,
#         'text': 'This is a wider card with supporting text below as a natural lead-in to additional content. This content is a little bit longer.',
#         'author': {'username': 'User2'},
#         'updated_at': 'Обновлен 3 минуты назад',
#         'votes': [50, 0],
#         'is_correct': False,
#         'comments': [
#             {
#                 'id': 201,
#                 'author': {'username': 'User2'},
#                 'created_at': '1 час назад',
#                 'text': 'Спасибо за ответ! Это помогло.',
#                 'votes': [50, 0],
#             },
#             {
#                 'id': 202,
#                 'author': {'username': 'User1'},
#                 'created_at': '30 мин назад',
#                 'text': 'Рад, что помогло! Обращайтесь.',
#                 'votes': [50, 0],
#             },
#             {
#                 'id': 203,
#                 'author': {'username': 'User3'},
#                 'created_at': '10 мин назад',
#                 'text': 'А можно пример кода?',
#                 'votes': [50, 0],
#             },
#         ],
#     },
#     {
#         'id': 3,
#         'text': 'This is a wider card with supporting text below as a natural lead-in to additional content. This content is a little bit longer.',
#         'author': {'username': 'User3'},
#         'updated_at': 'Обновлен 3 минуты назад',
#         'votes': [50, 0],
#         'is_correct': False,
#         'comments': [
#             {
#                 'id': 201,
#                 'author': {'username': 'User2'},
#                 'created_at': '1 час назад',
#                 'text': 'Спасибо за ответ! Это помогло.',
#                 'votes': [50, 0],
#             },
#             {
#                 'id': 202,
#                 'author': {'username': 'User1'},
#                 'created_at': '30 мин назад',
#                 'text': 'Рад, что помогло! Обращайтесь.',
#                 'votes': [50, 0],
#             },
#             {
#                 'id': 203,
#                 'author': {'username': 'User3'},
#                 'created_at': '10 мин назад',
#                 'text': 'А можно пример кода?',
#                 'votes': [50, 0],
#             },
#         ],
#     },
# ]

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

class ListNewQuestionsView(TemplateView):
    template_name = "questions/index.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        questions = Question.objects.get_new()
        page_obj = paginate(questions, self.request)
        context.update({
            'questions': page_obj.object_list,
            'page_obj': page_obj,
            'popular_tags': POPULAR_TAGS,
            'top_users': TOP_USERS,
            'user': USER_UNAUTHORIZED
        })
        return context
    
class ListHotQuestionsView(TemplateView):
    template_name = "questions/hot.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        questions = Question.objects.get_hot()
        page_obj = paginate(questions, self.request)
        context.update({
            'questions': page_obj.object_list,
            'page_obj': page_obj,
            'popular_tags': POPULAR_TAGS,
            'top_users': TOP_USERS,
            'user': USER_UNAUTHORIZED
        })
        return context      

class AskFormView(TemplateView):
    template_name = "questions/ask.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'popular_tags': POPULAR_TAGS,
            'top_users': TOP_USERS,
            'user': USER_UNAUTHORIZED
        })
        return context

class QuestionView(TemplateView):
    template_name = "questions/question.html"
    
    def get_context_data(self, question_id, **kwargs):
        context = super().get_context_data(**kwargs)
        question = Question.objects.get_question(question_id)
        if not question:
            raise Http404("Вопрос не найден")
        
        answers = Answer.objects.get_answers(question_id)
        page_obj = paginate(answers, self.request)
        context.update({
            'question': question,
            'answers': page_obj.object_list,
            'page_obj': page_obj,
            'popular_tags': POPULAR_TAGS,
            'top_users': TOP_USERS,
            'user': USER_UNAUTHORIZED
        })
        return context
    

class SearchView(RedirectView):
    pattern_name = 'questions:tag'
    def get_redirect_url(self, *args, **kwargs):
        tag = self.request.GET.get('tag', '').strip()
        if not tag:
            return reverse('questions:index')
            
        return reverse(self.pattern_name, kwargs={'tag_name': tag})

class ListFoundQuestionsView(TemplateView):
    template_name = "questions/tag.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tag_name = self.kwargs.get('tag_name')
        found_questions = Question.objects.get_questions_with_tag(tag_name)
        if not found_questions.exists():
            raise Http404(f"Вопросы с тегом {tag_name} не найдены")
               
        page_obj = paginate(found_questions, self.request)
        context.update({
            'search_query': tag_name,
            'questions': page_obj.object_list,
            'page_obj': page_obj,
            'popular_tags': POPULAR_TAGS,
            'top_users': TOP_USERS,
            'user': USER_UNAUTHORIZED
        })
        return context