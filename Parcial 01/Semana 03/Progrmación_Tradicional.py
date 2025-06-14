# Definimos las ciudades y los días de la semana
ciudades = ['Quito', 'Guayaquil', 'Ibarra', 'Zamora Chinchipe']
dias_semana = ['Domingo', 'Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado']
semanas = 4  # Número de semanas
print ("Hola a continuación se muestra la temperatura durante el día que tuvieron las ciudades de "
       "Quito, Guayaquil, Ibarra y Zamora Chinchipe en las 4 semanas del mes de febrero del 2025")
# Creamos una matriz 3D con temperaturas ficticias
# La estructura es: [ciudad][semana][dia]
temperaturas = [
    [  # Quito
        [16, 18, 18, 17, 16, 18, 19],  # Semana 1
        [20, 21, 18, 18, 16, 16, 17],  # Semana 2
        [19, 17, 17, 19, 14, 18, 19],  # Semana 3
        [16, 16, 14, 16, 14, 15, 17]   # Semana 4
    ],
    [  # Guayaquil
        [35, 34, 34, 31, 31, 32, 31],  # Semana 1
        [32, 31, 31, 34, 33, 33, 33],  # Semana 2
        [32, 33, 33, 34, 34, 33, 34],  # Semana 3
        [33, 33, 32, 34, 32, 33, 33]   # Semana 4
    ],
    [  # Ibarra
        [18, 19, 17, 18, 20, 19, 18],  # Semana 1
        [19, 20, 18, 17, 19, 20, 19],  # Semana 2
        [17, 18, 19, 20, 18, 17, 18],  # Semana 3
        [18, 19, 17, 18, 19, 20, 19]   # Semana 4
    ],
    [  # Zamora Chinchipe
        [35, 34, 34, 31, 31, 32, 31],  # Semana 1
        [32, 31, 31, 34, 33, 33, 33],  # Semana 2
        [32, 33, 33, 34, 34, 33, 34],  # Semana 3
        [33, 33, 32, 34, 32, 33, 33]   # Semana 4
    ]
]

# Calculamos el promedio de temperaturas por ciudad y semana
promedios = []

for ciudad in range(len(ciudades)):
    promedios_ciudad = []
    for semana in range(semanas):
        suma_temperaturas = sum(temperaturas[ciudad][semana])
        promedio = suma_temperaturas / len(dias_semana)
        promedios_ciudad.append(promedio)
    promedios.append(promedios_ciudad)

# Mostramos los resultados
for i, ciudad in enumerate(ciudades):
    print(f"Promedio de temperaturas para {ciudad}:")
    for semana in range(semanas):
        print(f"  Semana {semana + 1}: {promedios[i][semana]:.2f} °C")