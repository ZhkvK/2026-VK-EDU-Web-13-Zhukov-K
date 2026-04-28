from django.contrib import admin
from questions.models import Tag, Question, Answer, Comment, QuestionLike, AnswerLike
# Register your models here.

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ["__str__", "author", "created_at", "is_active"]
    list_filter = ["is_active"]
    search_fields = ["title", "author__username", "tags__name"]
    autocomplete_fields = ["tags"]
    raw_id_fields = ["author"]
    readonly_fields = ["rating", "answers_count"]
    list_select_related = ["author"] 

    class AnswerInline(admin.TabularInline):
        model = Answer
        raw_id_fields = ["author"]
        fields = ["content", "author", "is_active", "rating", "is_correct"]
        readonly_fields = ["rating"]
        extra = 0
    
    inlines = [AnswerInline]
    

@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ["__str__", "author", "created_at", "is_active"]
    list_filter = ["is_active"]
    search_fields = ["content", "author__username"]
    raw_id_fields = ["author", "question"]
    list_select_related = ["author", "question"]
    readonly_fields = ["rating"]

    class CommentInline(admin.TabularInline):
        model = Comment
        raw_id_fields = ["author"]
        fields = ["content", "author", "is_active"]
        # readonly_fields = ["author"]
        extra = 0
    
    inlines = [CommentInline]

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ["__str__", "is_active"]
    list_filter = ["is_active"]
    search_fields = ["name"]

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ["answer", "author", "created_at", "is_active"]
    list_filter = ["is_active"]
    search_fields = ["content", "author__username"]
    raw_id_fields = ["author", "answer"]
    list_select_related = ["author", "answer"]

@admin.register(QuestionLike)
class QuestionLikeAdmin(admin.ModelAdmin):
    list_display = ["question", "value",  "user"]
    list_filter = ["value"]
    search_fields = ["question__title","user__username"]
    raw_id_fields = ["question", "user"]
    list_select_related = ["question", "user"]


@admin.register(AnswerLike)
class AnswerLikeAdmin(admin.ModelAdmin):
    list_display = ["answer", "value", "user"]
    list_filter = ["value"]
    search_fields = ["answer__question__title", "user__username"]
    raw_id_fields = ["answer", "user"]
    list_select_related = ["answer", "user"]