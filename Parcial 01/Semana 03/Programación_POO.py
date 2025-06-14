# Clase base que representa una ciudad con sus temperaturas semanales
class Ciudad:
    def __init__(self, nombre, temperaturas):
        self._nombre = nombre                    # Nombre de la ciudad
        self._temperaturas = temperaturas        # Lista 2D: temperaturas por semana y por día

    def calcular_promedios(self, dias_semana):
        # Calcula los promedios semanales de temperatura para la ciudad
        promedios = []
        for semana in self._temperaturas:
            promedio = sum(semana) / len(dias_semana)
            promedios.append(promedio)
        return promedios

    def mostrar_promedios(self, dias_semana):
        # Muestra los promedios de temperatura semanales de la ciudad
        print(f"Promedio de temperaturas para {self._nombre}:")
        promedios = self.calcular_promedios(dias_semana)
        for i, promedio in enumerate(promedios, start=1):
            print(f" Semana {i}: {promedio:.2f} °C")
        print()

# Subclase que representa una ciudad costera, hereda de Ciudad
class CiudadCostera(Ciudad):
    # Sobrescribimos el método para dar un mensaje especial
    def mostrar_promedios(self, dias_semana):
        print(f"(Zona costera) Promedio de temperaturas para {self._nombre}:")
        super().mostrar_promedios(dias_semana)  # Llama al método de la clase base

# Clase que gestiona los datos de temperaturas y las operaciones relacionadas
class GestorTemperaturas:
    def __init__(self):
        # Lista de los días de la semana y número de semanas
        self._dias_semana = ['Domingo', 'Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado']
        self._semanas = 4
        # Crea la lista de objetos Ciudad (o CiudadCostera)
        self._ciudades = self._crear_ciudades()

    def _crear_ciudades(self):
        # Diccionario con los datos de temperaturas por ciudad
        datos_temperaturas = {
            'Quito': [
                [16, 18, 18, 17, 16, 18, 19],
                [20, 21, 18, 18, 16, 16, 17],
                [19, 17, 17, 19, 14, 18, 19],
                [16, 16, 14, 16, 14, 15, 17]
            ],
            'Guayaquil': [
                [35, 34, 34, 31, 31, 32, 31],
                [32, 31, 31, 34, 33, 33, 33],
                [32, 33, 33, 34, 34, 33, 34],
                [33, 33, 32, 34, 32, 33, 33]
            ],
            'Ibarra': [
                [18, 19, 17, 18, 20, 19, 18],
                [19, 20, 18, 17, 19, 20, 19],
                [17, 18, 19, 20, 18, 17, 18],
                [18, 19, 17, 18, 19, 20, 19]
            ],
            'Zamora Chinchipe': [
                [35, 34, 34, 31, 31, 32, 31],
                [32, 31, 31, 34, 33, 33, 33],
                [32, 33, 33, 34, 34, 33, 34],
                [33, 33, 32, 34, 32, 33, 33]
            ]
        }

        ciudades = []
        # Crea instancias de Ciudad o CiudadCostera según el nombre
        for nombre, temperaturas in datos_temperaturas.items():
            if nombre in ['Guayaquil', 'Zamora Chinchipe']:
                ciudades.append(CiudadCostera(nombre, temperaturas))
            else:
                ciudades.append(Ciudad(nombre, temperaturas))
        return ciudades

    def mostrar_resultados(self):
        # Muestra un mensaje introductorio y los promedios por ciudad
        print("Hola, a continuación se muestra la temperatura durante el día que tuvieron las ciudades de "
              "Quito, Guayaquil, Ibarra y Zamora Chinchipe en las 4 semanas del mes de febrero del 2025\n")
        for ciudad in self._ciudades:
            ciudad.mostrar_promedios(self._dias_semana)  # Polimorfismo

# Función principal que inicia el programa
def main():
    gestor = GestorTemperaturas()  # Instancia del gestor
    gestor.mostrar_resultados()    # Muestra los resultados

# Ejecutar el programa
main()
