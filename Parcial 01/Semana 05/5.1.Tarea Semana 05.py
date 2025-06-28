# El siguiente programa es desarrollado para calcular el área de un triángulo Equilátero
# usando la fórmula matemática: (base * altura) / 2.
# El programa solicita al usuario la base y la altura, valida los datos ingresados,
# realiza el cálculo del área y muestra el resultado.

def calcular_area_triangulo(base: float, altura: float) -> float:
    """
    Calcula el área de un triángulo dada la base y la altura.
    :param base: longitud de la base del triángulo (float)
    :param altura: altura del triángulo desde la base (float)
    :return: área del triángulo (float)
    """
    return (base * altura) / 2

# Solicita el nombre del usuario (tipo string)
nombre_usuario: str = input("Ingresa tu nombre: ")

# Mensaje de bienvenida personalizado
print(f"Hola, {nombre_usuario}. Vamos a calcular el área de un triángulo.")

# Solicita la base del triángulo (tipo float)
base_valida: bool = False
while not base_valida:
    try:
        base_triangulo: float = float(input("Ingresa la base del triángulo (en metros): "))
        if base_triangulo > 0:
            base_valida = True
        else:
            print("La base debe ser un número positivo.")
    except ValueError:
        print("Por favor, ingresa un número válido.")

# Solicita la altura del triángulo (tipo float)
altura_valida: bool = False
while not altura_valida:
    try:
        altura_triangulo: float = float(input("Ingresa la altura del triángulo (en metros): "))
        if altura_triangulo > 0:
            altura_valida = True
        else:
            print("La altura debe ser un número positivo.")
    except ValueError:
        print("Por favor, ingresa un número válido.")

# Calcula el área usando la función definida
area_triangulo: float = calcular_area_triangulo(base_triangulo, altura_triangulo)

# Muestra el resultado con dos decimales
print(f"{nombre_usuario}, el área del triángulo es: {area_triangulo:.2f} metros cuadrados.")
