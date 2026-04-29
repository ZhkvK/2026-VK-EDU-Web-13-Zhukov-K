from questions.models import Tag
from core.models import Profile

def sidebar_data(request):
    return {
        'popular_tags': Tag.objects.get_popular(),
        'top_users': Profile.objects.get_most_active(),
    }