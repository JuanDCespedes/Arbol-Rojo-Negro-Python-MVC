from model.arbol_rojo_negro import ArbolRojoNegro
from model.nodo import ROJO, NEGRO


def validar(arbol, esperados):
    valido, mensaje = arbol.verificar_propiedades()
    assert valido, mensaje
    assert arbol.inorden() == sorted(esperados), (
        f"Inorden incorrecto: {arbol.inorden()} != {sorted(esperados)}"
    )
    assert arbol.cantidad == len(esperados), "Contador de nodos incorrecto"
    for valor in esperados:
        assert arbol.buscar(valor), f"No se encuentra {valor}"


def probar_cinco_casos():
    casos = (
        ("izquierda", [10, 20, 30]),
        ("derecha", [30, 20, 10]),
        ("izquierda-derecha", [30, 10, 20]),
        ("derecha-izquierda", [10, 30, 20]),
        ("recoloreo", [10, 5, 15, 1]),
    )
    for nombre, elementos in casos:
        arbol = ArbolRojoNegro()
        for i, numero in enumerate(elementos):
            assert arbol.insertar(numero)
            validar(arbol, elementos[:i + 1])
        if nombre != "recoloreo":
            assert arbol.raiz.valor == 20
            assert arbol.raiz.color == NEGRO
            assert arbol.raiz.izquierdo.color == ROJO
            assert arbol.raiz.derecho.color == ROJO
        else:
            assert arbol.raiz.valor == 10
            assert arbol.raiz.izquierdo.color == NEGRO
            assert arbol.raiz.derecho.color == NEGRO
        print("OK:", nombre)


def probar_casos_de_eliminacion():
    casos = (
        ([10], [10]),
        ([10, 5], [10, 5]),
        ([10, 5, 15], [10, 5, 15]),
        ([10, 5, 15, 1], [5, 15, 10, 1]),
        ([20, 10, 30, 5, 15, 25, 40, 1, 6], [10, 20, 25, 30, 5, 15, 1, 6, 40]),
        (list(range(1, 101)), list(range(100, 0, -1))),
    )
    for inserciones, eliminaciones in casos:
        arbol = ArbolRojoNegro()
        valores = set()
        for v in inserciones:
            assert arbol.insertar(v)
            valores.add(v)
            validar(arbol, valores)
        for v in eliminaciones:
            assert arbol.eliminar(v)
            valores.remove(v)
            validar(arbol, valores)
        assert not arbol.eliminar(1234567)
        assert arbol.raiz is arbol.NIL
        validar(arbol, set())
    print("OK: eliminación de hojas, raíz, nodos con 1 y 2 hijos y vaciado")


def probar_muchos_datos():
    comprobaciones = 0
    for semilla_inicial in range(1, 13):
        valores = list(range(-125, 125))
        semilla = semilla_inicial * 42 + 17
        for i in range(len(valores) - 1, 0, -1):
            semilla = (1664525 * semilla + 1013904223) % (2 ** 32)
            j = semilla % (i + 1)
            valores[i], valores[j] = valores[j], valores[i]

        arbol = ArbolRojoNegro()
        presentes = set()
        for numero in valores:
            assert arbol.insertar(numero)
            presentes.add(numero)
            validar(arbol, presentes)
            comprobaciones += 1
        assert not arbol.insertar(valores[0]), "No debe admitir duplicados"

        for numero in reversed(valores):
            assert arbol.eliminar(numero)
            presentes.remove(numero)
            validar(arbol, presentes)
            comprobaciones += 1
        assert not presentes
    print(f"OK: {comprobaciones} operaciones con mezclas deterministas")


def ejecutar_pruebas():
    probar_cinco_casos()
    probar_casos_de_eliminacion()
    probar_muchos_datos()
    print("\nTODAS LAS PRUEBAS PASARON")


if __name__ == "__main__":
    ejecutar_pruebas()
