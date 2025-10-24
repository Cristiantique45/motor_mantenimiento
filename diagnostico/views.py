# from django.shortcuts import render, get_object_or_404
# from .models import Pregunta, Respuesta

# # def diagnostico(request):
# #     return render(request, 'diagnostico/diagnostico.html')    
# def diagnostico(request):
#     question_id = request.GET.get('q')
#     answer_id = request.GET.get('a')

#     if not question_id:
#         # Si no hay pregunta, comenzamos desde la raíz
#         question = Pregunta.objects.filter(is_root=True).first()
#     else:
#         # Si hay respuesta, buscamos la siguiente pregunta
#         answer = get_object_or_404(Respuesta, id=answer_id)
#         if answer.next_question:
#             question = answer.next_question
#         elif answer.diagnosis:
#             # Si ya tiene diagnóstico final, lo mostramos
#             return render(request, 'diagnostico/resultado.html', {'diagnosis': answer.diagnosis})
#         else:
#             question = None

#     return render(request, 'diagnostico/pregunta.html', {'question': question})

# from .arbol import DecisionTree

# def diagnostico(request):
#     tree = DecisionTree()
#     question_id = request.GET.get('q')
#     answer_id = request.GET.get('a')

#     if not answer_id:
#         question = tree.root
#         return render(request, 'diagnostico/pregunta.html', {'question': question})

#     result = tree.get_next(answer_id)
#     if result['type'] == 'question':
#         return render(request, 'diagnostico/pregunta.html', {'question': result['object']})
#     else:
#         return render(request, 'diagnostico/resultado.html', {'diagnosis': result['object']})

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
        return render(request, 'diagnostico/pregunta.html', {'question': result['object']})

    if result['type'] == 'diagnosis':
        print("RESULTADO DE get_next:", result)
        # result['object'] es un string con el diagnóstico final
        return render(request, 'diagnostico/resultado.html', {'diagnosis': result['object']})

    if result['type'] == 'error':
        return render(request, 'diagnostico/error.html', {'mensaje': result['object']})

    # tipo 'end' u otro -> mensaje genérico
    return render(request, 'diagnostico/error.html', {'mensaje': 'Flujo terminado sin diagnóstico.'})
