from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.core.validators import BaseValidator, FileExtensionValidator, EmailValidator

from django.contrib.auth.models import User

from core.models import Profile

class LoginForm(AuthenticationForm):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
    
class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True, validators=[EmailValidator(message="Введите корректный email-адрес")],)
    
    class Meta:
        model = User
        fields = ('username', 'email')
        
    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Пользователь с таким email уже существует")
        return email
    
    def save(self, commit=True):
        user = super().save(commit=commit)
        if commit:
            Profile.objects.create(user=user)
        return user
    
class ProfileUpdateForm(forms.ModelForm):
    username = forms.CharField(label="Имя пользователя", required=True)
    email = forms.EmailField(label="Email", required=True)
    
    class Meta:
        model = Profile
        fields = ['avatar', 'bio']
        
    class ImageSizeValidator(BaseValidator):
        message = "Размер файла не должен превышать %(limit_value)s Мб."
        code = None
        def compare(self, file, max_size_mb):
            return file and file.size > 1024 * 1024 * max_size_mb
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance:
            self.fields['username'].initial = self.instance.user.username
            self.fields['email'].initial = self.instance.user.email
            self.fields['avatar'].validators += [
                # FileExtensionValidator(allowed_extensions=['png', 'jpeg', 'jpg']),
                self.ImageSizeValidator(2)
            ]
            
    def save(self, commit=True):
        profile = super().save(commit=False)
        user = profile.user
        user.username = self.cleaned_data['username']
        user.email = self.cleaned_data['email']
    
        if commit:
            user.save()
            profile.save()
            
        return profile