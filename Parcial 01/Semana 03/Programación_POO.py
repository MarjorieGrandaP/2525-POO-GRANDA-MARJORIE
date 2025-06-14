# --- 1. Definición de Datos ---

# Nombres de las ciudades.
ciudades = ['Quito', 'Guayaquil', 'Ibarra', 'Zamora Chinchipe']

# Días de la semana. Usado aquí principalmente para obtener la cantidad de días por semana.
dias_semana = ['Domingo', 'Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado']

# Número fijo de semanas en el mes para este análisis.
semanas = 4

# Mensaje inicial para el usuario.
print("Hola, a continuación se muestra la temperatura semanal promedio de "
      "Quito, Guayaquil, Ibarra y Zamora Chinchipe en las 4 semanas del mes de febrero del 2025.")

# --- 2. Temperaturas Ficticias Organizadas ---
# Esta es una "matriz 3D": [ciudad][semana][día]
# Contiene los datos de temperatura para cada ciudad, por semana y por día.
temperaturas = [
    [   # Quito (índice 0)
        [16, 18, 18, 17, 16, 18, 19],  # Semana 1
        [20, 21, 18, 18, 16, 16, 17],  # Semana 2
        [19, 17, 17, 19, 14, 18, 19],  # Semana 3
        [16, 16, 14, 16, 14, 15, 17]   # Semana 4
    ],
    [   # Guayaquil (índice 1)
        [35, 34, 34, 31, 31, 32, 31],  # Semana 1
        [32, 31, 31, 34, 33, 33, 33],  # Semana 2
        [32, 33, 33, 34, 34, 33, 34],  # Semana 3
        [33, 33, 32, 34, 32, 33, 33]   # Semana 4
    ],
    [   # Ibarra (índice 2)
        [18, 19, 17, 18, 20, 19, 18],  # Semana 1
        [19, 20, 18, 17, 19, 20, 19],  # Semana 2
        [17, 18, 19, 20, 18, 17, 18],  # Semana 3
        [18, 19, 17, 18, 19, 20, 19]   # Semana 4
    ],
    [   # Zamora Chinchipe (índice 3)
        [35, 34, 34, 31, 31, 32, 31],  # Semana 1
        [32, 31, 31, 34, 33, 33, 33],  # Semana 2
        [32, 33, 33, 34, 34, 33, 34],  # Semana 3
        [33, 33, 32, 34, 32, 33, 33]   # Semana 4
    ]
]

# --- 3. Cálculo de Promedios Semanales ---

# Esta lista almacenará los promedios calculados para todas las ciudades.
# Su estructura será: [[promedios_semanales_ciudad1], [promedios_semanales_ciudad2], ...]
promedios_por_ciudad_y_semana = []

# Iteramos a través de cada ciudad usando su índice (0, 1, 2, 3).
for i_ciudad in range(len(ciudades)):
    # Para cada ciudad, creamos una lista vacía donde guardaremos sus 4 promedios semanales.
    promedios_semanales_ciudad_actual = []

    # Iteramos a través de las 4 semanas.
    for i_semana in range(semanas):
        # Obtenemos la lista de temperaturas para la semana actual de la ciudad actual.
        # Por ejemplo, en la primera iteración sería: temperaturas[0][0] (Semana 1 de Quito).
        temperaturas_semana_actual = temperaturas[i_ciudad][i_semana]

        # Calculamos la suma de las temperaturas de esa semana usando sum().
        suma_temperaturas = sum(temperaturas_semana_actual)

        # Calculamos el promedio: suma total dividida por el número de días en la semana (7).
        promedio_semanal = suma_temperaturas / len(dias_semana)

        # Añadimos este promedio semanal a la lista de promedios de la ciudad actual.
        promedios_semanales_ciudad_actual.append(promedio_semanal)

    # Una vez que tenemos los 4 promedios semanales de una ciudad,
    # los añadimos a la lista principal de promedios.
    promedios_por_ciudad_y_semana.append(promedios_semanales_ciudad_actual)

# --- 4. Mostrar Resultados ---

print("\n--- Promedios de Temperaturas por Ciudad y Semana ---")

# Iteramos de nuevo sobre las ciudades, usando enumerate para obtener tanto el índice (i_ciudad)
# como el nombre de la ciudad (nombre_ciudad).
for i_ciudad, nombre_ciudad in enumerate(ciudades):
    print(f"**{nombre_ciudad}**:") # Imprimimos el nombre de la ciudad.

    # Iteramos sobre los promedios semanales que calculamos para esta ciudad.
    # Usamos i_semana para mostrar "Semana 1", "Semana 2", etc.
    for i_semana in range(semanas):
        # Accedemos al promedio correcto usando los índices de ciudad y semana.
        promedio_a_mostrar = promedios_por_ciudad_y_semana[i_ciudad][i_semana]
        # Imprimimos el promedio formateado a dos decimales.
        print(f"  Semana {i_semana + 1}: {promedio_a_mostrar:.2f} °C")
    print("-" * 30) # Un separador visual para cada ciudad.

print("\nCálculo de promedios semanales finalizado.")