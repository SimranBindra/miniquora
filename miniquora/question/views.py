from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.core.exceptions import SuspiciousOperation
from django.views.decorators.http import require_http_methods, require_GET, require_POST
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Question, Answer, Topic
from .forms import QuestionCreateForm

# Create your views here.
@login_required
@require_http_methods(['GET', 'POST'])
def create_question(request):
    if request.method == 'GET':
        f = QuestionCreateForm()
    else:
        f = QuestionCreateForm(request.POST)
        if f.is_valid():
            q = f.save(commit = False)
            q.by = request.user
            q.save()
            f.save_m2m()
            return redirect('myquestions')
    return render(request, 'questions/create.html', { 'form' : f})

@login_required
@require_GET
def myquestions(request, page_num = 1):
    questions = Question.objects.filter(by = request.user).order_by('-created_at')
    p = Paginator(questions, 1)
    current_page = p.page(page_num)
    return render(request, 'questions/myquestions.html', { 'questions' : current_page.object_list, 'page':current_page})

@login_required
@require_GET
def search(request):
    query_term = request.GET.get('q')
    data = {'questions': []}
    if not query_term:
        return JsonResponse(data)
    questions = Question.objects.filter(
        Q(title__icontains = query_term)|Q(desc__icontains = query_term)
    )
    data['questions'] = [{'id' : q.id, 'title' : q.title} for q in questions]
    return JsonResponse(data)

@login_required
@require_POST
def addanswer(request, q_id = None):
    ques = get_object_or_404(Question, id = q_id);
    answer_text = request.POST.get('answer').strip()
    if answer_text:
        answer = Answer.objects.create(
            question = ques, 
            by = request.user,
            text = answer_text
        );
    return JsonResponse({'success': 1, 'answer' : { 'id' : answer.id, 'text' : answer.text } });
