from django.db import models
from django.db.models import Count
from django.db import transaction

class QuestionManager(models.Manager):
    def get_new(self):
        return self.select_related('author').prefetch_related('tags').order_by('-created_at')

    def get_hot(self):
        return self.select_related('author').prefetch_related('tags').order_by('-rating', 'created_at')

    def get_question(self, question_id):
        return self.select_related('author').prefetch_related('tags').filter(id=question_id).first()
        
    def get_questions_with_tag(self, tag_name):
        return self.select_related('author').prefetch_related('tags').filter(tags__name=tag_name, is_active=True).order_by('-created_at')
        
class AnswerManager(models.Manager):
    def get_answers(self, question_id):
        return self.filter(question_id=question_id).select_related('author').prefetch_related(
            'comments', 
            'comments__author'
        ).order_by('-is_correct', '-rating', '-created_at')
        
    def check_correct(self, answer_id):
        with transaction.atomic():
            answer = self.get(id=answer_id)
            new_status = not answer.is_correct
            if new_status is True:
                self.filter(question=answer.question, is_correct=True).update(is_correct=False)
            
            answer.is_correct = new_status
            answer.save(update_fields=['is_correct'])
            
            return answer.is_correct
        
class TagManager(models.Manager):
    def get_popular(self):
        return self.annotate(q_count=Count('questions')).order_by('-q_count')[:10]
    
class QuestionVoteManager(models.Manager):
    def toggle_vote(self, user, question_id, value):
        try:
            value = int(value)
        except (ValueError, TypeError):
            raise ValueError("Значение должно быть числом")
        
        if value not in [1, -1]:
            raise ValueError("Неверное значение лайка/дизлайка (должно быть 1 или -1)")
        
        from .models import Question 
        with transaction.atomic():
            question = Question.objects.get(id=question_id)
            vote, created = self.get_or_create(
                user=user, 
                question=question,
                defaults={'value': value}
            )
            if not created:
                if vote.value == value:
                    vote.delete()
                    question.rating -= value
                else:
                    vote.value = value
                    vote.save()
                    question.rating += (value * 2)
            else:
                question.rating += value
                
            question.save()
            return question.rating
        
class AnswerVoteManager(models.Manager):
    def toggle_vote(self, user, answer_id, value):
        
        try:
            value = int(value)
        except (ValueError, TypeError):
            raise ValueError("Значение должно быть числом")
        
        if value not in [1, -1]:
            raise ValueError("Неверное значение лайка/дизлайка (должно быть 1 или -1)")
        
        from .models import Answer 
        with transaction.atomic():
            answer = Answer.objects.get(id=answer_id)
            vote, created = self.get_or_create(
                user=user, 
                answer=answer,
                defaults={'value': value}
            )
            if not created:
                if vote.value == value:
                    vote.delete()
                    answer.rating -= value
                else:
                    vote.value = value
                    vote.save()
                    answer.rating += (value * 2)
            else:
                answer.rating += value
                
            answer.save()
            return answer.rating
        
class CommentManager(models.Manager):
    def get_comments(self, answer_id, offset, limit=3):
        return self.filter(answer_id=answer_id).select_related('author').order_by('created_at')[offset:offset+limit]