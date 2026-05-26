from application.celery import app
from django.conf import settings
from django.core.cache import cache
from cent import Client, PublishRequest
from django.core.mail import send_mail

from core.models import Profile
from questions.models import Tag, Question, Answer

@app.task(bind=True, ignore_result=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
    
@app.task()
def publish_to_centrifuge_task(channel, data):
        api_url = f"{settings.CENTRIFUGE_URL}api"
        api_key = f"{settings.CENTRIFUGE_API_KEY}"

        client = Client(api_url, api_key)
        request = PublishRequest(channel=channel, data=data)
        result = client.publish(request)
        
@app.task()
def refresh_cache_task():
    top_users_key = "top_users"
    top_tags_key = "top_tags"
    
    top_users = Tag.objects.get_popular()
    cache.set(top_users_key, top_users, timeout=5*60)
    top_tags = Profile.objects.get_most_active()
    cache.set(top_tags_key, top_tags, timeout=5*60)

@app.task()
def send_email_task(question_id):
    question = Question.objects.get_question(question_id)
    if not question:
        return 

    send_mail(
        "Notification",
        f"New answer to your question \"{question.content}\" was published!.",
        "from@example.com",
        [question.author.email],
        fail_silently=False,
    )
    
@app.task()
def update_user_activity_task(user_id):
    profile, created = Profile.objects.get_or_create(user_id=user_id)
    profile.update_activity()
    
@app.task()
def update_answer_count_task(question_id):
    question = Question.objects.get(id=question_id)
    question.update_answer_count()