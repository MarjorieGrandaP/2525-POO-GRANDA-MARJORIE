#El programa desarrollado mediante POO, es un Sistema Bibliotecario
# Clase que representa un libro
class Libro:
    def __init__(self, titulo, autor, isbn):
        self.titulo = titulo
        self.autor = autor
        self.isbn = isbn
        self.disponible = True  # True = disponible, False = prestado

    def __str__(self):
        estado = "Disponible" if self.disponible else "Prestado"
        return f"{self.titulo} de {self.autor} (ISBN: {self.isbn}) - {estado}"


# Clase que representa a un usuario
class Usuario:
    def __init__(self, nombre, id_usuario):
        self.nombre = nombre
        self.id_usuario = id_usuario
        self.libros_prestados = []

    def agregar_libro(self, libro):
        self.libros_prestados.append(libro)

    def quitar_libro(self, libro):
        if libro in self.libros_prestados:
            self.libros_prestados.remove(libro)

    def listar_libros(self):
        if not self.libros_prestados:
            print(f"{self.nombre} no tiene libros prestados.")
        else:
            print(f"Libros que han sido pedidos prestados por {self.nombre}:")
            for libro in self.libros_prestados:
                print(f"  - {libro.titulo}")


# Clase que representa a la bibliotecaria
class Bibliotecaria:
    def __init__(self, nombre):
        self.nombre = nombre

    def prestar_libro(self, libro, usuario):
        print(f"\n Bibliotecaria {self.nombre} gestionando préstamo...")
        if libro.disponible:
            libro.disponible = False
            usuario.agregar_libro(libro)
            print(f"{usuario.nombre} ha pedido prestado '{libro.titulo}' correctamente.")
        else:
            print(f"El libro '{libro.titulo}' no está disponible actualmente.")

    def recibir_devolucion(self, libro, usuario):
        print(f"\n Bibliotecaria {self.nombre} gestionando devolución...")
        if libro in usuario.libros_prestados:
            libro.disponible = True
            usuario.quitar_libro(libro)
            print(f"{usuario.nombre} ha devuelto el libro '{libro.titulo}'.")
        else:
            print(f"{usuario.nombre} no tiene prestado el libro '{libro.titulo}'.")

    def mostrar_catalogo(self, biblioteca):
        print(f"\n Catálogo de la biblioteca '{biblioteca.nombre}':")
        for libro in biblioteca.catalogo:
            print("  -", libro)


# Clase Biblioteca (gestiona catálogo y usuarios)
class Biblioteca:
    def __init__(self, nombre):
        self.nombre = nombre
        self.catalogo = []
        self.usuarios = []

    def agregar_libro(self, libro):
        self.catalogo.append(libro)

    def registrar_usuario(self, usuario):
        self.usuarios.append(usuario)

    def buscar_libro(self, titulo):
        for libro in self.catalogo:
            if libro.titulo.lower() == titulo.lower():
                return libro
        return None


#  Ejemplo de uso del sistema

# Crear biblioteca
biblioteca = Biblioteca("Biblioteca Municipal")

# Crear libros
libro1 = Libro("El Alquimista", "Paulo Coelho", "001")
libro2 = Libro("Rayuela", "Julio Cortázar", "002")
libro3 = Libro("Orgullo y Prejuicio", "Jane Austen", "003")

# Agregar libros
biblioteca.agregar_libro(libro1)
biblioteca.agregar_libro(libro2)
biblioteca.agregar_libro(libro3)

# Crear usuarios
usuario1 = Usuario("Camila", "U100")
usuario2 = Usuario("Jorge", "U101")

# Registrar usuarios
biblioteca.registrar_usuario(usuario1)
biblioteca.registrar_usuario(usuario2)

# Crear bibliotecaria
bibliotecaria = Bibliotecaria("María")

# Mostrar catálogo inicial
bibliotecaria.mostrar_catalogo(biblioteca)

# Préstamos
bibliotecaria.prestar_libro(libro1, usuario1)
bibliotecaria.prestar_libro(libro2, usuario2)

# Intento de préstamo de libro ya prestado
bibliotecaria.prestar_libro(libro1, usuario2)

# Devolución
bibliotecaria.recibir_devolucion(libro1, usuario1)

# Usuario 2 lo presta después de devolución
bibliotecaria.prestar_libro(libro1, usuario2)

# Listar libros prestados
usuario1.listar_libros()
usuario2.listar_libros()

# Mostrar catálogo actualizado
bibliotecaria.mostrar_catalogo(biblioteca)
