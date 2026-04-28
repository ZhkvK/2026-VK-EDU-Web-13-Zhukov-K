from django.db import models
from django.contrib.auth.models import User
from core.managers import ProfileManager

class Profile(models.Model):

    user = models.OneToOneField(User, verbose_name="Пользователь", on_delete=models.CASCADE, related_name='profile')
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True, verbose_name="Аватар")
    bio = models.TextField(max_length=500, blank=True, verbose_name="О себе")

    objects = ProfileManager()

    class Meta:
        verbose_name = "Профиль"
        verbose_name_plural = "Профили"

    def __str__(self):
        return f"Профиль пользователя {self.user.username}"
