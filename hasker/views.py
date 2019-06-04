from django.shortcuts import render
from hasker.models import Question, Answer

def index(request):
    context = {
            'questions' : Question.objects.all(),
            'answers' : Answer.objects.all(),
            }
    return render(request, 'index.html', context)


def ask(request):
    questions = Question.objects.all()
    context = {
            'questions' : questions
            }
    return render(request, 'ask.html', context)
