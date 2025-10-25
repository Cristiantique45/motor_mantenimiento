from django.shortcuts import render, redirect
from .arbol import DecisionTree
from .models import Pregunta

def diagnostico(request):
    tree = DecisionTree()

    # Si no hay raíz, mostrar mensaje útil
    if not tree.root:
        return render(request, 'diagnostico/error.html', {'mensaje': 'No hay pregunta raíz configurada.'})

    answer_id = request.GET.get('a')

    if not answer_id:
        # Empezar desde la raíz
        question = tree.root
        return render(request, 'diagnostico/pregunta.html', {'question': question})

    # Si viene answer_id, obtener siguiente nodo
    result = tree.get_next(answer_id)

    if result['type'] == 'question':
        print("RESULTADO DE get_next:", result)
        return render(request, 'diagnostico/pregunta.html', {'question': result['object']})

    if result['type'] == 'diagnosis':
        # result['object'] es un string con el diagnóstico final
        return render(request, 'diagnostico/resultado.html', {'diagnosis': result['object']})

    if result['type'] == 'error':
        return render(request, 'diagnostico/error.html', {'mensaje': result['object']})

    # tipo 'end' u otro -> mensaje genérico
    return render(request, 'diagnostico/error.html', {'mensaje': 'Flujo terminado sin diagnóstico.'})
