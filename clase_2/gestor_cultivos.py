class Cultivo:
    def __init__(self, nombre : str, hectareas : int, produccion_toneladas: int):
        self.nombre = nombre
        self.hectareas = hectareas
        self.produccion_toneladas = produccion_toneladas
    
    def calcular_rendimiento_por_hectareas(self):
        if self.hectareas == 0:
            return 0
        return self.produccion_toneladas / self.hectareas


class GestorCultivos:

    def __init__(self, lista_cultivos : list[Cultivo]):
        self.lista_cultivos = lista_cultivos
    def mostrar_cultivos(self):
        if len(self.lista_cultivos) == 0 or not self.lista_cultivos:
            return None
        for cultivo in self.lista_cultivos:
            print(f"{cultivo.nombre} tiene un rendimiento de {cultivo.calcular_rendimiento_por_hectareas()} por hectarea")
    def cultivo_mayor_rendimiento(self):
        if len(self.lista_cultivos) == 0 or not self.lista_cultivos:
            return None
        cultivo_mayor = self.lista_cultivos[0]
        for cultivo in self.lista_cultivos:
            if cultivo.calcular_rendimiento_por_hectareas() > cultivo_mayor.calcular_rendimiento_por_hectareas():
                cultivo_mayor = cultivo
        return cultivo_mayor

cultivo_1 = Cultivo("papa", 100, 200)
cultivo_2 = Cultivo("maiz", 200, 300)
cultivo_3 = Cultivo("arroz", 300, 400)

gestor_cultivos = GestorCultivos([cultivo_1, cultivo_2, cultivo_3])
gestor_cultivos.mostrar_cultivos()
cultivo_mayor = gestor_cultivos.cultivo_mayor_rendimiento()
print(f"El cultivo con mayor rendimiento es {cultivo_mayor.nombre} con un rendimiento de {cultivo_mayor.calcular_rendimiento_por_hectareas()} por hectarea")

        
