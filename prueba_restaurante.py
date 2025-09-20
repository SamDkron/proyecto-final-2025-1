from ClaseRestaurante import Restaurante
from ClaseCliente import Cliente
from ClaseEmpresa import Empresa
from datetime import date

##historia de usuario 1
restaurante1 = Restaurante('Santa Marta', 'Cra 1 #2-3', '08:00', '22:00', 16)
print(f"Restaurante creado: {restaurante1.ciudad}, {restaurante1.direccion}, Horario: {restaurante1.horario_apertura} - {restaurante1.horario_cierre}, Mesas: {restaurante1.cantidad_de_mesas}")
restaurante2 = Restaurante('Barranquilla', 'Cra 2 #3-4', '09:00', '23:00', 20) ##error en mesas
print(f"Restaurante creado: {restaurante2.ciudad}, {restaurante2.direccion}, Horario: {restaurante2.horario_apertura} - {restaurante2.horario_cierre}, Mesas: {restaurante2.cantidad_de_mesas}")    

##historia de usuario 2 y 3
id_mesa = restaurante1.AsignarMesa(2, "Carlos Gomez")
print(f"Mesa asignada: {id_mesa}")
id_mesa2 = restaurante1.AsignarMesa(8, "Maria Lopez") 
print(f"Mesa asignada: {id_mesa2}")

##Historia de usuario 4
restaurante1.agregar_consumo_mesa(id_mesa, 'rapida', 25000)
restaurante1.agregar_consumo_mesa(id_mesa, 'gourmet', 40000)
print(restaurante1.mostrar_consumo_mesa(id_mesa, 'si')) 
print("Sin propina")
print(restaurante1.mostrar_consumo_mesa(id_mesa, 'no'))

##Historia de usuario 5
restaurante1.liberar_mesa(id_mesa)
print(f"Mesa {id_mesa} liberada.")
restaurante1.liberar_mesa() ##mesa no asignada
print("Mesa libre.")

##Historia de usuario 6
print(restaurante1.calcular_zona_mesas_mas_utilizada_y_tasa_ocupacion_sede_especifica())
print(restaurante2.calcular_zona_mesas_mas_utilizadas_y_tasa_ocupacion_sede_especifica())

##Historia de usuario 7
print(restaurante1.porcentaje_productos_consumidos_por_categoría_sede_especifica())
print(restaurante2.porcentaje_productos_consumidos_por_categoría_sede_especifica())

##historia de usuario 8

empresa = Empresa('MiEmpresa')

empresa.agregar_restaurante('Santa Marta', 'Cra 1 #2-3', '08:00', '22:00', 16)
empresa.agregar_restaurante('Barranquilla', 'Cra 2 #3-4', '09:00', '23:00', 25)
restaurante3 = empresa.restaurantes[0]
cliente1 = Cliente('Juan Perez', date(2000, 5, 10), 'M')
cliente2 = Cliente('Ana Lopez', date(1998, 8, 20), 'F')

id_mesa = restaurante3.AsignarMesa(2, cliente1)
print(f"Mesa asignada: {id_mesa}")
restaurante3.agregar_consumo_mesa(id_mesa, 'rapida', 25000)
restaurante3.agregar_consumo_mesa(id_mesa, 'gourmet', 40000)
print("zobra de mesas más utilizada y tasa de ocupación general:")
print(empresa.calcular_zona_mesas_mas_utilizadas_y_tasa_ocupacion_sedes_general())

##historia de usuario 9
print("Porcentaje de productos consumidos por categoría en todas las sedes:")
print(empresa.porcentaje_productos_consumidos_por_categoria_general())

##historia de usuario 10
print("Tiempo promedio de permanencia en el restaurante:")
print(restaurante3.tiempo_promedio_permanencia())

restaurante4 =  empresa.restaurantes[1]
print(restaurante4.tiempo_promedio_permanencia())
