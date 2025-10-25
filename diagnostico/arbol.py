from .models import Pregunta, Respuesta
from django.core.exceptions import ObjectDoesNotExist


# Clase Nodo y Arbol adaptadas desde Nodo.py
class Nodo:
    def __init__(self, valor):
        self.valor = valor
        self.izq = None
        self.der = None


class Arbol:
    def __init__(self):
        self.raiz = None

    def insertar(self, valor):
        if self.raiz is None:
            self.raiz = Nodo(valor)
        else:
            self._insertar_ordenar(self.raiz, valor)

    def _insertar_ordenar(self, nodo_actual, valor):
        # Inserción por comparación; adecuado cuando los valores son comparables
        if valor < nodo_actual.valor:
            if nodo_actual.izq is None:
                nodo_actual.izq = Nodo(valor)
            else:
                self._insertar_ordenar(nodo_actual.izq, valor)
        else:
            if nodo_actual.der is None:
                nodo_actual.der = Nodo(valor)
            else:
                self._insertar_ordenar(nodo_actual.der, valor)

    def inorden(self, nodo, visit=lambda x: print(x)):
        if nodo:
            self.inorden(nodo.izq, visit)
            visit(nodo.valor)
            self.inorden(nodo.der, visit)

    def preorden(self, nodo, visit=lambda x: print(x)):
        if nodo:
            visit(nodo.valor)
            self.preorden(nodo.izq, visit)
            self.preorden(nodo.der, visit)

    def postorden(self, nodo, visit=lambda x: print(x)):
        if nodo:
            self.postorden(nodo.izq, visit)
            self.postorden(nodo.der, visit)
            visit(nodo.valor)


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

