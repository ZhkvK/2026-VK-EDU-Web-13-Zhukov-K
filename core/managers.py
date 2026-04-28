from django.db import models
from django.shortcuts import get_object_or_404

class ProfileManager(models.Manager):
    
    def get_user(self, user_id):
        return get_object_or_404(self, user__id=user_id)