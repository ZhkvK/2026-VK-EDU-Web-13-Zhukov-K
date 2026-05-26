from django.urls import path

from questions.views import AddCommentView, AnswerVoteView, CorrectAnswerCheckView, ListNewQuestionsView, ListHotQuestionsView, AskFormView, LoadMoreCommentsView, QuestionView, QuestionVoteView, SearchView, ListFoundQuestionsView

app_name = 'questions'

urlpatterns = [
    path('', ListNewQuestionsView.as_view(), name='index'),
    path('hot', ListHotQuestionsView.as_view(), name='hot'),
    path('ask', AskFormView.as_view(), name='ask'),
    path('question/<int:question_id>', QuestionView.as_view(), name='question'),
    path('answer/<int:answer_id>/comments/', AddCommentView.as_view(), name='add_comment'),
    path('search/', SearchView.as_view(), name='search'),
    path('tag/<str:tag_name>/', ListFoundQuestionsView.as_view(), name='tag'),
    path('question/<int:question_id>/vote', QuestionVoteView.as_view(), name='question_vote'),
    path('answer/<int:answer_id>/vote', AnswerVoteView.as_view(), name='answer_vote'),
    path('answer/<int:answer_id>/is_correct', CorrectAnswerCheckView.as_view(), name='answer_correct_check'),
    path('answer/<int:answer_id>/comments/load', LoadMoreCommentsView.as_view(), name='load_comments')
]