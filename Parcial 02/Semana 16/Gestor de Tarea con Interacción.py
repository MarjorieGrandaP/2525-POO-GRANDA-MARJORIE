# Creación de una aplicación que permite crear una lista de tareas
import tkinter as tk  # Importo tkinter para crear la GUI
from tkinter import messagebox  # Importo messagebox para mostrar ventanas de alerta
import json  # Importo json para guardar y cargar tareas
import os    # Importo os para verificar si existe el archivo de tareas


# CONFIGURACIÓN PERSONALIZABLE
CONFIG = {
    "fondo": "#e6e3a8",  # Defino el color de fondo de la ventana
    "color_texto": "#071447",  # Defino el color del texto
    "color_botones": "#317182",  # Color normal de los botones
    "color_botones_hover": "#45a049",  # Color de botones al pasar el mouse
    "fuente": ("OpenDyslexic", 12),  # Fuente para los textos
    "fuente_botones": ("Arial", 11, "bold"),  # Fuente para los botones
    "alto_boton": 2,  # Altura de los botones
    "ancho_boton": 18  # Anchura de los botones
}

ARCHIVO_TAREAS = "tareas.json"  # Archivo donde guardo las tareas


# TOOLTIP (Mensajes emergentes)

class Tooltip:
    """Clase que muestra un mensaje flotante al pasar el mouse sobre un widget"""
    def __init__(self, widget, texto):
        self.widget = widget  # Guardo el widget
        self.texto = texto  # Guardo el texto del tooltip
        self.tooltip = None  # Inicializo la variable que contendrá el tooltip
        widget.bind("<Enter>", self.mostrar)  # Cuando el mouse entra, muestro el tooltip
        widget.bind("<Leave>", self.ocultar)  # Cuando el mouse sale, oculto el tooltip

    def mostrar(self, event=None):
        try:
            x, y, _, _ = self.widget.bbox("insert")  # Intento obtener la posición del cursor
        except:
            x = y = 0  # Si el widget no tiene cursor, pongo x=0, y=0
        x += self.widget.winfo_rootx() + 25  # Ajusto la posición horizontal
        y += self.widget.winfo_rooty() + 25  # Ajusto la posición vertical
        self.tooltip = tk.Toplevel(self.widget)  # Creo la ventana flotante
        self.tooltip.wm_overrideredirect(True)  # Quito bordes
        self.tooltip.wm_geometry(f"+{x}+{y}")  # Posiciono el tooltip
        label = tk.Label(self.tooltip, text=self.texto, bg="yellow", relief="solid",
                         borderwidth=1, font=("Arial", 9))
        label.pack(ipadx=3)  # Agrego padding interno

    def ocultar(self, event=None):
        if self.tooltip:  # Si existe el tooltip
            self.tooltip.destroy()  # Lo destruyo
            self.tooltip = None

# APLICACIÓN PRINCIPAL

class GestorTareas:
    def __init__(self, root):
        self.root = root  # Guardo la ventana principal
        self.root.title("Gestor de Tareas")  # Pongo título a la ventana
        self.root.configure(bg=CONFIG["fondo"])  # Aplico color de fondo

        # Ajusto tamaño de la ventana según porcentaje de pantalla
        ancho = int(self.root.winfo_screenwidth() * 0.4)
        alto = int(self.root.winfo_screenheight() * 0.6)
        self.root.geometry(f"{ancho}x{alto}")  # Configuro geometría

        # Texto introductorio
        label_intro = tk.Label(
            self.root,
            text="Bienvenido/a al Gestor de Tareas.\n\nAquí podrás añadir, completar y eliminar tareas.\n"
                 "A continuación escribe una Tarea por completar 📌",
            bg=CONFIG["fondo"], fg=CONFIG["color_texto"], font=("Arial", 12), justify="center"
        )
        label_intro.pack(pady=10)  # Lo agrego a la ventana con padding vertical

        # Entrada de texto para nuevas tareas
        self.entry = tk.Entry(self.root, width=40, font=CONFIG["fuente"])
        self.entry.pack(pady=10)
        self.entry.bind("<Return>", self.agregar_tarea)  # Solo Enter añade la tarea
        Tooltip(self.entry, "Escribe aquí la nueva tarea y presiona Enter o el botón Añadir.")


        # Frame de botones

        frame_botones = tk.Frame(self.root, bg=CONFIG["fondo"])
        frame_botones.pack(pady=5)

        # Botón: Añadir tarea
        self.btn_add = tk.Button(frame_botones, text="Añadir Tarea", command=self.agregar_tarea,
                                 bg=CONFIG["color_botones"], fg="white",
                                 font=CONFIG["fuente_botones"], width=CONFIG["ancho_boton"], height=CONFIG["alto_boton"])
        self.btn_add.grid(row=0, column=0, padx=5)
        Tooltip(self.btn_add, "Añade la tarea escrita en la caja de texto.\nAtajo: Enter")

        # Botón: Marcar completada
        self.btn_done = tk.Button(frame_botones, text="Marcar como Completada", command=self.marcar_completada,
                                  bg=CONFIG["color_botones"], fg="white",
                                  font=CONFIG["fuente_botones"], width=CONFIG["ancho_boton"], height=CONFIG["alto_boton"])
        self.btn_done.grid(row=0, column=1, padx=5)
        Tooltip(self.btn_done, "Marca la tarea seleccionada como completada.\nAtajo: C")

        # Botón: Eliminar tarea
        self.btn_delete = tk.Button(frame_botones, text="Eliminar Tarea", command=self.eliminar_tarea,
                                    bg=CONFIG["color_botones"], fg="white",
                                    font=CONFIG["fuente_botones"], width=CONFIG["ancho_boton"], height=CONFIG["alto_boton"])
        self.btn_delete.grid(row=0, column=2, padx=5)
        Tooltip(self.btn_delete, "Elimina la tarea seleccionada de la lista.\nAtajo: D / Delete")


        # Lista de tareas

        self.lista = tk.Listbox(self.root, width=60, height=15, selectmode=tk.SINGLE, font=CONFIG["fuente"])
        self.lista.pack(pady=10)
        self.lista.bind("<Double-1>", self.marcar_completada)
        Tooltip(self.lista, "Haz doble clic en una tarea para marcarla como completada.")

        # Diccionario para estados de tareas
        self.tareas = {}
        self.cargar_tareas()  # Cargo tareas si existen
        self.actualizar_colores()  # Aplico colores según estado


        # Atajos de teclado globales solo en la lista
        self.root.bind("<Key>", self.manejador_teclas)  # Capturo todas las teclas


        # Tabla de atajos dentro de la ventana
        self.crear_tabla_atajos()

        # Captura cierre de ventana
        self.root.protocol("WM_DELETE_WINDOW", self.cerrar_app)


    # Funciones de lógica

    def guardar_tareas(self):
        datos = []
        for i in range(self.lista.size()):
            texto = self.lista.get(i)
            estado = self.tareas.get(i, False)
            datos.append({"texto": texto, "completada": estado})
        with open(ARCHIVO_TAREAS, "w", encoding="utf-8") as f:
            json.dump(datos, f, indent=4, ensure_ascii=False)

    def cargar_tareas(self):
        if os.path.exists(ARCHIVO_TAREAS):
            with open(ARCHIVO_TAREAS, "r", encoding="utf-8") as f:
                datos = json.load(f)
                for tarea in datos:
                    self.lista.insert(tk.END, tarea["texto"])
                    index = self.lista.size() - 1
                    self.tareas[index] = tarea["completada"]

    def actualizar_colores(self):
        for i in range(self.lista.size()):
            estado = self.tareas.get(i, False)
            if estado:
                self.lista.itemconfig(i, fg="white", bg="#4CAF50")
            else:
                self.lista.itemconfig(i, fg="black", bg="white")

    def agregar_tarea(self, event=None):
        tarea = self.entry.get().strip()
        if tarea:
            self.lista.insert(tk.END, tarea)
            index = self.lista.size() - 1
            self.tareas[index] = False
            self.entry.delete(0, tk.END)
            self.guardar_tareas()
            self.actualizar_colores()
        else:
            messagebox.showwarning("Atención", "No puedes añadir una tarea vacía.")

    def marcar_completada(self, event=None):
        seleccion = self.lista.curselection()
        if seleccion:
            index = seleccion[0]
            estado = self.tareas.get(index, False)
            texto = self.lista.get(index)
            if not estado:
                self.lista.delete(index)
                self.lista.insert(index, f"✔ {texto}")
                self.tareas[index] = True
            else:
                texto_sin_check = texto.replace("✔ ", "")
                self.lista.delete(index)
                self.lista.insert(index, texto_sin_check)
                self.tareas[index] = False
            self.guardar_tareas()
            self.actualizar_colores()
        else:
            messagebox.showinfo("Información", "Selecciona una tarea para marcarla.")

    def eliminar_tarea(self, event=None):
        seleccion = self.lista.curselection()
        if seleccion:
            index = seleccion[0]
            self.lista.delete(index)
            del self.tareas[index]
            self.tareas = {i: self.tareas.get(i, False) for i in range(self.lista.size())}
            self.guardar_tareas()
            self.actualizar_colores()
        else:
            messagebox.showinfo("Información", "Selecciona una tarea para eliminarla.")

    def cerrar_app(self):
        messagebox.showinfo("¡Hasta luego!", "¡Ha sido un placer ayudarte!")
        self.root.destroy()


    # Manejo de atajos de teclado

    def manejador_teclas(self, event):
        """Solo ejecuto los atajos si el foco está en la lista de tareas"""
        widget_actual = self.root.focus_get()
        if widget_actual == self.lista:
            tecla = event.keysym.lower()
            if tecla == "c":
                self.marcar_completada()
            elif tecla == "d" or tecla == "delete":
                self.eliminar_tarea()
        # Si el foco está en el Entry u otro widget, no hago nada

    # Crear tabla de atajos dentro de la ventana
    def crear_tabla_atajos(self):
        frame_info = tk.Frame(self.root, bg=CONFIG["fondo"])
        frame_info.pack(pady=10, fill="x")

        label_info = tk.Label(frame_info, text="Atajos de teclado disponibles",
                              bg=CONFIG["fondo"], fg=CONFIG["color_texto"], font=("Arial", 12, "bold"))
        label_info.grid(row=0, column=0, columnspan=2, pady=5, sticky="w")

        atajos = [
            ("Acción", "Atajo"),
            ("Añadir tarea", "Enter"),
            ("Marcar completada", "C"),
            ("Eliminar tarea", "D / Delete"),
            ("Salir de la aplicación", "Escape")
        ]

        for i, (accion, tecla) in enumerate(atajos, start=1):
            fg_color = "black"
            font_style = ("Arial", 11)
            tk.Label(frame_info, text=accion, bg=CONFIG["fondo"], fg=fg_color, font=font_style,
                     width=25, anchor="w").grid(row=i, column=0, padx=5, sticky="w")
            tk.Label(frame_info, text=tecla, bg=CONFIG["fondo"], fg=fg_color, font=font_style,
                     width=15, anchor="w").grid(row=i, column=1, padx=5, sticky="w")

# EJECUCION DEL PROGRAMA PRINCIPAL

if __name__ == "__main__":
    root = tk.Tk()
    app = GestorTareas(root)
    root.mainloop()
