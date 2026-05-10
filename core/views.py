from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.contrib.auth import login
from core.forms import LoginForm, RegistrationForm
from core.models import Profile

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

class MyLoginView(LoginView):
    template_name = "core/login.html"
    form_class = LoginForm
    redirect_authenticated_user = False
    
class SignupView(CreateView):
    template_name = "core/signup.html"
    form_class = RegistrationForm
    success_url = reverse_lazy('questions:index')
    
    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        return response

class ProfiveView(LoginRequiredMixin, TemplateView):
    template_name = "core/profile.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_id = self.kwargs.get('user_id') 
        profile = Profile.objects.get_user(user_id)
        context.update({
            'profile': profile,
            'popular_tags': POPULAR_TAGS,
            'top_users': TOP_USERS,
        })
        return context