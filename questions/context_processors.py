from django.core.cache import cache

from questions.models import Tag
from core.models import Profile

def sidebar_data(request):
    top_users_key = "top_users"
    top_tags_key = "top_tags"
    
    top_users = cache.get(top_tags_key)
    top_tags = cache.get(top_tags_key)
    
    if not top_users:
        top_users = Tag.objects.get_popular()
        cache.set(top_users_key, top_users, timeout=5*60)
    if not top_tags:
        top_tags = Profile.objects.get_most_active()
        cache.set(top_tags_key, top_tags, timeout=5*60)
    
    return {
        'popular_tags': top_users,
        'top_users': top_tags,
    }