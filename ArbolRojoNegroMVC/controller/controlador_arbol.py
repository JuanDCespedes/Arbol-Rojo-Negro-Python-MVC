

from model.arbol_rojo_negro import ArbolRojoNegro


class ControladorArbol:
    EJEMPLOS = {
        "1": ("Rotación izquierda", [10, 20, 30]),
        "2": ("Rotación derecha", [30, 20, 10]),
        "3": ("Doble izquierda-derecha", [30, 10, 20]),
        "4": ("Doble derecha-izquierda", [10, 30, 20]),
        "5": ("Recoloreo", [10, 5, 15, 1]),
    }

    def __init__(self, modelo, vista):
        self.modelo = modelo
        self.vista = vista

    def ejecutar(self):
        self.vista.bienvenida()
        while True:
            try:
                opcion = self.vista.menu()
            except (EOFError, KeyboardInterrupt):
                self.vista.mensaje("Programa finalizado.")
                break

            if opcion == "1":
                valor = self.vista.solicitar_entero("Valor a insertar: ")
                if valor is not None:
                    agregado = self.modelo.insertar(valor)
                    self.vista.mensaje("Insertado." if agregado else "Valor duplicado.")
                    self._mostrar_estado()

            elif opcion == "2":
                valor = self.vista.solicitar_entero("Valor a buscar: ")
                if valor is not None:
                    resultado = self.modelo.buscar(valor)
                    self.vista.mensaje("Valor encontrado." if resultado else "Valor no encontrado.")

            elif opcion == "3":
                valor = self.vista.solicitar_entero("Valor a eliminar: ")
                if valor is not None:
                    eliminado = self.modelo.eliminar(valor)
                    self.vista.mensaje("Eliminado." if eliminado else "Valor no encontrado.")
                    self._mostrar_estado()

            elif opcion == "4":
                self.vista.mostrar_arbol(self.modelo.dibujar())

            elif opcion == "5":
                self.vista.mostrar_inorden(self.modelo.inorden())

            elif opcion == "6":
                correcto, detalle = self.modelo.verificar_propiedades()
                self.vista.mensaje(("VÁLIDO: " if correcto else "INVÁLIDO: ") + detalle)

            elif opcion == "7":
                self._cargar_ejemplo()

            elif opcion == "8":
                self.vista.mostrar_pasos(self.modelo.pasos)

            elif opcion == "9":
                self.modelo = ArbolRojoNegro()
                self.vista.mensaje("Árbol reiniciado.")

            elif opcion == "0":
                self.vista.mensaje("Gracias. ¡Hasta luego!")
                break

            else:
                self.vista.mensaje("Opción no válida. Selecciona una opción del menú.")

    def _mostrar_estado(self):
        self.vista.mostrar_arbol(self.modelo.dibujar())
        valido, detalle = self.modelo.verificar_propiedades()
        self.vista.mensaje(("VÁLIDO. " if valido else "INVÁLIDO. ") + detalle)
        self.vista.mostrar_pasos(self.modelo.pasos)

    def _cargar_ejemplo(self):
        eleccion = self.vista.elegir_ejemplo()
        if eleccion not in self.EJEMPLOS:
            self.vista.mensaje("Ejemplo no válido.")
            return
        nombre, valores = self.EJEMPLOS[eleccion]
        self.modelo = ArbolRojoNegro()
        self.vista.mensaje(f"Ejemplo: {nombre}. Inserciones: {valores}")
        for valor in valores:
            self.modelo.insertar(valor)
            self.vista.mensaje(f"Después de insertar {valor}:")
            self.vista.mostrar_arbol(self.modelo.dibujar())
            self.vista.mostrar_pasos(self.modelo.pasos)
        valido, detalle = self.modelo.verificar_propiedades()
        self.vista.mensaje(("VÁLIDO. " if valido else "INVÁLIDO. ") + detalle)
