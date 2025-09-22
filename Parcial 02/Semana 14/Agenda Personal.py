# Importamos las librerías necesarias
import tkinter as tk #es la libreria que permite crear la interfaz gráfica de usuario
from tkinter import ttk #ttk contiene widgets más avanzados como Treeview
from tkinter import messagebox #permite mostrar diálogos de confirmación o alertas.
import json #permite guardar y cargar los eventos desde un archivo, sin que se borren cuando se cierra el programa
from datetime import datetime, date #permite manejar fechas y horas correctamente.
from tkcalendar import DateEntry  # pip install tkcalendar

# Creación de la ventana principal
root = tk.Tk() #Tk() crea la ventana principal de la aplicación.
root.title("🗓 Agenda Personal") #title() define el título de la ventana.
root.state("zoomed")  # maximiza la ventana automáticamente


#FRAMES PRINCIPALS
# Frame para la lista de eventos
frame_lista = tk.Frame(root)
frame_lista.pack(pady=10, fill="both", expand=True)

# Frame para los campos de entrada
frame_entrada = tk.Frame(root)
frame_entrada.pack(pady=10)

# Frame para los botones
frame_botones = tk.Frame(root)
frame_botones.pack(pady=10)

#TREEVIEW CON SCROLLBARS
# Crear TreeView con columnas para Fecha, Hora y Descripción
tree = ttk.Treeview(frame_lista, columns=("fecha", "hora", "descripcion"), show="headings")
#Treeview permite mostrar tablas con varias columnas.
#show="headings" oculta la columna de índice predeterminada.
tree.heading("fecha", text="Fecha") #heading() define el nombre que se mostrará en cada columna.
tree.heading("hora", text="Hora")
tree.heading("descripcion", text="Actividades")

# Ajustar el tamaño de las columnas
tree.column("fecha", width=120, anchor="center") #column() define el ancho de cada columna.
tree.column("hora", width=80, anchor="center")
tree.column("descripcion", width=450, anchor="w")

# Scroll vertical y horizontal
scroll_v = ttk.Scrollbar(frame_lista, orient="vertical", command=tree.yview)
scroll_h = ttk.Scrollbar(frame_lista, orient="horizontal", command=tree.xview)
tree.configure(yscrollcommand=scroll_v.set, xscrollcommand=scroll_h.set)
scroll_v.pack(side="right", fill="y")
scroll_h.pack(side="bottom", fill="x")
tree.pack(fill="both", expand=True)

# Filas alternadas
tree.tag_configure("evenrow", background="#E0F7FA")
tree.tag_configure("oddrow", background="#F1F8E9")

#ENTRADAS Y ETIQUETAS
# Etiquetas
#Label muestra texto descriptivo para cada campo.
fuente_label = ("Helvetica", 11)
tk.Label(frame_entrada, text="Fecha:", font=fuente_label).grid(row=0, column=0, padx=5, pady=5, sticky="e")
tk.Label(frame_entrada, text="Hora (HH:MM):", font=fuente_label).grid(row=1, column=0, padx=5, pady=5, sticky="e")
tk.Label(frame_entrada, text="Descripción:", font=fuente_label).grid(row=2, column=0, padx=5, pady=5, sticky="e")


#ENTRADA PARA LA FECHA, HORA Y ACTIVIDADES
# Entradas
#Entry permite al usuario ingresar texto.
entry_fecha = DateEntry(frame_entrada, date_pattern='dd/mm/yyyy', mindate=date.today(), font=("Helvetica",11))
#padx y pady agregan márgenes internos.
entry_fecha.grid(row=0, column=1, padx=5, pady=5)

entry_hora = tk.Entry(frame_entrada, font=("Helvetica", 11))
entry_hora.grid(row=1, column=1, padx=5, pady=5)

entry_descripcion = tk.Text(frame_entrada, width=40, height=5, font=("Helvetica", 11))
entry_descripcion.grid(row=2, column=1, padx=5, pady=5)


#FUNCIONES PRINCIPALES
     #FUNCIONAMIENTO DE LOS BOTONES
# Archivo JSON donde se guardarán los eventos
ARCHIVO_EVENTOS = "eventos.json"

def validar_hora(hora):
    try:
        datetime.strptime(hora, "%H:%M")
        return True
    except ValueError:
        return False

def insertar_fila(evento):
    fila = tree.insert("", "end", values=(evento["fecha"], evento["hora"], evento["descripcion"]))
    # Alternar color
    if len(tree.get_children()) % 2 == 0:
        tree.item(fila, tags=("evenrow",))
    else:
        tree.item(fila, tags=("oddrow",))


# Función para cargar eventos desde JSON al TreeView
def cargar_eventos(): #cargar_eventos() lee los eventos guardados y los muestra en el TreeView al iniciar.
    try:
        with open(ARCHIVO_EVENTOS, "r") as archivo:
            eventos = json.load(archivo)
            for evento in eventos:
                insertar_fila(evento)
    except FileNotFoundError:
        # Si no existe el archivo, no hacemos nada
        pass

# Función para guardar todos los eventos del TreeView al JSON
def guardar_eventos(): #guardar_eventos() guarda todos los eventos actuales del TreeView en el archivo JSON.
    eventos = []
    for item in tree.get_children():
        fecha, hora, descripcion = tree.item(item, "values")
        eventos.append({"fecha": fecha, "hora": hora, "descripcion": descripcion})
    with open(ARCHIVO_EVENTOS, "w") as archivo:
        json.dump(eventos, archivo, indent=4)

# Función para agregar un nuevo evento
def agregar_evento(): #agregar_evento() toma los datos de los campos de entrada y los agrega al TreeView y JSON.
    fecha = entry_fecha.get()
    hora = entry_hora.get()
    descripcion = entry_descripcion.get("1.0", tk.END).strip()

    if not fecha or not hora or not descripcion:
        messagebox.showwarning("Campos vacíos", "Por favor, complete todos los campos.")
        return

    if not validar_hora(hora):
        messagebox.showwarning("Hora inválida", "Ingrese la hora en formato HH:MM (00:00 a 23:59).")
        return

    evento = {"fecha": fecha, "hora": hora, "descripcion": descripcion}
    insertar_fila(evento)
    guardar_eventos()

    entry_hora.delete(0, tk.END)
    entry_descripcion.delete(0, tk.END)

# Función para eliminar el evento seleccionado
def eliminar_evento(): #eliminar un evento
    seleccionado = tree.selection()
    if not seleccionado:
        messagebox.showwarning("Selección vacía", "Seleccione un evento para eliminar.")
        return
    if messagebox.askyesno("Confirmar eliminación", "¿Está seguro de eliminar este evento?"):
        tree.delete(seleccionado)
        guardar_eventos()

# Función para salir de la aplicación
def salir(): #cierra la ventana de eventos
    root.destroy()

 #CARACTERISTICAS DE LOS BOTONES
    # Botones
fuente_botones = ("Helvetica", 11, "bold")

btn_agregar = tk.Button(frame_botones, text="🗓 Agregar Evento", command=agregar_evento,
                        bg="#A8D5BA", fg="black", width=18, font=fuente_botones)
btn_agregar.grid(row=0, column=0, padx=10, pady=5)

btn_eliminar = tk.Button(frame_botones, text="❌ Eliminar Evento", command=eliminar_evento,
                         bg="#F7C5CC", fg="black", width=18, font=fuente_botones)
btn_eliminar.grid(row=0, column=1, padx=10, pady=5)

btn_salir = tk.Button(frame_botones, text="🚪 Salir", command=salir,
                      bg="#FFE3A3", fg="black", width=18, font=fuente_botones)
btn_salir.grid(row=0, column=2, padx=10, pady=5)


#INICIAR LA APLICACION
# Cargar eventos existentes al iniciar
cargar_eventos()

# Ejecutar la ventana principal
root.mainloop()






