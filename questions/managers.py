from django.db import models
from django.db.models import Count

class QuestionManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()\
            .select_related('author')\
            .prefetch_related('tags')\
    
    def get_new(self):
        return self.get_queryset().order_by('-created_at')

    def get_hot(self):
        return self.get_queryset().order_by('-rating', 'created_at')

    def get_question(self, question_id):
        question = self.get_queryset().filter(id=question_id).first()
        return question
    
    def get_questions_with_tag(self, tag_name):
        return self.get_queryset().filter(tags__name=tag_name, is_active=True).order_by('-created_at')
    
class AnswerManager(models.Manager):
    def get_answers(self, question_id):
        return self.filter(question_id=question_id).select_related('author').prefetch_related(
            'comments', 
            'comments__author'
        ).order_by('-rating', '-created_at')

class TagManager(models.Manager):
    def get_popular(self):
        return self.annotate(q_count=Count('questions')).order_by('-q_count')[:10]     
    