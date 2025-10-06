#Creación de una aplicación que permite crear una lista de taras
import tkinter as tk
from tkinter import messagebox, font
import json
import os

#  CONFIGURACIÓN PERSONALIZABLE
# Aquí definimos colores, fuentes y tamaños de botones para que se puedan cambiar fácilmente
CONFIG = {
    "fondo": "#e6e3a8",                 # Color de fondo de la ventana
    "color_texto": "#071447",           # Color del texto
    "color_botones": "#317182",         # Color normal de los botones
    "color_botones_hover": "#45a049",   # Color de los botones al pasar el mouse (hover)
    "fuente": ("OpenDyslexic", 12),            # Fuente por defecto para textos
    "fuente_botones": ("Arial", 11, "bold"),  # Fuente para los botones
    "alto_boton": 2,                    # Altura de los botones
    "ancho_boton": 18                   # Anchura de los botones
}

# Archivo JSON donde se guardan las tareas de manera persistente
ARCHIVO_TAREAS = "tareas.json"

# - TOOLTIP (mensajes emergentes)
# Clase que muestra un mensaje flotante al pasar el mouse sobre un widget
class Tooltip:
    def __init__(self, widget, texto):
        self.widget = widget
        self.texto = texto
        self.tooltip = None
        # Asociamos eventos al widget: cuando entra o sale el mouse
        widget.bind("<Enter>", self.mostrar)
        widget.bind("<Leave>", self.ocultar)

    def mostrar(self, event=None):
        # Calcula la posición del tooltip al lado del cursor
        x, y, _, _ = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 25
        # Se crea una ventana flotante sin bordes
        self.tooltip = tk.Toplevel(self.widget)
        self.tooltip.wm_overrideredirect(True)
        self.tooltip.wm_geometry(f"+{x}+{y}")
        # Texto del tooltip
        label = tk.Label(self.tooltip, text=self.texto, bg="yellow", relief="solid",
                         borderwidth=1, font=("Arial", 9))
        label.pack(ipadx=3)

    def ocultar(self, event=None):
        # Cierra el tooltip cuando se quita el mouse
        if self.tooltip:
            self.tooltip.destroy()
            self.tooltip = None

# APLICACIÓN PRINCIPAL
class GestorTareas:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestor de Tareas")
        self.root.configure(bg=CONFIG["fondo"])

        # Ajustamos el tamaño de la ventana a un porcentaje de la pantalla
        ancho = int(self.root.winfo_screenwidth() * 0.4)
        alto = int(self.root.winfo_screenheight() * 0.6)
        self.root.geometry(f"{ancho}x{alto}")

        # Texto introductorio para el usuario
        label_intro = tk.Label(
            self.root,
            text="Bienvenido/a al Gestor de Tareas.\n\nAquí podrás añadir, completar y eliminar tareas.\n"
                 "A continuación escribe una Tarea por completar 📌",
            bg=CONFIG["fondo"], fg=CONFIG["color_texto"], font=("Arial", 12), justify="center"
        )
        label_intro.pack(pady=10)

        # Entrada de texto para nuevas tareas
        self.entry = tk.Entry(self.root, width=40, font=CONFIG["fuente"])
        self.entry.pack(pady=10)
        # Al presionar ENTER se agrega la tarea
        self.entry.bind("<Return>", self.agregar_tarea)
        Tooltip(self.entry, "Escribe aquí la nueva tarea y presiona Enter o el botón Añadir.")

        # Frame donde se organizan los botones
        frame_botones = tk.Frame(self.root, bg=CONFIG["fondo"])
        frame_botones.pack(pady=5)

        # Botón: Añadir tarea
        self.btn_add = tk.Button(frame_botones, text="Añadir Tarea", command=self.agregar_tarea,
                                 bg=CONFIG["color_botones"], fg="white",
                                 font=CONFIG["fuente_botones"], width=CONFIG["ancho_boton"], height=CONFIG["alto_boton"])
        self.btn_add.grid(row=0, column=0, padx=5)
        Tooltip(self.btn_add, "Añade la tarea escrita en la caja de texto.")

        # Botón: Marcar como completada
        self.btn_done = tk.Button(frame_botones, text="Marcar como Completada", command=self.marcar_completada,
                                  bg=CONFIG["color_botones"], fg="white",
                                  font=CONFIG["fuente_botones"], width=CONFIG["ancho_boton"], height=CONFIG["alto_boton"])
        self.btn_done.grid(row=0, column=1, padx=5)
        Tooltip(self.btn_done, "Marca la tarea seleccionada como completada.")

        # Botón: Eliminar tarea
        self.btn_delete = tk.Button(frame_botones, text="Eliminar Tarea", command=self.eliminar_tarea,
                                    bg=CONFIG["color_botones"], fg="white",
                                    font=CONFIG["fuente_botones"], width=CONFIG["ancho_boton"], height=CONFIG["alto_boton"])
        self.btn_delete.grid(row=0, column=2, padx=5)
        Tooltip(self.btn_delete, "Elimina la tarea seleccionada de la lista.")

        # Lista de tareas
        self.lista = tk.Listbox(self.root, width=60, height=15, selectmode=tk.SINGLE, font=CONFIG["fuente"])
        self.lista.pack(pady=10)
        # Doble clic también marca como completada
        self.lista.bind("<Double-1>", self.marcar_completada)
        Tooltip(self.lista, "Haz doble clic en una tarea para marcarla como completada.")

        # Diccionario para estados de tareas (True= completada, False= pendiente)
        self.tareas = {}

        # Cargar las tareas previas desde el archivo JSON
        self.cargar_tareas()

    #  FUNCIONES DE LÓGICA

    def guardar_tareas(self):
        """Guarda las tareas y sus estados en un archivo JSON."""
        datos = []
        for i in range(self.lista.size()):
            texto = self.lista.get(i)
            estado = self.tareas.get(i, False)
            datos.append({"texto": texto, "completada": estado})
        # Se escribe el archivo JSON con indentación y UTF-8
        with open(ARCHIVO_TAREAS, "w", encoding="utf-8") as f:
            json.dump(datos, f, indent=4, ensure_ascii=False)

    def cargar_tareas(self):
        """Carga tareas desde el archivo JSON si existe."""
        if os.path.exists(ARCHIVO_TAREAS):
            with open(ARCHIVO_TAREAS, "r", encoding="utf-8") as f:
                datos = json.load(f)
                for tarea in datos:
                    self.lista.insert(tk.END, tarea["texto"])
                    index = self.lista.size() - 1
                    self.tareas[index] = tarea["completada"]

    def agregar_tarea(self, event=None):
        """Añade una nueva tarea escrita en el Entry."""
        tarea = self.entry.get().strip()
        if tarea:
            self.lista.insert(tk.END, tarea)       # Insertar en la lista
            index = self.lista.size() - 1
            self.tareas[index] = False             # Estado inicial = pendiente
            self.entry.delete(0, tk.END)           # Limpiar caja de texto
            self.guardar_tareas()                  # Guardar en JSON
        else:
            messagebox.showwarning("Atención", "No puedes añadir una tarea vacía.")

    def marcar_completada(self, event=None):
        """Marca/desmarca la tarea seleccionada como completada."""
        seleccion = self.lista.curselection()
        if seleccion:
            index = seleccion[0]
            estado = self.tareas.get(index, False)
            texto = self.lista.get(index)

            if not estado:
                # Añadir un "✔" al inicio del texto
                self.lista.delete(index)
                self.lista.insert(index, f"✔ {texto}")
                self.tareas[index] = True
            else:
                # Quitar el "✔"
                texto_sin_check = texto.replace("✔ ", "")
                self.lista.delete(index)
                self.lista.insert(index, texto_sin_check)
                self.tareas[index] = False

            self.guardar_tareas()  # Guardar cambios
        else:
            messagebox.showinfo("Información", "Selecciona una tarea para marcarla.")

    def eliminar_tarea(self):
        """Elimina la tarea seleccionada de la lista y del diccionario."""
        seleccion = self.lista.curselection()
        if seleccion:
            index = seleccion[0]
            self.lista.delete(index)     # Borra de la lista
            del self.tareas[index]       # Borra del diccionario
            # Reorganiza índices para mantener coherencia
            self.tareas = {i: self.tareas.get(i, False) for i in range(self.lista.size())}
            self.guardar_tareas()        # Guardar cambios
        else:
            messagebox.showinfo("Información", "Selecciona una tarea para eliminarla.")

#  PROGRAMA PRINCIPAL
if __name__ == "__main__":
    root = tk.Tk()            # Crea la ventana principal
    app = GestorTareas(root)  # Instancia la aplicación
    root.mainloop()           # Inicia el loop principal de Tkinter