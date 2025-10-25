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
            self.insertar_ordenar(self.raiz,valor)
            
    def insertar_ordenar(self, nodo_actual, valor):
        if valor < nodo_actual.valor:
            if nodo_actual.izq is None:
                nodo_actual.izq = Nodo(valor)
            else:
                self.insertar_ordenar(nodo_actual.izq, valor)
        else:
            if nodo_actual.der is None:
                nodo_actual.der = Nodo(valor)
            else:
                self.insertar_ordenar(nodo_actual.der, valor)
            
            
    def inorden(self, nodo):
        if nodo:
            self.inorden(nodo.izq)
            print(nodo.valor)
            self.inorden(nodo.der)
            
    def preorden(self, nodo):
        if nodo:
            print(nodo.valor)
            self.preorden(nodo.izq)
            self.preorden(nodo.der)
            
    def postorden(self, nodo):
        if nodo:
            self.postorden(nodo.izq)
            self.postorden(nodo.der)
            print(nodo.valor)
        
arbol = Arbol()
arbol.insertar(45)
arbol.insertar(23)
arbol.insertar(65)
arbol.insertar(2)
arbol.insertar(38)
arbol.insertar(52)
arbol.insertar(96)
arbol.insertar(7)
arbol.insertar(48)

print("------------------inorden------------------------")
arbol.inorden(arbol.raiz)
print("-------------------preorden----------------------")
arbol.preorden(arbol.raiz)
print("-------------------postorden---------------------")
arbol.postorden(arbol.raiz)