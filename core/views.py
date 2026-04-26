from django.shortcuts import render

POPULAR_TAGS = ['python', 'javascript', 'html', 'css', 'bootstrap', 'django', 'react', 'sql']

TOP_USERS = [
    {'username': 'User1', 'reputation': 1234},
    {'username': 'User2', 'reputation': 987},
    {'username': 'User3', 'reputation': 756},
]

USER_AUTHORIZED = {
    'username': "Dr.Pepper",
    'email': "dr.pepper@example.com",
    'avatar_image': "questions/img/Logo.png",
    'about': "Привет! Я увлекаюсь программированием и технологиями.",
    'is_Authorized': True
}

USER_UNAUTHORIZED = {
    'username': "Dr.Pepper",
    'email': "dr.pepper@example.com",
    'avatar_image': "questions/img/Logo.png",
    'about': "Привет! Я увлекаюсь программированием и технологиями.",
    'is_Authorized': False
}

# Create your views here.
def login(request):
    return render(request, 'core/login.html', context={'user':USER_UNAUTHORIZED})

def signup(request):
    return render(request, 'core/signup.html', context={'user':USER_UNAUTHORIZED})

def profile(request):
    return render(request, 'core/profile.html', context={
        'user':USER_AUTHORIZED,
        'popular_tags': POPULAR_TAGS,
        'top_users': TOP_USERS
        })