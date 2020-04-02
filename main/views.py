from django.shortcuts import render

from .models import Message

def index(request):
    message = Message.objects.all()[0]
    context = {
        'message': message.message
    }
    return render(request, 'main/index.html', context)
