from math import sqrt
import numpy as np

class MatrizMesas:
    def __init__(self, Cantidad_De_Mesas: int):

        raiz_cuadrada = sqrt(Cantidad_De_Mesas)

        if not raiz_cuadrada.is_integer():
            raise ValueError("la sala debe ser cuadrada!")

        if raiz_cuadrada not in(4, 5, 6, 8):
            raise ValueError("Dimensiones no validas para el restaurante!")
        
        
        self.filas = int(raiz_cuadrada)
        self.columnas = int(raiz_cuadrada)
        self.cantidad_mesas = Cantidad_De_Mesas
        letras_alfabeto = ('A','B','C','D','E','F','G','H','I','J','K','L','M','N','Ñ','O','P','Q','R','S','T','U','V','W','X','Y','Z')
        self.letras_filas = letras_alfabeto[:self.filas] 
        self.tamaño_mesas = {
                    "m": 2, ##morado
                    "v": 4, ##verde
                    "a": 8 ##azul
                }
        self.matriz = self.generar_matriz()

        
    def generar_matriz(self):
        """
        Genera la matriz de mesas con un patrón de colores/capacidades.
        Las letras indican colores: 'v' (verde) = 4 personas,
                                     'm' (morado) = 2 personas,
                                     'a' (azul) = 8 personas.
        El patrón depende del tamaño total de la matriz.
        """
        base = ("v", "m", "a")


        # Determina con qué letra (color) empieza la matriz
        if self.cantidad_mesas == 16:
            inicio = "m"  # para 4x4
        elif self.cantidad_mesas == 36:
            inicio = "a"  # para 6x6
        else:
            inicio = "v"

        i = base.index(inicio)
        base = base[i:] + base[:i]  # rota la base para cambiar el orden

        matriz = np.empty((self.filas, self.columnas), dtype=object)  # matriz numpy de objetos
        for i in range(self.filas):
            for j in range(self.columnas):
                letra = base[(j - i) % len(base)]  # patrón para alternar letras   
                identificador = f"{self.letras_filas[i]}{j+1}" # identificador de la mesa

                # Asigna un diccionario a cada celda de la matriz
                matriz[i, j] = { 
                    "id": identificador,
                    "capacidad": self.tamaño_mesas[letra],
                    "ocupado": False,
                    "letra": letra
                }
        return matriz
