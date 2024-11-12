import tkinter as tk
from tkinter import ttk, messagebox

class GestorTareasGUI:
    def __init__(self, root, gestor):
        self.gestor = gestor
        self.root = root
        self.root.title("Gestor de Tareas")

        # Configurar la ventana principal
        self.frame = ttk.Frame(root, padding="15")
        self.frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Título con texto en negrita y tamaño 10
        ttk.Label(self.frame, text="Título de la Tarea:", font=("Arial", 10, "bold")).grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.titulo_entry = ttk.Entry(self.frame, width=40)
        self.titulo_entry.grid(row=0, column=1, sticky=tk.W, padx=5, pady=5)
        self.titulo_entry.insert(0, "Escribe el título aquí...")
        self.titulo_entry.bind("<FocusIn>", self.eliminar_texto_titulo)
        self.titulo_entry.bind("<FocusOut>", self.agregar_texto_titulo)

        # Descripción con texto en negrita y tamaño 10
        ttk.Label(self.frame, text="Descripción de la Tarea:", font=("Arial", 10, "bold")).grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.descripcion_text = tk.Text(self.frame, width=40, height=5)
        self.descripcion_text.grid(row=1, column=1, sticky=tk.W, padx=5, pady=5)
        self.descripcion_text.insert("1.0", "Escribe una descripción aquí...")
        self.descripcion_text.bind("<FocusIn>", self.eliminar_texto_descripcion)
        self.descripcion_text.bind("<FocusOut>", self.agregar_texto_descripcion)

        # Botón Agregar
        self.agregar_btn = ttk.Button(self.frame, text="Agregar Tarea", command=self.agregar_tarea)
        self.agregar_btn.grid(row=2, column=1, sticky=tk.W, padx=5, pady=5)

        # Lista de tareas
        self.tareas_listbox = tk.Listbox(self.frame, height=10, width=70)  # Ancho más grande para mostrar la fecha
        self.tareas_listbox.grid(row=3, column=1, sticky=tk.W, padx=5, pady=5)

        # Botones de acción
        self.completar_btn = ttk.Button(self.frame, text="Marcar como Completada", command=self.marcar_completada, state=tk.DISABLED)
        self.completar_btn.grid(row=4, column=1, sticky=tk.W, padx=5, pady=5)

        self.eliminar_btn = ttk.Button(self.frame, text="Eliminar Tarea", command=self.eliminar_tarea, state=tk.DISABLED)
        self.eliminar_btn.grid(row=5, column=1, sticky=tk.W, padx=5, pady=5)

        # Botón de Salir
        self.salir_btn = ttk.Button(self.frame, text="Salir", command=self.salir)
        self.salir_btn.grid(row=6, column=1, sticky=tk.W, padx=5, pady=10)

        # Actualizar la lista de tareas
        self.actualizar_lista()

        # Vincular selección en la lista de tareas
        self.tareas_listbox.bind('<<ListboxSelect>>', self.habilitar_botones)

    # Función para agregar tarea
    def agregar_tarea(self):
        titulo = self.titulo_entry.get()
        descripcion = self.descripcion_text.get("1.0", tk.END).strip()
        try:
            self.gestor.agregar_tarea(titulo, descripcion)
            self.actualizar_lista()
            self.titulo_entry.delete(0, tk.END)
            self.descripcion_text.delete("1.0", tk.END)
            self.titulo_entry.insert(0, "Escribe el título aquí...")
            self.descripcion_text.insert("1.0", "Escribe una descripción aquí...")
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    # Función para actualizar la lista de tareas
    def actualizar_lista(self):
        self.tareas_listbox.delete(0, tk.END)
        for indice, tarea in enumerate(self.gestor.obtener_tareas()):
            estado = "Completada" if tarea.completada else "Pendiente"
            self.tareas_listbox.insert(tk.END, f"{indice + 1}. {tarea.titulo} - {estado} - {tarea.fecha_carga}")

    # Habilitar los botones cuando se selecciona una tarea
    def habilitar_botones(self, event=None):
        seleccion = self.tareas_listbox.curselection()
        if seleccion:
            self.completar_btn.config(state=tk.NORMAL)
            self.eliminar_btn.config(state=tk.NORMAL)
        else:
            self.completar_btn.config(state=tk.DISABLED)
            self.eliminar_btn.config(state=tk.DISABLED)

    # Función para marcar la tarea como completada
    def marcar_completada(self):
        seleccion = self.tareas_listbox.curselection()
        if seleccion:
            indice = seleccion[0]
            self.gestor.marcar_completada(indice)
            self.actualizar_lista()
        else:
            messagebox.showwarning("Advertencia", "Selecciona una tarea para marcar como completada")

    # Función para eliminar una tarea
    def eliminar_tarea(self):
        seleccion = self.tareas_listbox.curselection()
        if seleccion:
            indice = seleccion[0]
            self.gestor.eliminar_tarea(indice)
            self.actualizar_lista()
        else:
            messagebox.showwarning("Advertencia", "Selecciona una tarea para eliminar")

    # Función para cerrar la aplicación
    def salir(self):
        self.root.quit()

    # Función para eliminar el texto de ejemplo en el campo de título
    def eliminar_texto_titulo(self, event=None):
        if self.titulo_entry.get() == "Escribe el título aquí...":
            self.titulo_entry.delete(0, tk.END)

    # Función para agregar el texto de ejemplo en el campo de título
    def agregar_texto_titulo(self, event=None):
        if not self.titulo_entry.get():
            self.titulo_entry.insert(0, "Escribe el título aquí...")

    # Función para eliminar el texto de ejemplo en el campo de descripción
    def eliminar_texto_descripcion(self, event=None):
        if self.descripcion_text.get("1.0", tk.END).strip() == "Escribe una descripción aquí...":
            self.descripcion_text.delete("1.0", tk.END)

    # Función para agregar el texto de ejemplo en el campo de descripción
    def agregar_texto_descripcion(self, event=None):
        if not self.descripcion_text.get("1.0", tk.END).strip():
            self.descripcion_text.insert("1.0", "Escribe una descripción aquí...")
