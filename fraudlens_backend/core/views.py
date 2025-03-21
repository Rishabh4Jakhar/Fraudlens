from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request, 'index.html')

def signin(request):
    return render(request, 'login.html')

def result(request):
    return render(request, 'result.html')