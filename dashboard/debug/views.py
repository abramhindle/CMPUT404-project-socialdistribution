from django.shortcuts import render


def test_404(request):
    return render(request, '404.html')


def test_500(request):
    return render(request, '500.html')
