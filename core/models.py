from django.db import models
from django.contrib.auth.models import User
from core.managers import ProfileManager

class Profile(models.Model):

    user = models.OneToOneField(User, verbose_name="Пользователь", on_delete=models.CASCADE, related_name='profile')
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True, verbose_name="Аватар", default='profile_image_dummy.png')
    bio = models.TextField(max_length=500, blank=True, verbose_name="О себе")
    activity_count = models.IntegerField(verbose_name="Активность", default=0)

    objects = ProfileManager()

    class Meta:
        verbose_name = "Профиль"
        verbose_name_plural = "Профили"

    def __str__(self):
        return f"Профиль пользователя {self.user.username}"
    
    def update_activity(self):
        self.activity_count = self.user.question_set.count() + self.user.answer_set.count()
        self.save(update_fields=['activity_count'])
