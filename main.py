from tkinter import *
from tkinter import filedialog
from tkinter import ttk
from tkinter import messagebox

contenido_texto = None

def carga_masiva():

    def abrir_archivo_afd():
        global contenido_texto
        # Abre el diálogo de buscar archivo y retorna la ruta del archivo seleccionado
        ruta_archivo = filedialog.askopenfilename(filetypes=[('Archivos AFD', '*.afd')])

        # Verifica si se seleccionó un archivo y si es así, lo lee y lo devuelve como un diccionario de Python
        if ruta_archivo:
            with open(ruta_archivo, 'r') as archivo_texto:
                contenido_texto = archivo_texto.read()
    
    def abrir_archivo_afn():
        global contenido_texto
        # Abre el diálogo de buscar archivo y retorna la ruta del archivo seleccionado
        ruta_archivo = filedialog.askopenfilename(filetypes=[('Archivos AFN', '*.afn')])

        # Verifica si se seleccionó un archivo y si es así, lo lee y lo devuelve como un diccionario de Python
        if ruta_archivo:
            with open(ruta_archivo, 'r') as archivo_texto:
                contenido_texto = archivo_texto.read()

    root = Tk()
    root.title("Carga Masiva")

    window = ttk.Frame(root, padding=50)
    window.grid()

    ttk.Label(window, text="Por favor, elija qué tipo de archivo desea cargar").grid(column=0, row=0, pady=30)

    ttk.Button(window, text="AFD", command=abrir_archivo_afd).grid(column=0, row=1, padx=20, pady=10)
    ttk.Button(window, text="AFN", command=abrir_archivo_afn).grid(column=0, row=2, padx=20, pady=10)
    ttk.Button(window, text="Cerrar", command=root.destroy).grid(column=0, row=3, padx=20, pady=10)

    root.mainloop()

def menu_afd():
    global contenido_texto

    def crear_afn():

        def guardar_datos():
            nombre = entry_nombre.get()
            estados = entry_estados.get().split(';')
            alfabeto = entry_alfabeto.get().split(';')
            estado_inicial = entry_estado_inicial.get()
            estados_aceptacion = entry_estados_aceptacion.get().split(';')
            transiciones = entry_transiciones.get().split(';')

            # Validar los datos ingresados y realizar las operaciones necesarias
            # ...

            # Ejemplo: Mostrar los datos ingresados
            messagebox.showinfo("Datos ingresados",
                                f"Nombre: {nombre}\n"
                                f"Estados: {estados}\n"
                                f"Alfabeto: {alfabeto}\n"
                                f"Estado Inicial: {estado_inicial}\n"
                                f"Estados de Aceptación: {estados_aceptacion}\n"
                                f"Transiciones: {transiciones}")

        root = Tk()
        root.title("Crear AFN")

        window = ttk.Frame(root, padding=50)
        window.grid()

        ttk.Label(window, text="Creando AFN (LLenar los siguientes campos)").grid(column=0, row=0)

        # Etiqueta y campo de entrada para el Nombre
        ttk.Label(window, text="Nombre:").grid(column=0, row=1)
        entry_nombre = ttk.Entry(window).grid(column=1, row=1)

        # Etiqueta y campo de entrada para los Estados
        ttk.Label(window, text="Estados:").grid(column=0, row=2)
        entry_estados = ttk.Entry(window).grid(column=1, row=2)

        # Etiqueta y campo de entrada para el Alfabeto
        ttk.Label(window, text="Alfabeto:").grid(column=0, row=3)
        entry_alfabeto = ttk.Entry(window).grid(column=1, row=3)

        # Etiqueta y campo de entrada para el Estado Inicial
        ttk.Label(window, text="Estado Inicial:").grid(column=0, row=4)
        entry_estado_inicial = ttk.Entry(window).grid(column=1, row=4)

        # Etiqueta y campo de entrada para los Estados de Aceptación
        ttk.Label(window, text="Estados de Aceptación:").grid(column=0, row=5)
        entry_estados_aceptacion = ttk.Entry(window).grid(column=1, row=5)

        # Etiqueta y campo de entrada para las Transiciones
        ttk.Label(window, text="Transiciones:").grid(column=0, row=6)
        entry_transiciones = ttk.Entry(window).grid(column=1, row=6)

        ttk.Button(window, text="Crear AFN", command=guardar_datos).grid(column=0, row=7, padx=20, pady=10)
        ttk.Button(window, text="Cerrar", command=root.destroy).grid(column=1, row=7, padx=20, pady=10)

        root.mainloop()

    root = Tk()
    root.title("Menu AFN")

    window = ttk.Frame(root, padding=50)
    window.grid()

    ttk.Label(window, text="Sección: A").grid(column=0, row=0)
    ttk.Label(window, text="Carné: 201901815").grid(column=0, row=1)
    ttk.Label(window, text="Ivan de Jesus Pisquiy Escobar").grid(column=0, row=2)

    ttk.Button(window, text="Crear AFN", command=crear_afn).grid(column=0, row=3, padx=20, pady=10)
    ttk.Button(window, text="Evaluar Cadena").grid(column=0, row=4, padx=20, pady=10)
    ttk.Button(window, text="Generar Reporte AFN").grid(column=0, row=5, padx=20, pady=10)
    ttk.Button(window, text="Cerrar", command=root.destroy).grid(column=0, row=6, padx=20, pady=10)

    root.mainloop()


def mostrar_contenido():
    global contenido_texto
    if contenido_texto:
        lineas = contenido_texto.splitlines()
        print(lineas)

def main_window():
    root = Tk()
    root.title("Gramáticas Regulares")

    window = ttk.Frame(root, padding=50)
    window.grid()

    ttk.Label(window, text="Lenguajes formales y de Programación").grid(column=0, row=0)
    ttk.Label(window, text="Sección: A").grid(column=1, row=0)
    ttk.Label(window, text="Carné: 201901815").grid(column=0, row=1)
    ttk.Label(window, text="Ivan de Jesus Pisquiy Escobar").grid(column=1, row=1)

    ttk.Button(window, text="AFN", command=menu_afd).grid(column=0, row=4, padx=20, pady=10)
    ttk.Button(window, text="AFD").grid(column=1, row=4, padx=20, pady=10)
    ttk.Button(window, text="OE").grid(column=0, row=5, padx=20, pady=10)
    ttk.Button(window, text="Carga Masiva", command=carga_masiva).grid(column=1, row=5, padx=20, pady=10)
    ttk.Button(window, text="Cerrar", command=root.quit).grid(column=0, row=6, padx=20, pady=10)
    root.mainloop()

main_window()