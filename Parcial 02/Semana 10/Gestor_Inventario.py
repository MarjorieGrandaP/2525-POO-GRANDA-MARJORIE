import json  # Importa el módulo para manejar archivos JSON (lectura y escritura de datos estructurados)
import os    # Importa el módulo para interactuar con el sistema de archivos (existencia de archivos, permisos, etc.)

# Clase Producto: representa un producto individual del inventario
class Producto:
    def __init__(self, id_producto, nombre, cantidad, precio):
        # Constructor que inicializa un producto con ID, nombre, cantidad y precio
        self.id = id_producto
        self.nombre = nombre
        self.cantidad = cantidad
        self.precio = precio

    def to_dict(self):
        """
        Convierte un objeto Producto a un diccionario.
        Esto es útil para guardar el producto en un archivo JSON.
        """
        return {
            "id": self.id,
            "nombre": self.nombre,
            "cantidad": self.cantidad,
            "precio": self.precio
        }

    @staticmethod
    def from_dict(data):
        """
        Crea un objeto Producto a partir de un diccionario.
        Esto permite reconstruir un producto que se leyó desde JSON.
        """
        return Producto(data['id'], data['nombre'], data['cantidad'], data['precio'])

    def __str__(self):
        # Representación legible del producto al imprimirlo
        return f"ID: {self.id}, Nombre: {self.nombre}, Cantidad: {self.cantidad}, Precio: ${self.precio:.2f}"


# Clase Inventario: maneja un conjunto de productos
class Inventario:
    def __init__(self, archivo_json="inventario.json"):
        # Inicializa el inventario con un archivo JSON opcional
        self.archivo_json = archivo_json
        self.productos = {}  # Diccionario con id_producto como clave y Producto como valor
        self.cargar_inventario()  # Carga los productos existentes del archivo al iniciar

    def cargar_inventario(self):
        """
        Carga los productos desde el archivo JSON.
        Si el archivo no existe, inicia un inventario vacío.
        Maneja errores como archivo corrupto o problemas de permisos.
        """
        if not os.path.exists(self.archivo_json):
            self.productos = {}
            return

        try:
            with open(self.archivo_json, "r") as f:
                # Lee el archivo JSON y convierte cada producto en un objeto Producto
                data = json.load(f)
                self.productos = {pid: Producto.from_dict(prod) for pid, prod in data.items()}
        except json.JSONDecodeError:
            print("Error: El archivo de inventario está corrupto. Se inicializa inventario vacío.")
            self.productos = {}
        except PermissionError:
            print("Error: No tiene permisos para leer el archivo de inventario.")
            self.productos = {}
        except Exception as e:
            print(f"Error inesperado al cargar inventario: {e}")
            self.productos = {}

    def guardar_inventario(self):
        """
        Guarda los productos en el archivo JSON.
        Maneja errores de permisos o cualquier error inesperado.
        """
        try:
            with open(self.archivo_json, "w") as f:
                json.dump({pid: prod.to_dict() for pid, prod in self.productos.items()}, f, indent=4)
        except PermissionError:
            print("Error: No tiene permisos para escribir en el archivo de inventario.")
        except Exception as e:
            print(f"Error inesperado al guardar inventario: {e}")

    def añadir_nuevo_producto(self, producto):
        """
        Agrega un nuevo producto al inventario.
        Si el producto ya existe, muestra un error.
        Guarda automáticamente los cambios en el archivo JSON.
        """
        if producto.id in self.productos:
            print("Error: El producto ya existe.")
            return
        self.productos[producto.id] = producto
        self.guardar_inventario()
        print("Producto agregado correctamente y guardado en el archivo.")

    def eliminar_producto(self, id_producto):
        """
        Elimina un producto del inventario por su ID.
        Si no existe, muestra un mensaje de error.
        Guarda automáticamente los cambios en el archivo JSON.
        """
        if id_producto in self.productos:
            del self.productos[id_producto]
            self.guardar_inventario()
            print("Producto eliminado correctamente y cambios guardados en el archivo.")
        else:
            print("Producto no encontrado.")

    def actualizar_producto(self, id_producto, nueva_cantidad=None, nuevo_precio=None):
        """
        Actualiza la cantidad y/o precio de un producto.
        Si el producto no existe, muestra un mensaje de error.
        Guarda automáticamente los cambios en el archivo JSON.
        """
        if id_producto in self.productos:
            if nueva_cantidad is not None:
                self.productos[id_producto].cantidad = nueva_cantidad
            if nuevo_precio is not None:
                self.productos[id_producto].precio = nuevo_precio
            self.guardar_inventario()
            print("Producto actualizado correctamente y cambios guardados en el archivo.")
        else:
            print("Producto no encontrado.")

    def buscar_por_nombre(self, nombre):
        """
        Busca productos cuyo nombre contenga la cadena ingresada (no distingue mayúsculas/minúsculas).
        Devuelve una lista de productos coincidentes.
        """
        return [p for p in self.productos.values() if nombre.lower() in p.nombre.lower()]

    def mostrar_productos(self):
        """
        Muestra todos los productos del inventario en consola.
        Si el inventario está vacío, indica que no hay productos.
        """
        if not self.productos:
            print("El inventario está vacío.")
            return
        for p in self.productos.values():
            print(p)


# Menú interactivo: permite al usuario gestionar el inventario desde consola
def menu():
    inventario = Inventario()  # Crea un inventario al iniciar

    while True:
        # Muestra las opciones del menú
        print("\nBienvenido al inventario de tu tienda")
        print("1. Agregar nuevo producto")
        print("2. Eliminar producto")
        print("3. Actualizar producto")
        print("4. Buscar producto por nombre")
        print("5. Mostrar todos los productos")
        print("6. Salir del menú")

        opcion = input("Ingrese la opción: ")

        if opcion == "1":
            # Agregar un nuevo producto solicitando datos al usuario
            id_p = input("Ingrese ID del producto: ")
            nombre = input("Ingrese nombre: ")
            try:
                cantidad = int(input("Ingrese cantidad: "))
                precio = float(input("Ingrese precio: "))
            except ValueError:
                print("Error: Debe ingresar un número válido para cantidad y precio.")
                continue
            inventario.añadir_nuevo_producto(Producto(id_p, nombre, cantidad, precio))

        elif opcion == "2":
            # Eliminar un producto por ID
            id_p = input("Ingrese ID del producto a eliminar: ")
            inventario.eliminar_producto(id_p)

        elif opcion == "3":
            # Actualizar cantidad o precio de un producto existente
            id_p = input("Ingrese ID del producto a actualizar: ")
            cantidad = input("Nueva cantidad (deje vacío si no cambia): ")
            precio = input("Nuevo precio (deje vacío si no cambia): ")
            try:
                nueva_cantidad = int(cantidad) if cantidad else None
                nuevo_precio = float(precio) if precio else None
            except ValueError:
                print("Error: Debe ingresar un número válido para cantidad o precio.")
                continue
            inventario.actualizar_producto(id_p, nueva_cantidad, nuevo_precio)

        elif opcion == "4":
            # Buscar productos por nombre o parte del nombre
            nombre = input("Ingrese nombre o parte del nombre: ")
            resultados = inventario.buscar_por_nombre(nombre)
            if resultados:
                print("Resultados encontrados:")
                for r in resultados:
                    print(r)
            else:
                print("No se encontraron productos.")

        elif opcion == "5":
            # Mostrar todos los productos
            inventario.mostrar_productos()

        elif opcion == "6":
            # Salir del menú
            print("Saliendo del sistema. ¡Hasta pronto!")
            break

        else:
            # Opción no válida
            print("Opción no válida. Intente de nuevo.")


# Ejecuta el menú si se corre este script directamente
if __name__ == "__main__":
    menu()

