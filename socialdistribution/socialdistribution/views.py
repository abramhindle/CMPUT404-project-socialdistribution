from django.shortcuts import render

def index(request):
    template = 'login/login.html'
    
    context = {
        
    }

    return render(request, template, context)

def index_register(request):
    template ='login/register.html'

    return render(request,template,{})

# the http error page
def error_404(request):
    template ='404.html'

    return render(request,template,{})

def error_403(request):
    template ='403.html'

    return render(request,template,{})

def error_500(request):
    template ='500.html'

    return render(request,template,{})