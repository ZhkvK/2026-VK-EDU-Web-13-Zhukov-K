import json

from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, Http404, JsonResponse
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.views.generic import CreateView, TemplateView, RedirectView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse, reverse_lazy
from django.template.loader import render_to_string

from questions.forms import AddAnswerForm, AddCommentForm, AddQuestionForm
from questions.models import AnswerLike, Comment, Question, Answer, QuestionLike

def paginate(objects_list, request, per_page=10):
    page_number = request.GET.get('page')
    paginator = Paginator(objects_list, per_page)
    try:
        page = paginator.page(page_number)
    except PageNotAnInteger:
        page = paginator.page(1)
    except EmptyPage:
        page = paginator.page(paginator.num_pages)
    return page

# Create your views here.

class ListNewQuestionsView(TemplateView):
    template_name = "questions/index.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        questions = Question.objects.get_new()
        page_obj = paginate(questions, self.request)
        context.update({
            'questions': page_obj.object_list,
            'page_obj': page_obj,
        })
        return context
    
class ListHotQuestionsView(TemplateView):
    template_name = "questions/hot.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        questions = Question.objects.get_hot()
        page_obj = paginate(questions, self.request)
        context.update({
            'questions': page_obj.object_list,
            'page_obj': page_obj,
        })
        return context      

class AskFormView(LoginRequiredMixin, CreateView):
    template_name = "questions/ask.html"
    form_class = AddQuestionForm
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        self.request.user.profile.update_activity()
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse('questions:question', kwargs={'question_id': self.object.id})


class QuestionView(TemplateView):
    template_name = "questions/question.html"
    
    def get_context_data(self, **kwargs):
        question_id = self.kwargs.get('question_id')
        context = super().get_context_data(**kwargs)
        question = get_object_or_404(
            Question.objects.select_related('author').prefetch_related('tags'), 
            id=question_id
        )
        
        answers = Answer.objects.get_answers(question_id)
        page_obj = paginate(answers, self.request)
        context.update({
            'question': question,
            'answers': page_obj.object_list,
            'page_obj': page_obj,
            'form': AddAnswerForm()
        })
        return context
    
    def post(self, request, *args, **kwargs):
        question_id = self.kwargs.get('question_id')
        question = get_object_or_404(Question, id=question_id)
        
        form = AddAnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.question = question
            answer.author = request.user
            answer.save()
            self.request.user.profile.update_activity()
            question.update_answer_count()
            
            return redirect(f'{reverse("questions:question", kwargs={"question_id": question_id})}#answer_{answer.id}')
            
        context = self.get_context_data(**kwargs)
        context['form'] = form
        return self.render_to_response(context)
    
class AddCommentView(LoginRequiredMixin, TemplateView):
    def post(self, request, answer_id):
        answer = get_object_or_404(Answer, id=answer_id)
        
        form = AddCommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.answer = answer
            comment.author = request.user
            comment.save()
            
            return redirect('questions:question', question_id=answer.question.id)
            
        return redirect('questions:question', question_id=answer.question.id)

class SearchView(RedirectView):
    pattern_name = 'questions:tag'
    def get_redirect_url(self, *args, **kwargs):
        tag = self.request.GET.get('tag', '').strip()
        if not tag:
            return reverse('questions:index')
            
        return reverse(self.pattern_name, kwargs={'tag_name': tag})

class ListFoundQuestionsView(TemplateView):
    template_name = "questions/tag.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tag_name = self.kwargs.get('tag_name')
        found_questions = Question.objects.get_questions_with_tag(tag_name)
        if not found_questions.exists():
            raise Http404(f"Вопросы с тегом {tag_name} не найдены")
               
        page_obj = paginate(found_questions, self.request)
        context.update({
            'search_query': tag_name,
            'questions': page_obj.object_list,
            'page_obj': page_obj,
        })
        return context
    
class QuestionVoteView(LoginRequiredMixin, View):
    def post(self, request, question_id):
        try:
            data = json.loads(request.body)
            value = data.get('value')
            
            updated_rating = QuestionLike.objects.toggle_vote(request.user, question_id, value)
            return JsonResponse({'status': 'ok', 'updated_rating': updated_rating})
            
        except Exception as e:
            return JsonResponse({'status': 'error', 'error': str(e)}, status=400)
        
class AnswerVoteView(LoginRequiredMixin, View):
    def post(self, request, answer_id):
        try:
            data = json.loads(request.body)
            value = data.get('value')
            
            updated_rating = AnswerLike.objects.toggle_vote(request.user, answer_id, value)
            return JsonResponse({'status': 'ok', 'updated_rating': updated_rating})
            
        except Exception as e:
            return JsonResponse({'status': 'error', 'error': str(e)}, status=400)
        
class CorrectAnswerCheckView(LoginRequiredMixin, View):
    def post(self, request, answer_id):
        try:
            data = json.loads(request.body)
            is_correct = Answer.objects.check_correct(answer_id)
            return JsonResponse({'status': 'ok', 'is_correct': is_correct})
            
        except Exception as e:
            return JsonResponse({'status': 'error', 'error': str(e)}, status=400)
        
class LoadMoreCommentsView(View):
    def post(self, request, answer_id):
        try:
            data = json.loads(request.body)
            offset = int(data.get('offset', 3))
            limit = 3
            comments = Comment.objects.get_comments(answer_id, offset, limit)
            
            comments_html = ""
            for comment in comments:
                comments_html += render_to_string('questions/partials/comment.html', {'comment': comment}, request=request)
                
            total_comments = Comment.objects.filter(answer_id=answer_id).count()
            has_more = (offset + limit) < total_comments
            
            return JsonResponse({'status': 'ok', 'html': comments_html, 'has_more': has_more})
            
        except Exception as e:
            return JsonResponse({'status': 'error', 'error': str(e)}, status=400)
            