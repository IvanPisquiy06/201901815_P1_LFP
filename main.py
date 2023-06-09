from tkinter import *
from tkinter import ttk

root = Tk()
root.title("Gramáticas Regulares")

window = ttk.Frame(root, padding=50)
window.grid()

ttk.Label(window, text="Lenguajes formales y de Programación").grid(column=0, row=0)
ttk.Label(window, text="Sección: A").grid(column=1, row=0)
ttk.Label(window, text="Carné: 201901815").grid(column=0, row=1)
ttk.Label(window, text="Ivan de Jesus Pisquiy Escobar").grid(column=1, row=1)

ttk.Button(window, text="AFN").grid(column=0, row=4, padx=20, pady=10)
ttk.Button(window, text="AFD").grid(column=1, row=4, padx=20, pady=10)
ttk.Button(window, text="OE").grid(column=0, row=5, padx=20, pady=10)
ttk.Button(window, text="Carga Masiva").grid(column=1, row=5, padx=20, pady=10)
ttk.Button(window, text="Quit", command=root.destroy).grid(column=0, row=6, padx=20, pady=10)
root.mainloop()