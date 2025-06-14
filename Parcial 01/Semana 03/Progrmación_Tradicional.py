# Función que devuelve los datos necesarios para el análisis de temperaturas
def obtener_datos():
    # Lista de nombres de las ciudades analizadas
    ciudades = ['Quito', 'Guayaquil', 'Ibarra', 'Zamora Chinchipe']

    # Lista de días de la semana
    dias_semana = ['Domingo', 'Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado']

    # Número de semanas analizadas
    semanas = 4

    # Matriz tridimensional que contiene las temperaturas por ciudad, por semana y por día
    temperaturas = [
        [  # Quito
            [16, 18, 18, 17, 16, 18, 19],  # Semana 1
            [20, 21, 18, 18, 16, 16, 17],  # Semana 2
            [19, 17, 17, 19, 14, 18, 19],  # Semana 3
            [16, 16, 14, 16, 14, 15, 17]  # Semana 4
        ],
        [  # Guayaquil
            [35, 34, 34, 31, 31, 32, 31],
            [32, 31, 31, 34, 33, 33, 33],
            [32, 33, 33, 34, 34, 33, 34],
            [33, 33, 32, 34, 32, 33, 33]
        ],
        [  # Ibarra
            [18, 19, 17, 18, 20, 19, 18],
            [19, 20, 18, 17, 19, 20, 19],
            [17, 18, 19, 20, 18, 17, 18],
            [18, 19, 17, 18, 19, 20, 19]
        ],
        [  # Zamora Chinchipe
            [35, 34, 34, 31, 31, 32, 31],
            [32, 31, 31, 34, 33, 33, 33],
            [32, 33, 33, 34, 34, 33, 34],
            [33, 33, 32, 34, 32, 33, 33]
        ]
    ]

    # Retorna todos los datos necesarios
    return ciudades, dias_semana, semanas, temperaturas


# Función que calcula los promedios semanales de temperatura por ciudad
def calcular_promedios(ciudades, dias_semana, semanas, temperaturas):
    promedios = []  # Lista para guardar los promedios por ciudad

    # Itera sobre cada ciudad
    for ciudad in range(len(ciudades)):
        promedios_ciudad = []  # Lista temporal para guardar los promedios por semana

        # Itera por cada semana de esa ciudad
        for semana in range(semanas):
            suma_temperaturas = sum(temperaturas[ciudad][semana])  # Suma de temperaturas de la semana
            promedio = suma_temperaturas / len(dias_semana)  # Cálculo del promedio semanal
            promedios_ciudad.append(promedio)  # Agrega el promedio a la lista de la ciudad

        promedios.append(promedios_ciudad)  # Agrega los promedios semanales de la ciudad a la lista general

    return promedios  # Retorna la matriz de promedios por ciudad


# Función que imprime los resultados de los promedios calculados
def mostrar_resultados(ciudades, promedios):
    print("Hola, a continuación se muestra la temperatura durante el día que tuvieron las ciudades de "
          "Quito, Guayaquil, Ibarra y Zamora Chinchipe en las 4 semanas del mes de febrero del 2025\n")

    # Recorre cada ciudad y sus promedios
    for i, ciudad in enumerate(ciudades):
        print(f"Promedio de temperaturas para {ciudad}:")
        for semana, promedio in enumerate(promedios[i], start=1):
            print(f" Semana {semana}: {promedio:.2f} °C")  # Muestra el promedio con dos decimales
        print()  # Línea en blanco para separar ciudades


# Función principal que organiza el flujo del programa
def main():
    # Obtiene los datos base
    ciudades, dias_semana, semanas, temperaturas = obtener_datos()

    # Calcula los promedios semanales por ciudad
    promedios = calcular_promedios(ciudades, dias_semana, semanas, temperaturas)

    # Muestra los resultados
    mostrar_resultados(ciudades, promedios)


# Punto de entrada del programa: ejecuta la función principal
main()
