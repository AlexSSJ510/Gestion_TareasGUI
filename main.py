
from src.vista.gestor_tareasGUI import GestorTareasGUI
from src.logica.gestor_tarea import GestorTareas

if __name__ == "__main__":
    import tkinter as tk
    from tkinter import ttk

    root = tk.Tk()
    gestor = GestorTareas()
    app = GestorTareasGUI(root, gestor)
    root.mainloop()


