from django.db import models
from django.contrib.auth.models import User

class QuestionManager(models.Manager):
    def get_new(self):
        return self.order_by('-created_at')

    def get_best(self):
        return self.order_by('-rating')

# Create your models here.

class Tag(models.Model):

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

class Answer(models.Model):

    question = models.ForeignKey(Question, verbose_name="Вопрос", on_delete=models.CASCADE, related_name="answers")
    author = models.ForeignKey(User, verbose_name="Автор", on_delete=models.CASCADE)
    content = models.TextField(verbose_name="Текст ответа")
    created_at = models.DateTimeField(verbose_name="Создан", auto_now_add=True)
    rating = models.IntegerField(verbose_name="Рейтинг", default=0)
    is_active = models.BooleanField(verbose_name="Активно?", default=True)

    class Meta:
        verbose_name = ("Ответ")
        verbose_name_plural = ("Ответы")
    
    def __str__(self):
        return f"Ответ на вопрос \"{self.question}\""


class Comment(models.Model):

    answer = models.ForeignKey(Answer, verbose_name="Ответ", on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(User, verbose_name="Автор", on_delete=models.CASCADE)
    content = models.TextField(verbose_name="Текст комментария")
    created_at = models.DateField(verbose_name="Создан", auto_now=False, auto_now_add=False)
    is_active = models.BooleanField(verbose_name="Активно?", default=True)

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

    class Meta:
        unique_together = ('user', 'answer')
        verbose_name = "Лайк к ответу"
        verbose_name_plural = "Лайки к ответам"
