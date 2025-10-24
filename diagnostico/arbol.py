# from .models import Pregunta, Respuesta

# class DecisionTree:
#     def __init__(self):
#         # obtenemos la pregunta raíz
#         self.root = Pregunta.objects.filter(is_root=True).first()

#     def get_next(self, current_question, answer):
#         """
#         Recibe la pregunta actual y la respuesta del usuario (True/False o 'si'/'no'),
#         y devuelve la siguiente pregunta o el diagnóstico final.
#         """
#         if answer in [True, 'si', 'sí', 'SI', 'SÍ']:
#             next_question = current_question.next_if_yes
#         else:
#             next_question = current_question.next_if_no

#         if next_question:
#             return {'type': 'question', 'object': next_question}
#         elif current_question.diagnosis:
#             return {'type': 'diagnosis', 'object': current_question.diagnosis}
#         else:
#             return {'type': 'end', 'object': None}


# decision_tree.py
# from .models import Pregunta, Respuesta

# class DecisionTree:
#     def __init__(self):
#         self.root = Pregunta.objects.filter(is_root=True).first()

#     def get_next(self, answer_id):
#         answer = Respuesta.objects.get(id=answer_id)
#         if answer.siguiente_pregunta_id:
#             return {'type': 'question', 'object': answer.siguiente_pregunta_id}
#         elif answer.diagnostico_final:
#             return {'type': 'diagnosis', 'object': answer.diagnostico_final}
#         else:
#             return None

from .models import Pregunta, Respuesta
from django.core.exceptions import ObjectDoesNotExist

class DecisionTree:
    def __init__(self):
        # Si el modelo tiene is_root, úsalo; si no, busca la pregunta sin padre
        if any(field.name == 'is_root' for field in Pregunta._meta.fields):
            self.root = Pregunta.objects.filter(is_root=True).first()
        else:
            self.root = Pregunta.objects.filter(pregunta_padre__isnull=True).first()

    def get_next(self, answer_id):
        try:
            answer = Respuesta.objects.get(id=answer_id)
        except ObjectDoesNotExist:
            return {'type': 'error', 'object': 'Respuesta no encontrada.'}

        # Si hay siguiente pregunta (objeto Pregunta), devolverla
        if answer.siguiente_pregunta:
            return {'type': 'question', 'object': answer.siguiente_pregunta}

        # Si la respuesta contiene un diagnóstico final (texto), devolverlo como diagnosis
        if answer.diagnostico_final:
            return {'type': 'diagnosis', 'object': answer.diagnostico_final}

        # Sin siguiente ni diagnóstico
        return {'type': 'end', 'object': None}

