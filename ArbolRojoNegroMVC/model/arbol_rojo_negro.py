

from model.nodo import Nodo, ROJO, NEGRO


class ArbolRojoNegro:
    def __init__(self):
        # NIL representa las hojas ausentes, que SIEMPRE son negras.
        self.NIL = Nodo(None, NEGRO)
        self.NIL.izquierdo = self.NIL
        self.NIL.derecho = self.NIL
        self.NIL.padre = self.NIL
        self.raiz = self.NIL
        self.pasos = []
        self.cantidad = 0

    def _anotar(self, descripcion):
        self.pasos.append(descripcion)

    # -------------------------------------------------------------
    # 1. BÚSQUEDA
    # -------------------------------------------------------------
    def _encontrar(self, valor):
        actual = self.raiz
        while actual is not self.NIL:
            if valor == actual.valor:
                return actual
            if valor < actual.valor:
                actual = actual.izquierdo
            else:
                actual = actual.derecho
        return self.NIL

    def buscar(self, valor):
        """Devuelve True si el valor existe; False en caso contrario."""
        return self._encontrar(valor) is not self.NIL

    # -------------------------------------------------------------
    # 2. ROTACIONES (conservan el orden de búsqueda)
    # -------------------------------------------------------------
    def _rotar_izquierda(self, x):
        y = x.derecho
        if y is self.NIL:
            raise ValueError("No se puede rotar a la izquierda sin hijo derecho")

        x.derecho = y.izquierdo
        if y.izquierdo is not self.NIL:
            y.izquierdo.padre = x

        y.padre = x.padre
        if x.padre is self.NIL:
            self.raiz = y
        elif x is x.padre.izquierdo:
            x.padre.izquierdo = y
        else:
            x.padre.derecho = y

        y.izquierdo = x
        x.padre = y
        self._anotar(f"Rotación IZQUIERDA alrededor de {x.valor}; sube {y.valor}.")

    def _rotar_derecha(self, x):
        y = x.izquierdo
        if y is self.NIL:
            raise ValueError("No se puede rotar a la derecha sin hijo izquierdo")

        x.izquierdo = y.derecho
        if y.derecho is not self.NIL:
            y.derecho.padre = x

        y.padre = x.padre
        if x.padre is self.NIL:
            self.raiz = y
        elif x is x.padre.derecho:
            x.padre.derecho = y
        else:
            x.padre.izquierdo = y

        y.derecho = x
        x.padre = y
        self._anotar(f"Rotación DERECHA alrededor de {x.valor}; sube {y.valor}.")

    # -------------------------------------------------------------
    # 3. INSERCIÓN + CORRECCIÓN
    # -------------------------------------------------------------
    def insertar(self, valor):
        """Inserta un número entero. Devuelve False si ya existe."""
        self.pasos = []
        if self.buscar(valor):
            self._anotar(f"El valor {valor} ya existe: no se permiten duplicados.")
            return False

        nuevo = Nodo(valor, ROJO)
        nuevo.izquierdo = self.NIL
        nuevo.derecho = self.NIL
        nuevo.padre = self.NIL

        padre = self.NIL
        actual = self.raiz
        while actual is not self.NIL:
            padre = actual
            if nuevo.valor < actual.valor:
                actual = actual.izquierdo
            else:
                actual = actual.derecho

        nuevo.padre = padre
        if padre is self.NIL:
            self.raiz = nuevo
        elif nuevo.valor < padre.valor:
            padre.izquierdo = nuevo
        else:
            padre.derecho = nuevo

        self.cantidad += 1
        self._anotar(f"Se inserta {valor} como nodo ROJO.")
        self._corregir_insercion(nuevo)
        return True

    def _corregir_insercion(self, nodo):
        while nodo.padre.color == ROJO:
            abuelo = nodo.padre.padre

            if nodo.padre is abuelo.izquierdo:
                tio = abuelo.derecho
                if tio.color == ROJO:
                    self._anotar(
                        f"Padre {nodo.padre.valor} y tío {tio.valor} ROJOS: "
                        "ambos pasan a NEGRO y el abuelo a ROJO."
                    )
                    nodo.padre.color = NEGRO
                    tio.color = NEGRO
                    abuelo.color = ROJO
                    nodo = abuelo
                else:
                    if nodo is nodo.padre.derecho:
                        self._anotar("Caso izquierda-derecha: se prepara rotación doble.")
                        nodo = nodo.padre
                        self._rotar_izquierda(nodo)
                    nodo.padre.color = NEGRO
                    nodo.padre.padre.color = ROJO
                    self._rotar_derecha(nodo.padre.padre)
            else:
                tio = abuelo.izquierdo
                if tio.color == ROJO:
                    self._anotar(
                        f"Padre {nodo.padre.valor} y tío {tio.valor} ROJOS: "
                        "ambos pasan a NEGRO y el abuelo a ROJO."
                    )
                    nodo.padre.color = NEGRO
                    tio.color = NEGRO
                    abuelo.color = ROJO
                    nodo = abuelo
                else:
                    if nodo is nodo.padre.izquierdo:
                        self._anotar("Caso derecha-izquierda: se prepara rotación doble.")
                        nodo = nodo.padre
                        self._rotar_derecha(nodo)
                    nodo.padre.color = NEGRO
                    nodo.padre.padre.color = ROJO
                    self._rotar_izquierda(nodo.padre.padre)

        if self.raiz.color != NEGRO:
            self._anotar("La raíz se establece en NEGRO.")
        self.raiz.color = NEGRO

    # -------------------------------------------------------------
    # 4. ELIMINACIÓN + CORRECCIÓN
    # -------------------------------------------------------------
    def _trasplantar(self, anterior, nuevo):
        """Sustituye un subárbol por otro."""
        if anterior.padre is self.NIL:
            self.raiz = nuevo
        elif anterior is anterior.padre.izquierdo:
            anterior.padre.izquierdo = nuevo
        else:
            anterior.padre.derecho = nuevo
        # También se actualiza el padre del NIL para corregir eliminaciones.
        nuevo.padre = anterior.padre

    def _minimo(self, nodo):
        while nodo.izquierdo is not self.NIL:
            nodo = nodo.izquierdo
        return nodo

    def eliminar(self, valor):
        """Elimina un número existente y mantiene los invariantes rojo-negro."""
        self.pasos = []
        z = self._encontrar(valor)
        if z is self.NIL:
            self._anotar(f"No se encontró {valor}; no hay nada que eliminar.")
            return False

        y = z
        color_original = y.color

        if z.izquierdo is self.NIL:
            x = z.derecho
            self._trasplantar(z, z.derecho)
        elif z.derecho is self.NIL:
            x = z.izquierdo
            self._trasplantar(z, z.izquierdo)
        else:
            y = self._minimo(z.derecho)  # Sucesor en orden.
            color_original = y.color
            x = y.derecho
            if y.padre is z:
                x.padre = y
            else:
                self._trasplantar(y, y.derecho)
                y.derecho = z.derecho
                y.derecho.padre = y

            self._trasplantar(z, y)
            y.izquierdo = z.izquierdo
            y.izquierdo.padre = y
            y.color = z.color

        self.cantidad -= 1
        self._anotar(f"Se elimina el valor {valor}.")

        if color_original == NEGRO:
            self._anotar("Se retiró un nodo negro: verificar y corregir altura negra.")
            self._corregir_eliminacion(x)
        else:
            self._anotar("El nodo retirado era rojo: no cambia la altura negra.")

        self.raiz.color = NEGRO
        self.NIL.color = NEGRO
        return True

    def _corregir_eliminacion(self, x):
        """Corrección de eliminación, con casos simétricos (algoritmo RB)."""
        while x is not self.raiz and x.color == NEGRO:
            if x is x.padre.izquierdo:
                hermano = x.padre.derecho
                if hermano.color == ROJO:
                    self._anotar("El hermano derecho es ROJO: recolorear y rotar izquierda.")
                    hermano.color = NEGRO
                    x.padre.color = ROJO
                    self._rotar_izquierda(x.padre)
                    hermano = x.padre.derecho

                if (hermano.izquierdo.color == NEGRO and
                        hermano.derecho.color == NEGRO):
                    self._anotar("Hermano negro con hijos negros: trasladar déficit arriba.")
                    if hermano is not self.NIL:
                        hermano.color = ROJO
                    x = x.padre
                else:
                    if hermano.derecho.color == NEGRO:
                        self._anotar("Sobrino interno ROJO: rotación derecha del hermano.")
                        hermano.izquierdo.color = NEGRO
                        hermano.color = ROJO
                        self._rotar_derecha(hermano)
                        hermano = x.padre.derecho

                    self._anotar("Sobrino externo ROJO: recolorear y rotar izquierda.")
                    hermano.color = x.padre.color
                    x.padre.color = NEGRO
                    hermano.derecho.color = NEGRO
                    self._rotar_izquierda(x.padre)
                    x = self.raiz
            else:
                hermano = x.padre.izquierdo
                if hermano.color == ROJO:
                    self._anotar("El hermano izquierdo es ROJO: recolorear y rotar derecha.")
                    hermano.color = NEGRO
                    x.padre.color = ROJO
                    self._rotar_derecha(x.padre)
                    hermano = x.padre.izquierdo

                if (hermano.derecho.color == NEGRO and
                        hermano.izquierdo.color == NEGRO):
                    self._anotar("Hermano negro con hijos negros: trasladar déficit arriba.")
                    if hermano is not self.NIL:
                        hermano.color = ROJO
                    x = x.padre
                else:
                    if hermano.izquierdo.color == NEGRO:
                        self._anotar("Sobrino interno ROJO: rotación izquierda del hermano.")
                        hermano.derecho.color = NEGRO
                        hermano.color = ROJO
                        self._rotar_izquierda(hermano)
                        hermano = x.padre.izquierdo

                    self._anotar("Sobrino externo ROJO: recolorear y rotar derecha.")
                    hermano.color = x.padre.color
                    x.padre.color = NEGRO
                    hermano.izquierdo.color = NEGRO
                    self._rotar_derecha(x.padre)
                    x = self.raiz

        x.color = NEGRO

    # -------------------------------------------------------------
    # 5. CONSULTAS Y VISUALIZACIÓN
    # -------------------------------------------------------------
    def inorden(self):
        elementos = []

        def recorrer(nodo):
            if nodo is self.NIL:
                return
            recorrer(nodo.izquierdo)
            elementos.append(nodo.valor)
            recorrer(nodo.derecho)

        recorrer(self.raiz)
        return elementos

    def altura(self):
        """Altura en aristas; árbol vacío: -1; solo raíz: 0."""
        def medir(nodo):
            if nodo is self.NIL:
                return -1
            return 1 + max(medir(nodo.izquierdo), medir(nodo.derecho))
        return medir(self.raiz)

    def dibujar(self):
        """Dibuja el árbol en consola. N = negro; R = rojo."""
        if self.raiz is self.NIL:
            return "(Árbol vacío)"

        lineas = []

        def agregar(nodo, prefijo, ultimo, etiqueta):
            if nodo is self.NIL:
                return
            rama = "└── " if ultimo else "├── "
            letra = "N" if nodo.color == NEGRO else "R"
            lineas.append(f"{prefijo}{rama}{etiqueta}: {nodo.valor} [{letra}]")
            hijos = []
            if nodo.izquierdo is not self.NIL:
                hijos.append(("I", nodo.izquierdo))
            if nodo.derecho is not self.NIL:
                hijos.append(("D", nodo.derecho))
            siguiente = prefijo + ("    " if ultimo else "│   ")
            for indice, (lado, hijo) in enumerate(hijos):
                agregar(hijo, siguiente, indice == len(hijos) - 1, lado)

        agregar(self.raiz, "", True, "RAÍZ")
        return "\n".join(lineas)

    # -------------------------------------------------------------
    # 6. VERIFICACIÓN DE LAS PROPIEDADES
    # -------------------------------------------------------------
    def verificar_propiedades(self):
        """Devuelve (True/False, explicación). Revisa BST, colores y altura negra."""
        if self.NIL.color != NEGRO:
            return False, "La hoja centinela NIL no es negra."
        if self.raiz is self.NIL:
            if self.cantidad != 0:
                return False, "La cantidad de nodos no coincide con el árbol vacío."
            return True, "Árbol vacío válido."
        if self.raiz.color != NEGRO:
            return False, "La raíz debe ser NEGRA."
        if self.raiz.padre is not self.NIL:
            return False, "La raíz tiene un padre incorrecto."

        visitados = set()
        contador = [0]

        def revisar(nodo, minimo, maximo):
            if nodo is self.NIL:
                return 1  # La hoja NIL cuenta como un nodo negro.
            if nodo is None or nodo.izquierdo is None or nodo.derecho is None:
                raise ValueError("Hay una referencia de hijo incorrecta.")
            if id(nodo) in visitados:
                raise ValueError("Existe un ciclo entre los nodos.")
            visitados.add(id(nodo))
            contador[0] += 1

            if minimo is not None and nodo.valor <= minimo:
                raise ValueError(f"{nodo.valor} viola el orden del BST (límite inferior).")
            if maximo is not None and nodo.valor >= maximo:
                raise ValueError(f"{nodo.valor} viola el orden del BST (límite superior).")
            if nodo.color not in (ROJO, NEGRO):
                raise ValueError(f"Color inválido en el nodo {nodo.valor}.")
            if nodo.izquierdo is not self.NIL and nodo.izquierdo.padre is not nodo:
                raise ValueError(f"Enlace padre-izquierdo incorrecto en {nodo.valor}.")
            if nodo.derecho is not self.NIL and nodo.derecho.padre is not nodo:
                raise ValueError(f"Enlace padre-derecho incorrecto en {nodo.valor}.")
            if nodo.color == ROJO and (nodo.izquierdo.color == ROJO or
                                       nodo.derecho.color == ROJO):
                raise ValueError(f"El nodo ROJO {nodo.valor} tiene un hijo ROJO.")

            izquierda = revisar(nodo.izquierdo, minimo, nodo.valor)
            derecha = revisar(nodo.derecho, nodo.valor, maximo)
            if izquierda != derecha:
                raise ValueError(
                    f"Altura negra distinta debajo de {nodo.valor}: "
                    f"izquierda={izquierda}, derecha={derecha}."
                )
            return izquierda + (1 if nodo.color == NEGRO else 0)

        try:
            altura_negra = revisar(self.raiz, None, None)
            if contador[0] != self.cantidad:
                return False, "El contador de nodos no coincide con los nodos reales."
        except ValueError as error:
            return False, str(error)

        return (True, f"Todas las propiedades se cumplen. "
                      f"Nodos={self.cantidad}, altura={self.altura()}, "
                      f"altura negra (incluyendo NIL)={altura_negra}.")
