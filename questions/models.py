from django.db import models
from django.contrib.auth.models import User
from questions.managers import AnswerVoteManager, CommentManager, QuestionManager, AnswerManager, QuestionVoteManager, TagManager
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.db.models import Sum


# Create your models here.

class Tag(models.Model):
    
    objects = TagManager()

    name = models.CharField(verbose_name="Название тега", max_length=50, unique=True)
    is_active = models.BooleanField(verbose_name="Активно?", default=True)

    class Meta:
        verbose_name = ("Тег")
        verbose_name_plural = ("Теги")

    def __str__(self):
        return self.name

class Question(models.Model):
    title = models.CharField(verbose_name="Название", max_length=255)
    content = models.TextField(verbose_name="Текст вопроса")
    author = models.ForeignKey(User, verbose_name=("Автор"), on_delete=models.CASCADE)
    created_at = models.DateTimeField(verbose_name="Создан", auto_now_add=True)
    tags = models.ManyToManyField(Tag, verbose_name="Теги", related_name="questions", blank=True)
    answers_count = models.IntegerField(verbose_name="Количество ответов", default=0)
    rating = models.IntegerField(verbose_name="Рейтинг (лайки минус дизлайки)", default=0)
    is_active = models.BooleanField(verbose_name="Активно?", default=True)

    objects = QuestionManager()

    class Meta:
        verbose_name="Вопрос"
        verbose_name_plural="Вопросы"

    def __str__(self):
        return self.title
    
    def update_answer_count(self):
        self.answers_count = Answer.objects.get_answers(self.id).count()
        self.save(update_fields=['answers_count'])
        
    def to_json(self):
        return {
            "id": self.id,
            "title": self.title,
            "author": self.author.username,
            "content": self.content,
            "tags": list(self.tags),
            "created_at": self.created_at.strftime('%d.%m.%Y %H.%m'),
            "rating": self.rating,
            "is_active": self.is_active,
            "is_correct": self.is_correct
        }

class Answer(models.Model):

    question = models.ForeignKey(Question, verbose_name="Вопрос", on_delete=models.CASCADE, related_name="answers")
    author = models.ForeignKey(User, verbose_name="Автор", on_delete=models.CASCADE)
    content = models.TextField(verbose_name="Текст ответа")
    created_at = models.DateTimeField(verbose_name="Создан", auto_now_add=True)
    rating = models.IntegerField(verbose_name="Рейтинг", default=0)
    is_active = models.BooleanField(verbose_name="Активно?", default=True)
    is_correct = models.BooleanField(verbose_name="Правильный ответ", default=False)

    objects = AnswerManager()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['question'], 
                condition=models.Q(is_correct=True),
                name='Должен быть только 1 правильный ответ для 1 вопроса'
            )
        ]
        verbose_name = ("Ответ")
        verbose_name_plural = ("Ответы")
    
    def __str__(self):
        return f"Ответ на вопрос \"{self.question}\""
    
    def to_json(self):
        return {
            "id": self.id,
            "question": self.question,
            "author": self.author,
            "content": self.content,
            "created_at": self.created_at.strftime('%d.%m.%Y %H.%m'),
            "rating": self.rating,
            "is_active": self.is_active,
            "is_correct": self.is_correct
        }


class Comment(models.Model):

    answer = models.ForeignKey(Answer, verbose_name="Ответ", on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(User, verbose_name="Автор", on_delete=models.CASCADE)
    content = models.TextField(verbose_name="Текст комментария")
    created_at = models.DateTimeField(verbose_name="Создан", auto_now_add=True)
    is_active = models.BooleanField(verbose_name="Активно?", default=True)

    objects = CommentManager()

    class Meta:
        verbose_name = ("Комментарий")
        verbose_name_plural = ("Комментарии")

    def __str__(self):
        return f"Комментарий к ответу {self.answer}"
    


class QuestionLike(models.Model):
    LIKE_CHOICES = (
        (1, 'Лайк'),
        (-1, 'Дизлайк')
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="likes", verbose_name="Вопрос")
    value = models.IntegerField(verbose_name="Значение", choices=LIKE_CHOICES)

    objects = QuestionVoteManager()

    class Meta:
        unique_together = ('user', 'question')
        verbose_name = "Лайк к вопросу"
        verbose_name_plural = "Лайки к вопросам"


class AnswerLike(models.Model):
    LIKE_CHOICES = (
        (1, 'Лайк'),
        (-1, 'Дизлайк')
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, related_name="likes", verbose_name="Ответ")
    value = models.IntegerField(verbose_name="Значение", choices=LIKE_CHOICES)

    objects = AnswerVoteManager()

    class Meta:
        unique_together = ('user', 'answer')
        verbose_name = "Лайк к ответу"
        verbose_name_plural = "Лайки к ответам"

## Методы для обновления счетчиков для fill_db
# @receiver([post_save, post_delete], sender=Question)
# @receiver([post_save, post_delete], sender=Answer)
# def update_profile_activity(sender, instance, **kwargs):
#     profile = instance.author.profile
#     q_count = Question.objects.filter(author=instance.author).count()
#     a_count = Answer.objects.filter(author=instance.author).count()
#     profile.activity_count = q_count + a_count
#     profile.save(update_fields=['activity_count'])

# @receiver([post_save, post_delete], sender=Answer)
# def update_question_answers_count(sender, instance, **kwargs):
#     question = instance.question
#     question.answers_count = question.answers.count()
#     question.save(update_fields=['answers_count'])

# @receiver([post_save, post_delete], sender=QuestionLike)
# def update_question_rating(sender, instance, **kwargs):
#     question = instance.question
#     rating = question.likes.aggregate(total=Sum('value'))['total'] or 0
#     question.rating = rating
#     question.save(update_fields=['rating'])

# @receiver([post_save, post_delete], sender=AnswerLike)
# def update_answer_rating(sender, instance, **kwargs):
#     answer = instance.answer
#     rating = answer.likes.aggregate(total=Sum('value'))['total'] or 0
#     answer.rating = rating
#     answer.save(update_fields=['rating'])