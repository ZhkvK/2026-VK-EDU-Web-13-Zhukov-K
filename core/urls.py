from django.urls import path
from core.views import LoginView, SignupView, ProfiveView 

app_name = 'core'

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('signup/', SignupView.as_view(), name='signup'),
    path('profile/<int:user_id>/', ProfiveView.as_view(), name='profile'),
]