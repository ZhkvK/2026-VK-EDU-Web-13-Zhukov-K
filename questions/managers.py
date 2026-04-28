from django.db import models

class QuestionManager(models.Manager):
    def get_new(self):
        return self.order_by('-created_at')

    def get_hot(self):
        return self.order_by('-rating')

    def get_question(self, question_id):
        question = self.filter(id=question_id).first()
        return question
    
    def get_questions_with_tag(self, tag_name):
        return self.filter(tags__name=tag_name, is_active=True).order_by('-created_at')
    
class AnswerManager(models.Manager):
    def get_answers(self, question_id):
        return self.filter(question_id=question_id).order_by('created_at')
    