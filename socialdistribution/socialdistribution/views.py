from django.shortcuts import render

def index(request):
    template = 'login/login.html'
    
    context = {
        
    }

    return render(request, template, context)