# Creación de un Inventario
#Nota el presente inventario guarda la información en la Ram para que la información permanezca
#se debe crear en formato JSON
# Clase Producto
class Producto:
    def __init__(self, id_producto, nombre, cantidad, precio):
        """
        Constructor de la clase Producto
        """
        self.id = id_producto        # Identificador único del producto
        self.nombre = nombre         # Denominación del producto
        self.cantidad = cantidad     # Unidades disponibles
        self.precio = precio         # Valor de venta al público (PVP)

    def __str__(self):
        """
        Representación legible al imprimir un producto
        """
        return f"ID: {self.id}, Nombre: {self.nombre}, Cantidad: {self.cantidad}, Precio: ${self.precio:.2f}"

# Clase Inventario

class Inventario:
    def __init__(self):
        """
        Constructor de la clase Inventario
        Atributo: lista de productos
        """
        self.lista_productos = []

    def añadir_nuevo_producto(self, producto):
        """
        Añade un nuevo producto al inventario verificando que el ID no esté repetido
        """
        if any(p.id == producto.id for p in self.lista_productos):
            print("Error: El producto ya existe.")
            return
        self.lista_productos.append(producto)
        print("Producto agregado correctamente.")

    def eliminar_producto(self, id_producto):
        """
        Elimina un producto por su ID
        """
        for p in self.lista_productos:
            if p.id == id_producto:
                self.lista_productos.remove(p)
                print("Producto eliminado correctamente.")
                return
        print("Producto no encontrado.")

    def actualizar_producto(self, id_producto, nueva_cantidad=None, nuevo_precio=None):
        """
        Actualiza la cantidad o el precio de un producto
        """
        for p in self.lista_productos:
            if p.id == id_producto:
                if nueva_cantidad is not None:
                    p.cantidad = nueva_cantidad
                if nuevo_precio is not None:
                    p.precio = nuevo_precio
                print("Producto actualizado correctamente.")
                return
        print("Producto no encontrado.")

    def buscar_por_nombre(self, nombre):
        """
        Busca productos que contengan el texto en el nombre
        """
        return [p for p in self.lista_productos if nombre.lower() in p.nombre.lower()]

    def mostrar_productos(self):
        """
        Muestra todos los productos en el inventario
        """
        if not self.lista_productos:
            print("El inventario está vacío.")
            return
        for p in self.lista_productos:
            print(p)


# Interfaz de Usuario (Menú)
def menu():
    inventario = Inventario()

    while True:
        print("\n Bienvenido al inventario de tu tienda")
        print("¿Qué deseas hacer hoy?")
        print("1. Agregar nuevo producto")
        print("2. Eliminar producto")
        print("3. Actualizar producto")
        print("4. Buscar producto por nombre")
        print("5. Mostrar todos los productos")
        print("6. Salir del menú")

        opcion = input("\nEscriba la opción de la \nacción que desea realizar: ")

        if opcion == "1":
            # Agregar producto
            id_p = input("Ingrese ID del producto: ")
            nombre = input("Ingrese nombre: ")
            cantidad = int(input("Ingrese cantidad: "))
            precio = float(input("Ingrese precio: "))
            inventario.añadir_nuevo_producto(Producto(id_p, nombre, cantidad, precio))

        elif opcion == "2":
            # Eliminar producto
            id_p = input("Ingrese ID del producto a eliminar: ")
            inventario.eliminar_producto(id_p)

        elif opcion == "3":
            # Actualizar producto
            id_p = input("Ingrese ID del producto a actualizar: ")
            cantidad = input("Nueva cantidad (deje vacío si no cambia): ")
            precio = input("Nuevo precio (deje vacío si no cambia): ")
            nueva_cantidad = int(cantidad) if cantidad else None
            nuevo_precio = float(precio) if precio else None
            inventario.actualizar_producto(id_p, nueva_cantidad, nuevo_precio)

        elif opcion == "4":
            # Buscar producto
            nombre = input("Ingrese el nombre o parte del nombre: ")
            resultados = inventario.buscar_por_nombre(nombre)
            if resultados:
                print("Resultados encontrados:")
                for r in resultados:
                    print(r)
            else:
                print("No se encontraron productos.")

        elif opcion == "5":
            # Mostrar inventario
            inventario.mostrar_productos()

        elif opcion == "6":
            # Salir
            print("Saliendo del sistema. ¡Hasta pronto!")
            break

        else:
            print("Opción no válida. \n Elige entre las opciones mostradas.")



# Ejecución del programa
if __name__ == "__main__":
    menu()





