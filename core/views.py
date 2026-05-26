from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.contrib.auth import login
from django.contrib import messages
from core.forms import LoginForm, ProfileUpdateForm, RegistrationForm
from core.models import Profile

class MyLoginView(LoginView):
    template_name = "core/login.html"
    form_class = LoginForm
    redirect_authenticated_user = False
    def form_valid(self, form):
        profile, created = Profile.objects.get_or_create(user=form.get_user())
        profile.update_activity()
        return super().form_valid(form)
    
    
class SignupView(CreateView):
    template_name = "core/signup.html"
    form_class = RegistrationForm
    success_url = reverse_lazy('questions:index')
    
    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        return response

class ProfiveView(LoginRequiredMixin, UpdateView):
    template_name = "core/profile.html"
    model = Profile
    success_url = reverse_lazy('core:profile')
    form_class = ProfileUpdateForm
    
    def get_object(self):
        profile, created = Profile.objects.get_or_create(user=self.request.user)
        return profile
    
    def form_valid(self, form):
        messages.success(self.request, "Ваш профиль успешно обновлен!")
        return super().form_valid(form)