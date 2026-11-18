


class VistaConsola:
    def bienvenida(self):
        print("\n" + "=" * 52)
        print("    ÁRBOL ROJO-NEGRO - PYTHON - ARQUITECTURA MVC")
        print("=" * 52)
        print("Sin librerías externas ni estándar. N=negro / R=rojo")

    def menu(self):
        print("\n" + "-" * 52)
        print("1. Insertar número")
        print("2. Buscar número")
        print("3. Eliminar número")
        print("4. Mostrar árbol")
        print("5. Recorrido inorden")
        print("6. Verificar las cinco propiedades")
        print("7. Cargar un ejemplo (rotaciones / recoloreo)")
        print("8. Mostrar pasos de la última operación")
        print("9. Vaciar árbol")
        print("0. Salir")
        print("-" * 52)
        return input("Selecciona una opción: ").strip()

    def solicitar_entero(self, mensaje):
        texto = input(mensaje).strip()
        try:
            return int(texto)
        except ValueError:
            self.mensaje("Error: introduce un número entero válido.")
            return None

    def mensaje(self, texto):
        print("\n" + texto)

    def mostrar_arbol(self, dibujo):
        print("\nÁRBOL ACTUAL (I=izquierda; D=derecha):")
        print(dibujo)

    def mostrar_inorden(self, valores):
        print("\nRecorrido inorden:", valores)

    def mostrar_pasos(self, pasos):
        print("\nPASOS DE LA ÚLTIMA OPERACIÓN:")
        if not pasos:
            print("No hay pasos registrados todavía.")
        for numero, paso in enumerate(pasos, 1):
            print(f"{numero}. {paso}")

    def elegir_ejemplo(self):
        print("\nEJEMPLOS PARA LA EXPOSICIÓN")
        print("1. Rotación izquierda:        10, 20, 30")
        print("2. Rotación derecha:          30, 20, 10")
        print("3. Doble izquierda-derecha:  30, 10, 20")
        print("4. Doble derecha-izquierda:  10, 30, 20")
        print("5. Recoloreo:                10, 5, 15, 1")
        return input("Selecciona el ejemplo (1-5): ").strip()
