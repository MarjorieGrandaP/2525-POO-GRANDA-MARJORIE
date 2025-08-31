import json           # 📄 Para leer y escribir archivos JSON
import os             # 📁 Para verificar existencia de archivos, permisos, etc.
from datetime import datetime  # 🕒 Para registrar fecha y hora de creación de productos

# 🎯 Clase Producto: representa un producto individual del inventario
class Producto:
    def __init__(self, id_producto, nombre, cantidad, precio, fecha=None):
        """
        Constructor de la clase Producto.
        Parámetros:
            - id_producto: str -> Identificador único del producto
            - nombre: str -> Nombre del producto
            - cantidad: int -> Cantidad disponible en inventario
            - precio: float -> Precio unitario del producto
            - fecha: str -> Fecha de creación/modificación (opcional)
        """
        self.id = id_producto
        self.nombre = nombre
        self.cantidad = cantidad
        self.precio = precio
        self.fecha = fecha or datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Fecha actual si no se proporciona

    def to_dict(self):
        """
        Convierte el objeto Producto a un diccionario.
        Esto permite guardarlo fácilmente en un archivo JSON.
        """
        return {
            "id": self.id,
            "nombre": self.nombre,
            "cantidad": self.cantidad,
            "precio": self.precio,
            "fecha": self.fecha
        }

    @staticmethod
    def from_dict(data):
        """
        Crea un objeto Producto a partir de un diccionario.
        Se utiliza al cargar desde el archivo JSON.
        """
        return Producto(
            data['id'],
            data['nombre'],
            data['cantidad'],
            data['precio'],
            data.get('fecha')  # Usa .get() por si el campo no existe en archivos antiguos
        )

    def __str__(self):
        """
        Representación en texto legible del producto.
        Se usa al imprimir por consola.
        """
        return f"🆔 {self.id} | 🛒 {self.nombre} | 📦 {self.cantidad} uds | 💲${self.precio:.2f} | 📅 {self.fecha}"


# 🧠 Clase Inventario: gestiona todos los productos usando un diccionario
class Inventario:
    def __init__(self, archivo_json="inventario.json"):
        """
        Constructor de la clase Inventario.
        Carga los datos desde el archivo JSON si existe.
        """
        self.archivo_json = archivo_json
        self.productos = {}  # Diccionario con ID como clave y Producto como valor
        self.cargar_inventario()

    def cargar_inventario(self):
        """
        Carga los productos desde el archivo JSON al diccionario `self.productos`.
        Si el archivo no existe o está corrupto, se crea un inventario vacío.
        """
        if not os.path.exists(self.archivo_json):
            self.productos = {}
            return

        try:
            with open(self.archivo_json, "r") as f:
                data = json.load(f)  # Diccionario leído desde el JSON
                self.productos = {
                    pid: Producto.from_dict(prod) for pid, prod in data.items()
                }
        except json.JSONDecodeError:
            print("⚠️ Error: El archivo está corrupto. Inventario vacío.")
            self.productos = {}
        except PermissionError:
            print("⛔ Error: No tienes permisos para leer el archivo.")
            self.productos = {}
        except Exception as e:
            print(f"❗ Error inesperado: {e}")
            self.productos = {}

    def guardar_inventario(self):
        """
        Guarda todos los productos actuales en el archivo JSON.
        Convierte cada objeto Producto en un diccionario antes de guardar.
        """
        try:
            with open(self.archivo_json, "w") as f:
                json.dump({pid: prod.to_dict() for pid, prod in self.productos.items()}, f, indent=4)
        except PermissionError:
            print("⛔ Error: No tienes permisos para escribir en el archivo.")
        except Exception as e:
            print(f"❗ Error inesperado al guardar: {e}")

    def añadir_nuevo_producto(self, producto):
        """
        Agrega un nuevo producto al inventario.
        Si el ID ya existe, permite aumentar la cantidad existente.
        """
        if producto.id in self.productos:
            print(f"⚠️ Producto con ID {producto.id} ya existe.")
            try:
                extra = int(input("🔁 Ingrese cantidad adicional o 0 para cancelar: "))
                if extra > 0:
                    self.productos[producto.id].cantidad += extra
                    self.guardar_inventario()
                    print("✅ Cantidad actualizada correctamente.")
                else:
                    print("🚫 Operación cancelada.")
            except ValueError:
                print("❌ Entrada inválida.")
        else:
            self.productos[producto.id] = producto
            self.guardar_inventario()
            print("✅ Producto agregado correctamente.")

    def eliminar_producto(self, id_producto):
        """
        Elimina un producto del inventario por su ID.
        """
        if id_producto in self.productos:
            del self.productos[id_producto]
            self.guardar_inventario()
            print("🗑️ Producto eliminado correctamente.")
        else:
            print("❌ Producto no encontrado.")

    def actualizar_producto(self, id_producto, nueva_cantidad=None, nuevo_precio=None):
        """
        Actualiza la cantidad y/o precio de un producto existente.
        """
        if id_producto in self.productos:
            if nueva_cantidad is not None:
                self.productos[id_producto].cantidad = nueva_cantidad
            if nuevo_precio is not None:
                self.productos[id_producto].precio = nuevo_precio
            self.guardar_inventario()
            print("🔄 Producto actualizado correctamente.")
        else:
            print("❌ Producto no encontrado.")

    def buscar_por_nombre(self, nombre):
        """
        Busca productos cuyo nombre contenga la cadena indicada.
        No distingue entre mayúsculas y minúsculas.
        """
        return [p for p in self.productos.values() if nombre.lower() in p.nombre.lower()]

    def mostrar_productos(self):
        """
        Muestra todos los productos del inventario en consola.
        """
        if not self.productos:
            print("📭 El inventario está vacío.")
            return
        print("📋 Listado de productos:\n" + "-"*40)
        for p in self.productos.values():
            print(p)


# 🧾 Menú de usuario: permite interactuar con el inventario
def menu():
    inventario = Inventario()  # Se crea el inventario y se carga automáticamente

    while True:
        # Menú principal
        print("\n📦📊 Bienvenido al Sistema de Gestión de Inventario 📊📦")
        print("1️⃣  Agregar nuevo producto")
        print("2️⃣  Eliminar producto")
        print("3️⃣  Actualizar producto")
        print("4️⃣  Buscar producto por nombre")
        print("5️⃣  Mostrar todos los productos")
        print("6️⃣  Salir")

        opcion = input("👉 Ingrese una opción: ")

        if opcion == "1":
            print("\n🆕 Agregar producto")
            id_p = input("🆔 ID del producto: ")
            nombre = input("🛒 Nombre: ")
            try:
                cantidad = int(input("📦 Cantidad: "))
                precio = float(input("💲 Precio: "))
            except ValueError:
                print("❌ Error: Valores inválidos.")
                continue
            inventario.añadir_nuevo_producto(Producto(id_p, nombre, cantidad, precio))

        elif opcion == "2":
            print("\n🗑️ Eliminar producto")
            id_p = input("🆔 Ingrese el ID: ")
            inventario.eliminar_producto(id_p)

        elif opcion == "3":
            print("\n🔄 Actualizar producto")
            id_p = input("🆔 ID del producto: ")
            cantidad = input("📦 Nueva cantidad (enter para omitir): ")
            precio = input("💲 Nuevo precio (enter para omitir): ")
            try:
                nueva_cantidad = int(cantidad) if cantidad else None
                nuevo_precio = float(precio) if precio else None
            except ValueError:
                print("❌ Error: Entrada inválida.")
                continue
            inventario.actualizar_producto(id_p, nueva_cantidad, nuevo_precio)

        elif opcion == "4":
            print("\n🔍 Buscar producto")
            nombre = input("🔤 Ingrese nombre o parte del nombre: ")
            resultados = inventario.buscar_por_nombre(nombre)
            if resultados:
                print("✅ Productos encontrados:\n")
                for r in resultados:
                    print(r)
            else:
                print("❌ No se encontraron coincidencias.")

        elif opcion == "5":
            print("\n📋 Todos los productos:")
            inventario.mostrar_productos()

        elif opcion == "6":
            print("👋 ¡Gracias por usar el sistema! Hasta luego.")
            break

        else:
            print("❗ Opción no válida. Intente nuevamente.")


# ▶️ Ejecuta el menú si se ejecuta este archivo directamente
if __name__ == "__main__":
    menu()
