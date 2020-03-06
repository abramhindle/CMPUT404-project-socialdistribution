from django.shortcuts import render

def index(request):
    template = 'login/login.html'
    
    context = {
        
    }

    return render(request, template, context)

def index_register(request):
    template ='login/register.html'

    return render(request,template,{})