class Estudiante:
    # Clase que representa a un estudiante con nombre y edad

    def __init__(self, nombre, edad):
        # Constructor: inicializa los atributos nombre y edad
        self.nombre = nombre
        self.edad = edad
        print(f"Estudiante {self.nombre}, de {self.edad} años, ha sido creado.")

    def mostrar_informacion(self):
        # Muestra los datos del estudiante
        print(f"Nombre: {self.nombre}")
        print(f"Edad: {self.edad}")

    def __del__(self):
        # Destructor: se ejecuta automáticamente al eliminar el objeto
        print(f"Estudiante {self.nombre} ha sido eliminado de la memoria.")


# Crear varios estudiantes

# Lista para guardar los objetos
lista_estudiantes = []

# Crear 3 estudiantes
lista_estudiantes.append(Estudiante("Ana Alvarez", 20))
lista_estudiantes.append(Estudiante("Luis Delgado", 22))
lista_estudiantes.append(Estudiante("María Vasquez", 19))

print("\nMostrando información de los estudiantes:\n")

# Mostrar la información de cada uno
for estudiante in lista_estudiantes:
    estudiante.mostrar_informacion()
    print("-----------")

# Eliminar los objetos (opcional, también se eliminarán automáticamente al finalizar el programa)
print("\nEliminando estudiantes:")
for estudiante in lista_estudiantes:
    del estudiante

# Vaciar la lista
lista_estudiantes.clear()

