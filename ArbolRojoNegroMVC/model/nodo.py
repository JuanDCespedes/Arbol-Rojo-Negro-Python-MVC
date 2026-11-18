

ROJO = "ROJO"
NEGRO = "NEGRO"


class Nodo:


    def __init__(self, valor, color=ROJO):
        self.valor = valor
        self.color = color
        self.izquierdo = None
        self.derecho = None
        self.padre = None

    def __repr__(self):
        return f"Nodo({self.valor}, {self.color})"
