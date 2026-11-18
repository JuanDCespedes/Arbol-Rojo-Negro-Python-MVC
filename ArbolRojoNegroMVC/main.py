"""Ejecuta este archivo en PyCharm (clic derecho > Run 'main')."""

from model.arbol_rojo_negro import ArbolRojoNegro
from view.vista_consola import VistaConsola
from controller.controlador_arbol import ControladorArbol


def main():
    modelo = ArbolRojoNegro()
    vista = VistaConsola()
    controlador = ControladorArbol(modelo, vista)
    controlador.ejecutar()


if __name__ == "__main__":
    main()
