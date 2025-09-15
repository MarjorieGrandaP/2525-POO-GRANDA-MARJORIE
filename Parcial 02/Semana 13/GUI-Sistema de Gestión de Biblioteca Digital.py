import json
import os
import unicodedata  # Para normalizar texto y eliminar tildes en las búsquedas


# CLASES

class Libro:
    """Representa un libro en la biblioteca"""
    def __init__(self, titulo, autor, categoria, isbn):
        # Los atributos título y autor se guardan como tupla porque son inmutables
        self.titulo_autor = (titulo, autor)
        self.categoria = categoria
        self.isbn = isbn # ISBN único que identifica al libro

    def __str__(self):
        # Representación legible del libro
        return f"'{self.titulo_autor[0]}' por {self.titulo_autor[1]} - Categoría: {self.categoria} - ISBN: {self.isbn}"

    def to_dict(self):
        # Convierte el objeto Libro a un diccionario para guardarlo en JSON
        return {
            "titulo": self.titulo_autor[0],
            "autor": self.titulo_autor[1],
            "categoria": self.categoria,
            "isbn": self.isbn
        }

    @staticmethod
    def from_dict(data):
        # Crea un objeto Libro a partir de un diccionario (al cargar datos JSON)
        return Libro(data["titulo"], data["autor"], data["categoria"], data["isbn"])


class Usuario:
    """Representa un usuario de la biblioteca"""
    def __init__(self, nombre, id_usuario):
        self.nombre = nombre
        self.id_usuario = id_usuario # ID único
        self.libros_prestados = [] # Lista de libros actualmente prestados

    def __str__(self):
        return f"Usuario: {self.nombre}, ID: {self.id_usuario}"

    def to_dict(self):
        # Convierte el objeto Usuario a diccionario, incluyendo libros prestados
        return {
            "nombre": self.nombre,
            "id_usuario": self.id_usuario,
            "libros_prestados": [libro.to_dict() for libro in self.libros_prestados]
        }

    @staticmethod
    def from_dict(data):
        # Crea un objeto Usuario a partir de un diccionario
        usuario = Usuario(data["nombre"], data["id_usuario"])
        usuario.libros_prestados = [Libro.from_dict(lib) for lib in data.get("libros_prestados", [])]
        return usuario

# CLASE BIBLIOTECA

class Biblioteca:
    def __init__(self, archivo_libros="libros.json", archivo_usuarios="usuarios.json"):
        # Archivos JSON para persistir datos
        self.archivo_libros = archivo_libros
        self.archivo_usuarios = archivo_usuarios
        self.libros = {}          # Diccionario ISBN -> Libro
        self.usuarios_ids = set() # Conjunto de IDs únicos
        self.usuarios = {}        # Diccionario ID -> Usuario
        self.cargar_datos() # Carga la información guardada en JSON al iniciar


    # GUARDADO Y CARGA

    def guardar_datos(self):
        with open(self.archivo_libros, "w", encoding="utf-8") as f:
            json.dump({isbn: libro.to_dict() for isbn, libro in self.libros.items()}, f, indent=4)
        with open(self.archivo_usuarios, "w", encoding="utf-8") as f:
            json.dump({uid: user.to_dict() for uid, user in self.usuarios.items()}, f, indent=4)

    def cargar_datos(self):
        if os.path.exists(self.archivo_libros):
            with open(self.archivo_libros, "r", encoding="utf-8") as f:
                libros_json = json.load(f)
                for isbn, lib_data in libros_json.items():
                    self.libros[isbn] = Libro.from_dict(lib_data)
        if os.path.exists(self.archivo_usuarios):
            with open(self.archivo_usuarios, "r", encoding="utf-8") as f:
                usuarios_json = json.load(f)
                for uid, user_data in usuarios_json.items():
                    usuario = Usuario.from_dict(user_data)
                    self.usuarios[uid] = usuario
                    self.usuarios_ids.add(uid)


    # FUNCIONALIDADES

    def añadir_libro(self, libro):
        if libro.isbn in self.libros:
            print("⚠ El libro ya existe en la biblioteca (mismo ISBN).")
        else:
            self.libros[libro.isbn] = libro
            print(f"Libro añadido: {libro}")
            self.guardar_datos()

    def quitar_libro(self, isbn):
        if isbn in self.libros:
            print(f"Libro eliminado: {self.libros[isbn]}")
            del self.libros[isbn]
            self.guardar_datos()
        else:
            print("No se encontró el libro con ese ISBN.")

    def registrar_usuario(self, usuario):
        if usuario.id_usuario in self.usuarios_ids:
            print("⚠ El ID de usuario ya existe.")
        else:
            self.usuarios_ids.add(usuario.id_usuario)
            self.usuarios[usuario.id_usuario] = usuario
            print(f"Usuario registrado: {usuario}")
            self.guardar_datos()

    def dar_baja_usuario(self, id_usuario):
        if id_usuario in self.usuarios_ids:
            print(f"Usuario dado de baja: {self.usuarios[id_usuario]}")
            self.usuarios_ids.remove(id_usuario)
            del self.usuarios[id_usuario]
            self.guardar_datos()
        else:
            print("No se encontró el usuario.")

    def prestar_libro(self, isbn, id_usuario):
        if isbn not in self.libros:
            print("El libro no existe.")
            return
        if id_usuario not in self.usuarios_ids:
            print("El usuario no está registrado.")
            return
        libro = self.libros[isbn]
        usuario = self.usuarios[id_usuario]
        usuario.libros_prestados.append(libro) # Se añade a la lista de libros prestados del usuario
        del self.libros[isbn] # Se quita del catálogo disponible
        print(f"Libro prestado: {libro} a {usuario}")
        self.guardar_datos()

    def devolver_libro(self, isbn, id_usuario):
        if id_usuario not in self.usuarios_ids:
            print("El usuario no está registrado.")
            return
        usuario = self.usuarios[id_usuario]
        for libro in usuario.libros_prestados:
            if libro.isbn == isbn:
                usuario.libros_prestados.remove(libro)
                self.libros[isbn] = libro
                print(f"Libro devuelto: {libro} por {usuario}")
                self.guardar_datos()
                return
        print("El usuario no tiene ese libro prestado.")


    # BÚSQUEDA FLEXIBLE

    def buscar_libros(self, criterio, valor):
        """Busca libros por título, autor, categoría o ISBN ignorando mayúsculas, minúsculas y tildes."""
        def normalizar(texto):
            texto = texto.lower()
            return ''.join(c for c in unicodedata.normalize('NFD', texto) if unicodedata.category(c) != 'Mn')

        valor_norm = normalizar(valor)
        resultados = []

        if criterio == "isbn":
            if valor in self.libros:
                resultados.append(self.libros[valor])
        else:
            for libro in self.libros.values():
                if criterio == "titulo" and valor_norm in normalizar(libro.titulo_autor[0]):
                    resultados.append(libro)
                elif criterio == "autor" and valor_norm in normalizar(libro.titulo_autor[1]):
                    resultados.append(libro)
                elif criterio == "categoria" and valor_norm == normalizar(libro.categoria):
                    resultados.append(libro)

        if resultados:
            print("Resultados de la búsqueda:")
            for libro in resultados:
                print(libro)
        else:
            print("No se encontraron libros que coincidan con la búsqueda.")


    # LISTAR LIBROS PRESTADOS DE UN USUARIO

    def listar_libros_prestados(self, id_usuario):
        if id_usuario not in self.usuarios_ids:
            print("El usuario no está registrado.")
            return
        usuario = self.usuarios[id_usuario]
        if usuario.libros_prestados:
            print(f"Libros prestados por {usuario.nombre}:")
            for libro in usuario.libros_prestados:
                print(libro)
        else:
            print(f"{usuario.nombre} no tiene libros prestados.")


    # LISTAR TODOS LOS LIBROS CON ESTADO: disponible/prestado

    def listar_todos_libros(self):
        """Muestra todos los libros con estado: Disponible o Prestado"""
        if not self.libros and not any(u.libros_prestados for u in self.usuarios.values()):
            print("No hay libros en la biblioteca.")
            return

        print("=== Lista completa de libros ===")
        # Libros disponibles
        for libro in self.libros.values():
            print(f"{libro} - Estado: Disponible")
        # Libros prestados
        for usuario in self.usuarios.values():
            for libro in usuario.libros_prestados:
                print(f"{libro} - Estado: Prestado por {usuario.nombre} (ID: {usuario.id_usuario})")



# MENÚ INTERACTIVO

def menu():
    biblioteca = Biblioteca()

    while True:
        print("\n====== MENÚ DE LA BIBLIOTECA ======")
        print("1. Añadir libro")
        print("2. Quitar libro")
        print("3. Registrar usuario")
        print("4. Dar de baja usuario")
        print("5. Prestar libro")
        print("6. Devolver libro")
        print("7. Buscar libro")
        print("8. Listar libros prestados de un usuario")
        print("9. Salir")
        print("10. Ver todos los libros con su estado")
        opcion = input("Selecciona una opción: ")

        if opcion == "1":             # Crear y añadir libro
            titulo = input("Título del libro: ")
            autor = input("Autor: ")
            categoria = input("Categoría: ")
            isbn = input("ISBN: ")
            libro = Libro(titulo, autor, categoria, isbn)
            biblioteca.añadir_libro(libro)

        elif opcion == "2":
            isbn = input("ISBN del libro a quitar: ")
            biblioteca.quitar_libro(isbn)

        elif opcion == "3":
            nombre = input("Nombre del usuario: ")
            id_usuario = input("ID de usuario: ")
            usuario = Usuario(nombre, id_usuario)
            biblioteca.registrar_usuario(usuario)

        elif opcion == "4":
            id_usuario = input("ID del usuario a dar de baja: ")
            biblioteca.dar_baja_usuario(id_usuario)

        elif opcion == "5":
            isbn = input("ISBN del libro a prestar: ")
            id_usuario = input("ID del usuario: ")
            biblioteca.prestar_libro(isbn, id_usuario)

        elif opcion == "6":
            isbn = input("ISBN del libro a devolver: ")
            id_usuario = input("ID del usuario: ")
            biblioteca.devolver_libro(isbn, id_usuario)

        elif opcion == "7":# Explicación clara del criterio de búsqueda
            print("Buscar por: titulo (nombre del libro), autor, categoria, isbn (identificador único)")
            criterio = input("Criterio de búsqueda: ").lower()
            valor = input("Valor a buscar: ")
            biblioteca.buscar_libros(criterio, valor)

        elif opcion == "8":
            id_usuario = input("ID del usuario: ")
            biblioteca.listar_libros_prestados(id_usuario)

        elif opcion == "10":
            biblioteca.listar_todos_libros()

        elif opcion == "9":
            print("Saliendo del sistema...")
            break

        else:
            print("Opción inválida, intenta nuevamente.")


if __name__ == "__main__":
    menu()
10