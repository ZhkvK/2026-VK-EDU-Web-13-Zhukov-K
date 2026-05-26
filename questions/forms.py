from django import forms
from django.forms import ModelForm

from questions.models import Answer, Comment, Question, Tag

class AddQuestionForm(ModelForm):
    
    new_tags = forms.CharField(
        required=False,
        label="Добавить новые теги",
        help_text="Введите названия через запятую (например: django, fastapi, new-tag)",
        widget=forms.TextInput(attrs={
            'class': 'form-control', 
            'placeholder': 'Новые теги через запятую'
        })
    )
    
    class Meta:
        model = Question
        fields = ['is_active', 'title', 'content', 'tags']
        
    def save(self, commit=True):
        question = super().save(commit=commit)
        
        if commit and self.cleaned_data.get('new_tags'):
            tag_names = [t.strip().lower() for t in self.cleaned_data['new_tags'].split(',') if t.strip()]
            for name in tag_names:
                tag, _ = Tag.objects.get_or_create(name=name)
                question.tags.add(tag)
                
        return question
    
class AddAnswerForm(ModelForm):
    class Meta:
        model = Answer
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control', 
                'rows': 4,
                'placeholder': 'Напишите ваш ответ здесь...'
            })
        }
        
class AddCommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['content']