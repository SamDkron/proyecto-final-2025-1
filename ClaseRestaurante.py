from datetime import datetime, time
from ClaseMesas import *
from random import randint 
from ClaseCliente import Cliente


class Restaurante:
    def __init__(self, ciudad: str, direccion, horario_apertura: time, horario_cierre: time , cantidad_de_mesas: int):
        if cantidad_de_mesas not in (16, 25, 36, 64):
            raise ValueError("La cantidad de mesas debe ser 16, 25, 36 o 64")
        if ciudad == "" or direccion == "" or horario_apertura == "" or horario_cierre == "":
            raise ValueError("La ciudad, dirección y horario no pueden estar vacíos")
        
        self.ciudad = ciudad
        self.direccion = direccion
        self.horario_apertura = horario_apertura
        self.horario_cierre = horario_cierre
        self.mesas = MatrizMesas(cantidad_de_mesas)
        self.fecha_creacion = datetime.now().date()
        self.consumo = {}


    def determinar_mesa_disponible(self, personas: int):
        """
        Busca mesas disponibles que puedan alojar al menos 'personas'.
        Retorna una mesa aleatoria disponible adecuada.
        """
        opciones = []
        for i in range(self.mesas.filas): ##recorre filas
            for j in range(self.mesas.columnas): ##recorre columnas
                mesa = self.mesas.matriz[i][j] ## accede a la mesa
                ##verifica si la mesa no está ocupada y si la capacidad es mayor o igual a la cantidad de personas
                if not mesa["ocupado"] and mesa["capacidad"] >= personas: 
                    opciones.append((i, j)) ## agrega la posición de la mesa a las opciones
        ##si no hay opciones, lanza una excepción
        if not opciones:
            raise ValueError(f"No hay mesas disponibles para {personas} personas")
        ##si hay opciones, selecciona una aleatoria
        ##y retorna la fila y columna de la mesa    
        return opciones[randint(0, len(opciones) - 1)]
        
        
    def AsignarMesa(self, cantidad_personas: int, cliente: Cliente):
        if cantidad_personas is None:
            raise ValueError("La cantidad de personas no puede estar vacía")
        
        if cantidad_personas < 2  or cantidad_personas > 8:
            raise ValueError("La cantidad de personas debe ser entre 2 y 8")
        
        if cliente.calcular_edad_actual_años() < 18:
            raise ValueError("El cliente debe ser mayor de edad para reservar una mesa")
        

        fila, columna = self.determinar_mesa_disponible(cantidad_personas) 
        mesa = self.mesas.matriz[fila][columna]
        if mesa["ocupado"]:
            raise ValueError("La mesa ya está ocupada")
        
        mesa["ocupado"] = True  # Marcar como ocupada
        mesa["Hora_llegada"] = datetime.now()  # Guardar la hora de llegada
        mesa["Hora_salida"] = None  # Inicialmente no hay hora de salida
        return mesa["id"]   # Retornar el id de la mesa
    

    def liberar_mesa(self, id_mesa: str): #Se le ingresa el id de la mesa que se quiere liberar
        for i in range(self.mesas.filas):
            for j in range(self.mesas.columnas):
                if self.mesas.matriz[i][j]["id"] == id_mesa: #Busca la mesa en la matriz
                    self.mesas.matriz[i][j]["ocupado"] = False #Marca la mesa como no ocupada
                    self.mesas.matriz[i][j]["Hora_salida"] = datetime.now()
                    return
        raise ValueError("La mesa no existe o no está ocupada") #Si no se encuentra la mesa o si está vacía, lanza una excepción
    
    
    def zona_mesas_mas_utilizadas(self):
        uso_mesas = {2: {"total": 0, "ocupadas": 0, "libres": 0},
                    4: {"total": 0, "ocupadas": 0, "libres": 0},  #crea un diccionario para almacenar el uso de las mesas
                    8: {"total": 0, "ocupadas": 0, "libres": 0}}

        for fila in self.mesas.matriz:
            for mesa in fila: #recorre la matriz de mesas
                capacidad = mesa["capacidad"] #obtiene la capacidad de la mesa
                uso_mesas[capacidad]["total"] += 1 #le suma 1 al numero total de mesas de esa capacidad
                if mesa["ocupado"]:
                    uso_mesas[capacidad]["ocupadas"] += 1 #le suma 1 al numero de mesas ocupadas de esa capacidad
                else:
                    uso_mesas[capacidad]["libres"] += 1 #le suma 1 al numero de mesas libres de esa capacidad
        return uso_mesas
    ##comentarios antes de la función:
    ##1. las capacidades de las mesas son 2, 4 y 8 y se ejecuta una vez el for para cada una de ellas
    ##2. el diccionario de uso de mesas es un diccionario que almacena la cantidad total de mesas de cada capacidad, la cantidad de mesas ocupadas y la cantidad de mesas libres


    def calcular_zona_mesas_mas_utilizada_y_tasa_ocupacion_sede_especifica(self):
        uso_mesas = self.calcular_zona_mesas_mas_utilizadas()
        zona_mas_ocupada = None
        max_ocupadas = 0
        tasa_ocupacion = 0
        hay_ocupadas = False
        for capacidad, valores in uso_mesas.items(): ## recorre el diccionario de uso de mesas
            ocupadas = valores["ocupadas"] ## obtiene el total de mesas ocupadas de esa capacidad
            total = valores["total"] ## obtiene el total de mesas de esa capacidad
            if ocupadas > 0: ## si hay mesas ocupadas de esa capacidad
                hay_ocupadas = True 
            if ocupadas > max_ocupadas: ## si la cantidad de mesas ocupadas de esa capacidad es mayor a la cantidad de mesas ocupadas de la zona más ocupada
                zona_mas_ocupada = capacidad ## asigna la capacidad de la zona más ocupada
                max_ocupadas = ocupadas ## actualiza la cantidad de mesas ocupadas de la zona más ocupada
                tasa_ocupacion = (ocupadas / total) * 100 if total > 0 else 0 ## calcula la tasa de ocupación de la zona más ocupada
        if not hay_ocupadas: 
            return None, 0.0  # No hay mesas ocupadas en ninguna zona
        return zona_mas_ocupada, tasa_ocupacion 



    def calcular_tasa_ocupacion(self, uso_mesas): #llama al diccionario de uso de mesas 
        for capacidad, valores in uso_mesas.items(): #recorre el diccionario de uso de mesas
            total = valores["total"] #obtiene el total de mesas de la capacidad que estamos trabajando
            ocupadas = valores["ocupadas"] #obtiene el total de mesas ocupadas de esa capacidad
            if total > 0: #si el numero total de mesas de la capacidad que estamos trabajando es mayor a 0
                tasa_ocupacion = (ocupadas / total) #calcula la tasa de ocupación
            else:
                tasa_ocupacion = 0 #si no hay mesas de esa capacidad, la tasa de ocupación es 0
            print(f"Capacidad {capacidad}: Tasa de ocupación: {tasa_ocupacion:.2f}%")

    def agregar_consumo_mesa(self, id_mesa: str, producto: str, precio: float):
        if producto.lower() not in ("rapida", "tradicional", "saludable", "gourmet"):
            raise ValueError("El producto no es válido. Debe ser uno de los siguientes: rapida, tradicional, saludable, gourmet")
        if precio <= 0:
            raise ValueError("El precio debe ser mayor a 0")
        for i in range(self.mesas.filas):  # Recorre las filas de la matriz de mesas
            for j in range(self.mesas.columnas):    # Recorre las columnas de la matriz de mesas
                mesa = self.mesas.matriz[i][j]  # Accede a la mesa en la posición (i, j)
                if mesa["id"] == id_mesa: # Verifica si el id de la mesa coincide
                    if not mesa.get("consumo"):     # Si no hay consumo registrado, inicializa el diccionario
                        mesa["consumo"] = {}  
                    if producto in mesa["consumo"]: # Si el producto ya existe en el consumo de la mesa, suma el precio
                        mesa["consumo"][producto] += precio 
                    else:  # Si el producto no existe, lo agrega con el precio
                        mesa["consumo"][producto] = precio 
                    # Agregar al consumo general del restaurante
                    if producto in self.consumo:  ## Verifica si el producto ya existe en el consumo general
                        self.consumo[producto] += precio  # Si existe, suma el precio al consumo general
                    else: 
                        self.consumo[producto] = precio # Si no existe, lo agrega con el precio
                    return
        raise ValueError("La mesa no existe.")
    
    def mostrar_consumo_mesa(self, id_mesa: str, incluir_propina: str):
        for i in range(self.mesas.filas):
            for j in range(self.mesas.columnas):
                mesa = self.mesas.matriz[i][j]
                if mesa["id"] == id_mesa:
                    consumo = mesa.get("consumo", {})
                    if not consumo:
                        print("No hay consumo registrado para esta mesa.")
                        return
                    print(f"Consumo de la mesa {id_mesa}:")
                    subtotal = sum(consumo.values())
                    for producto, precio in consumo.items():
                        print(f"{producto}: ${precio:.2f}")
                    print(f"Subtotal: ${subtotal:.2f}")
                    if incluir_propina.lower() == "si":
                        propina = subtotal * 0.10
                        print(f"Propina: ${propina:.2f}")
                        print(f"Total: ${subtotal + propina:.2f}")
                    else:
                        print(f"Total: ${subtotal:.2f}")
                    return
        print("La mesa no existe.")
    
    def tiempo_promedio_permanencia(self, fecha: str):
        """
        Calcula el tiempo promedio de permanencia (en minutos) de los grupos en la sede para una fecha dada (YYYY-MM-DD).
        """
        try:
            datetime.strptime(fecha, "%Y-%m-%d")  # Verifica que la fecha esté en el formato correcto
        except ValueError:
            raise ValueError("La fecha debe estar en el formato YYYY-MM-DD")
        
        total_tiempo = 0
        conteo = 0
        for fila in self.mesas.matriz: 
            for mesa in fila:
                llegada = mesa.get("hora_llegada") #obtiene la hora de llegada
                salida = mesa.get("hora_salida") #obtiene la hora de salida
                if llegada and salida: #verifica si hay hora de llegada y salida
                    if llegada.date().isoformat() == fecha and salida.date().isoformat() == fecha: #ambas fechas deben coincidir
                        minutos = (salida - llegada).total_seconds() / 60 #calcula la diferencia en minutos
                        total_tiempo += minutos  #suma el tiempo total
                        conteo += 1 #incrementa el conteo
        if conteo == 0:
            return 0
        return total_tiempo / conteo  # Promedio en minutos
    
    def porcentaje_productos_consumidos_por_categoría_sede_especifica(self):
        total = sum(self.consumo.values())
        if total == 0:
            print("No se ingresaron los productos correctamente")
            return
        for categoria, valor in self.consumo.items():
            porcentaje = (valor / total) * 100
            print(f"Porcentaje de productos consumidos en comida {categoria}: {porcentaje:.2f}%")
