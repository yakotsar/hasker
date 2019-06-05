from django.shortcuts import render
from hasker.models import Question, Answer, Tag
from hasker.forms import AskForm
from django.views.generic import View
from django.http import HttpResponseRedirect

def index(request):
    context = {
            'questions' : Question.objects.all(),
            'answers' : Answer.objects.all(),
            }
    return render(request, 'index.html', context)


class AskView(View):

    def get(self, request):
        form = AskForm()
        context = {
            'questions' : Question.objects.all(),
            'form' : form
        }
        return render(request, 'ask.html', context)

    def post(self, request):
        form = AskForm(request.POST)
        if form.is_valid():
            new_question = Question(
                    title=form.cleaned_data['title'],
                    text=form.cleaned_data['text'],
                    author=request.user,
                    )
            new_question.save()
            return HttpResponseRedirect('/')
    
