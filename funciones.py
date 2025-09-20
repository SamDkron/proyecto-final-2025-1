from datetime import datetime, date

def esEntero(mensaje)->bool:
    try:
        mensaje = int(mensaje)
        return True
    except ValueError:
        return False
    
def esPositivo(número)->bool:
    return número > 0

def esMayorOIgualA0(número)->bool:
    return número >= 0

def pedirOpcion()->int:
    while True:
        opc = input("Ingrese una opción: ")
        if esEntero(opc) and opc in ("1", "2"):
            return int(opc)
        else:
            print("Solo opciones númericas en rango [1,2]")

def pedirNombreyApellido(opción:str)->str:
    while True:
        texto = input(f"Ingrese el {opción} del aspirante: ").strip()
        partes = texto.split()
        if all(parte.isalpha() and len(parte) >= 2 for parte in partes) and len(partes) >= 2:
            return texto
        else:
            print(f"Error, {opción} no permitido. Debe ingresar al menos nombre y apellido, cada uno con al menos 2 letras y sin números.")

def pedirPeso()->float:
    while True:
        try: 
            peso = float(input(f"Ingrese el peso del aspirante: "))
            if esPositivo(peso):
                return peso
            else:
                print("El peso debe ser positivo.")
        except:
            print("El peso debe ser un número.")

def pedirDisparosGolesAsistencias(opción:str)->int:
    while True:
        valor = input(f"Ingrese el número de {opción}: ")
        if esEntero(valor):
            if esMayorOIgualA0(int(valor)):
                return int(valor)
            else:
                print("No se permiten números negativos.")
        else:
            print("Solo se permiten números enteros.")

def validar_entero_positivo(mensaje):
    while True:
        try:
            valor = int(input(mensaje))
            if valor > 0:
                return valor
            else:
                print("El valor debe ser un número entero positivo.")
        except ValueError:
            print("Por favor, ingrese un número entero válido.")

def validar_cadena_caracteres(mensaje):
    while True:
            texto = input(mensaje)
            if texto.isalpha():
                return texto
            elif not texto:
                print("No puede dejar este espacio vacío")
            else:
                print("Ingrese unicamente letras, sin números o caracteres especiales")

def validar_horario_apertura_cierre(mensaje):
    formato = "%H:%M"
    while True:
        horario = input(mensaje)
        partes = horario.strip().split()
        if len(partes) != 2:
            print("Debe ingresar dos horarios: apertura y cierre, separados por un espacio.")
            continue
        try:
            apertura = datetime.strptime(partes[0], formato)
            cierre = datetime.strptime(partes[1], formato)
            if apertura < cierre:
                return partes[0], partes[1]
            else:
                print("El horario de apertura debe ser anterior al de cierre.")
        except ValueError:
            print("Formato incorrecto. Use HH:MM para ambos horarios.")

def pedir_fecha_nacimiento(): #valida que la fecha de nacimiento del cliente sea valida
    while True:
        fecha_str = input("Ingrese la fecha de nacimiento (YYYY-MM-DD): ")
        try:
            fecha = datetime.strptime(fecha_str, "%Y-%m-%d").date()
            if fecha >= date.today():
                print("La fecha debe ser anterior a hoy.")
            else:
                return fecha
        except ValueError:
            print("Formato incorrecto. Use YYYY-MM-DD.")

def pedir_sexo_biologico(): #Valida que el sexo bilogico del cliente exista
    while True:
        sexo = input("Ingrese el sexo biológico (M/F): ").strip().upper()
        if sexo in ("M", "F"):
            return sexo
        else:
            print("Solo se permite 'M' o 'F'.")

