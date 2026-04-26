from django.urls import path

from questions import views

app_name = 'questions'

urlpatterns = [
    path('', views.index, name='index'),
    path('hot', views.hot, name='hot'),
    path('ask', views.ask, name='ask'),
    path('question/<int:question_id>', views.question, name='question'),
    path('search/', views.search, name='search'),
    path('tag/<str:tag>/', views.tag, name='tag'),
]