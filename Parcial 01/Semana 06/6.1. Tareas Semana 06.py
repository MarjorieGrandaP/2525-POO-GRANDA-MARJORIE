# Clase base: Libro
class Libro:
    def __init__(self, titulo, autor, isbn):
        # Atributos privados (encapsulación)
        self.__titulo = titulo
        self.__autor = autor
        self.__isbn = isbn

    # Métodos getters para acceder a los atributos encapsulados
    def obtener_titulo(self):
        return self.__titulo

    def obtener_autor(self):
        return self.__autor

    def obtener_isbn(self):
        return self.__isbn

    # Método para mostrar la información del libro
    def mostrar_info(self):
        print(f"Título: {self.__titulo}")
        print(f"Autor: {self.__autor}")
        print(f"ISBN: {self.__isbn}")

# Clase derivada: LibroPrestado hereda de Libro
class LibroPrestado(Libro):
    def __init__(self, titulo, autor, isbn, prestatario, fecha_devolucion):
        # Llama al constructor de la clase base
        super().__init__(titulo, autor, isbn)
        # Nuevos atributos de la clase derivada
        self.prestatario = prestatario
        self.fecha_devolucion = fecha_devolucion

    # Método sobrescrito (polimorfismo)
    def mostrar_info(self):
        # Muestra también la información base
        super().mostrar_info()
        print(f"Prestado a: {self.prestatario}")
        print(f"Fecha de devolución: {self.fecha_devolucion}")

# DEMOSTRACIÓN DEL CÓDIGO

# Creación de una instancia de Libro
libro1 = Libro("El principito", "George Orwell", "978-0451524935")

# Creación de una instancia de LibroPrestado
libro2 = LibroPrestado("Cien años de soledad", "Gabriel García Márquez", "978-0307474728", "Juan Pérez", "15/07/2025")

# Mostrar información del libro (uso de encapsulación y acceso por métodos)
print("=== Libro Disponible ===")
libro1.mostrar_info()

print("\n=== Libro Prestado ===")
# Mostrar información del libro prestado (uso de herencia y polimorfismo)
libro2.mostrar_info()

# Acceso individual a atributos encapsulados (sólo a través de métodos públicos)
print("\nAccediendo a la información sobre el título del primer libro de forma segura (encapsulación):")
print(libro1.obtener_titulo())
