from django.shortcuts import render

# Create your views here.
def index(request):
    context = {'mensaje': '¡Bienvenido a mi página inicial con Django!'}
    return render(request, 'home/index.html', context)
