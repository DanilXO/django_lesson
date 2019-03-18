from django.contrib.auth import authenticate, login
from django.db.models import F
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render, HttpResponse, get_object_or_404, redirect
from django.template import RequestContext, loader
from django.urls import reverse
from django.views import generic

from polls.forms import LogInForm
from polls.models import Question, Choice

def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    login_form = LogInForm()
    if login_form.is_valid():
        HttpResponseRedirect(reverse('polls:login'))
    context = {'latest_question_list': latest_question_list, 'login_form': login_form}
    return render(request, 'polls/index.html', context)


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'

def login_view(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    print(user)
    if user is not None:
        if user.is_active:
            login(request, user)
            redirect('polls:index')
        else:
            return render(request, 'polls/index.html', {
                    'error_message': "disabled account!",
                })
    else:
        return render(request, 'polls/index.html', {
                'error_message': "invalid login!",
            })
    return HttpResponseRedirect(reverse('polls:index'))

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        print(request.POST)
        print(request.GET)
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes = F('votes') + 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
        # return redirect(reverse('polls:results', args=(question.id,)))