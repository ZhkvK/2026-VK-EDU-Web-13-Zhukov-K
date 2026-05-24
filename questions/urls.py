from django.urls import path

from questions.views import AddCommentView, ListNewQuestionsView, ListHotQuestionsView, AskFormView, QuestionView, SearchView, ListFoundQuestionsView

app_name = 'questions'

urlpatterns = [
    path('', ListNewQuestionsView.as_view(), name='index'),
    path('hot', ListHotQuestionsView.as_view(), name='hot'),
    path('ask', AskFormView.as_view(), name='ask'),
    path('question/<int:question_id>', QuestionView.as_view(), name='question'),
    path('answer/<int:answer_id>/comment/', AddCommentView.as_view(), name='add_comment'),
    path('search/', SearchView.as_view(), name='search'),
    path('tag/<str:tag_name>/', ListFoundQuestionsView.as_view(), name='tag'),
]