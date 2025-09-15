import tkinter as tk
from tkinter import messagebox, simpledialog
from tkinter import ttk  # Para tablas más avanzadas
import json
import os
import unicodedata

#  CLASES
class Libro:
    def __init__(self, titulo, autor, categoria, isbn):
        self.titulo_autor = (titulo, autor)
        self.categoria = categoria
        self.isbn = isbn

    def __str__(self):
        return f"'{self.titulo_autor[0]}' por {self.titulo_autor[1]} - Categoría: {self.categoria} - ISBN: {self.isbn}"

    def to_dict(self):
        return {"titulo": self.titulo_autor[0],
                "autor": self.titulo_autor[1],
                "categoria": self.categoria,
                "isbn": self.isbn}

    @staticmethod
    def from_dict(data):
        return Libro(data["titulo"], data["autor"], data["categoria"], data["isbn"])

class Usuario:
    def __init__(self, nombre, id_usuario):
        self.nombre = nombre
        self.id_usuario = id_usuario
        self.libros_prestados = []

    def __str__(self):
        return f"Usuario: {self.nombre}, ID: {self.id_usuario}"

    def to_dict(self):
        return {"nombre": self.nombre,
                "id_usuario": self.id_usuario,
                "libros_prestados": [libro.to_dict() for libro in self.libros_prestados]}

    @staticmethod
    def from_dict(data):
        usuario = Usuario(data["nombre"], data["id_usuario"])
        usuario.libros_prestados = [Libro.from_dict(lib) for lib in data.get("libros_prestados", [])]
        return usuario

class Biblioteca:
    def __init__(self, archivo_libros="libros.json", archivo_usuarios="usuarios.json"):
        self.archivo_libros = archivo_libros
        self.archivo_usuarios = archivo_usuarios
        self.libros = {}
        self.usuarios_ids = set()
        self.usuarios = {}
        self.cargar_datos()

    # Guardado y carga
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

    # Funcionalidades básicas
    def añadir_libro(self, libro):
        if libro.isbn in self.libros:
            return False
        self.libros[libro.isbn] = libro
        self.guardar_datos()
        return True

    def listar_todos_libros(self):
        lista = []
        for libro in self.libros.values():
            lista.append([libro.titulo_autor[0], libro.titulo_autor[1], libro.categoria, libro.isbn, "Disponible"])
        for usuario in self.usuarios.values():
            for libro in usuario.libros_prestados:
                lista.append([libro.titulo_autor[0], libro.titulo_autor[1], libro.categoria, libro.isbn, f"Prestado por {usuario.nombre}"])
        return lista

# ----- INTERFAZ GRÁFICA -----
class BibliotecaGUI:
    def __init__(self, root):
        self.biblio = Biblioteca()
        self.root = root
        self.root.title("Sistema de Biblioteca GUI")
        self.root.geometry("700x500")

        # Etiqueta y campo de entrada
        tk.Label(root, text="Título del libro:").pack(pady=5)
        self.entry_titulo = tk.Entry(root, width=50)
        self.entry_titulo.pack(pady=5)

        tk.Label(root, text="Autor:").pack(pady=5)
        self.entry_autor = tk.Entry(root, width=50)
        self.entry_autor.pack(pady=5)

        tk.Label(root, text="Categoría:").pack(pady=5)
        self.entry_categoria = tk.Entry(root, width=50)
        self.entry_categoria.pack(pady=5)

        tk.Label(root, text="ISBN:").pack(pady=5)
        self.entry_isbn = tk.Entry(root, width=50)
        self.entry_isbn.pack(pady=5)

        # Botones
        tk.Button(root, text="Agregar libro", command=self.agregar_libro).pack(pady=5)
        tk.Button(root, text="Limpiar campos", command=self.limpiar_campos).pack(pady=5)
        tk.Button(root, text="Actualizar lista de libros", command=self.actualizar_tabla).pack(pady=5)

        # Tabla para mostrar libros
        self.tabla = ttk.Treeview(root, columns=("Titulo", "Autor", "Categoria", "ISBN", "Estado"), show="headings")
        for col in ("Titulo", "Autor", "Categoria", "ISBN", "Estado"):
            self.tabla.heading(col, text=col)
            self.tabla.column(col, width=130)
        self.tabla.pack(pady=10, fill="both", expand=True)
        self.actualizar_tabla()

    def agregar_libro(self):
        titulo = self.entry_titulo.get().strip()
        autor = self.entry_autor.get().strip()
        categoria = self.entry_categoria.get().strip()
        isbn = self.entry_isbn.get().strip()
        if not titulo or not autor or not categoria or not isbn:
            messagebox.showwarning("Advertencia", "Todos los campos son obligatorios.")
            return
        libro = Libro(titulo, autor, categoria, isbn)
        if self.biblio.añadir_libro(libro):
            messagebox.showinfo("Éxito", f"Libro '{titulo}' agregado correctamente.")
            self.actualizar_tabla()
            self.limpiar_campos()
        else:
            messagebox.showerror("Error", "El ISBN ya existe.")

    def limpiar_campos(self):
        self.entry_titulo.delete(0, tk.END)
        self.entry_autor.delete(0, tk.END)
        self.entry_categoria.delete(0, tk.END)
        self.entry_isbn.delete(0, tk.END)

    def actualizar_tabla(self):
        for fila in self.tabla.get_children():
            self.tabla.delete(fila)
        for libro in self.biblio.listar_todos_libros():
            self.tabla.insert("", tk.END, values=libro)

# ----- EJECUCIÓN -----
if __name__ == "__main__":
    root = tk.Tk()
    app = BibliotecaGUI(root)
    root.mainloop()
