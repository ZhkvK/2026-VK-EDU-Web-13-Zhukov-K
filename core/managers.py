from django.db import models

class ProfileManager(models.Manager):
    def get_user(self, user_id):
        return self.select_related('user').filter(user__id=user_id).first()
    
    def get_most_active(self):
        return self.select_related('user').order_by("-activity_count")[:5]