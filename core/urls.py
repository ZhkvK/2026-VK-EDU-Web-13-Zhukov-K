from django.urls import path
from core.views import MyLoginView, SignupView, ProfiveView 
from django.contrib.auth.views import LogoutView 

app_name = 'core'

urlpatterns = [
    path('login/', MyLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='core:login'), name='logout'),
    path('signup/', SignupView.as_view(), name='signup'),
    path('profile/', ProfiveView.as_view(), name='profile'),
    
]