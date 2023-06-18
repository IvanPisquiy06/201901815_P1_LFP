from tkinter import *
from tkinter import filedialog
from tkinter import ttk
from tkinter import messagebox
import os
import graphviz
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from PIL import ImageTk, Image

contenido_texto = None

def reporte():
    global contenido_texto

    lineas = contenido_texto.splitlines()
    nombres = []

    grupos = []
    grupo_actual = []

    for elemento in lineas:
        if elemento == "%":
            grupos.append(grupo_actual)
            grupo_actual = []
        else:
            grupo_actual.append(elemento)

    for i in range(len(grupos)):
        nombres.append(grupos[i][0])

    def crear_reporte():

        automata = combobox.current()

        nombre = grupos[automata][0]
        estados = grupos[automata][1].split(',')
        alfabetos = grupos[automata][2].split(',')
        inicial = grupos[automata][3]
        aceptacion = grupos[automata][4]
        transiciones = grupos[automata][5:]

        grafica = graphviz.Digraph(format='png')
        conexiones = {}
        
        for j in range(len(estados)):
            grafica.node(estados[j], color='yellow')
        for transicion in transiciones:
            fase = transicion.split(';')
            inicial = fase[0].split(',')
            if (inicial[0], fase[1]) in conexiones:
                # Agregar el label al conector existente
                conexiones[(inicial[0], fase[1])]['label'] += f",{inicial[1]}"
            else:
                # Crear un nuevo conector
                conexiones[(inicial[0], fase[1])] = {'label': inicial[1]}

        # Agregar los conectores al gráfico
        for conexion, atributos in conexiones.items():
            origen, destino = conexion
            label = atributos['label']
            grafica.edge(origen, destino, label=label)

        archivo = f'{nombre}'
        grafica.render(archivo, cleanup=True)

        #Creando PDF
        c = canvas.Canvas(f"{nombre}.pdf", pagesize=letter)

        # Agregar texto al PDF
        c.drawString(3.5 * inch, 10 * inch, f'Nombre: {nombre}')
        c.drawString(1 * inch, 9.5 * inch, f'Estados: {grupos[i][1]}')
        c.drawString(1 * inch, 9.25 * inch, f'Alfabeto: {grupos[i][2]}')
        c.drawString(1 * inch, 9 * inch, f'Estados de aceptación: {aceptacion}')
        c.drawString(1 * inch, 8.5 * inch, f'Estados inicial: {grupos[i][3]}')
        c.drawString(1 * inch, 8 * inch, 'Transiciones:')
        y = 7.75
        for transicion in transiciones:
            c.drawString(1 * inch, y * inch, transicion)
            y -= 0.25

        # Agregar una imagen al PDF
        image_path = archivo + '.png'
        c.drawImage(image_path, 4.5 * inch, 4 * inch) 

        # Guardar y cerrar el PDF
        c.save()

        messagebox.showinfo("¡Éxito!", "Reporte creado correctamente")
        main_reporte.destroy()

    main_reporte = Tk()
    main_reporte.title("Menú reporte")

    window = ttk.Frame(main_reporte, padding=50)
    window.grid()

    ttk.Label(window, text="Elija un autómata disponible para crear reporte").grid()

    combobox = ttk.Combobox(window, values=nombres)
    combobox.current(0)  # Establecer el valor predeterminado
    combobox.grid()
    ttk.Button(window, text="Crear Reporte", command=crear_reporte).grid()

def carga_masiva():

    def abrir_archivo_afd():
        global contenido_texto
        # Abre el diálogo de buscar archivo y retorna la ruta del archivo seleccionado
        ruta_archivo = filedialog.askopenfilename(filetypes=[('Archivos AFD', '*.afd')])

        # Verifica si se seleccionó un archivo y si es así, lo lee y lo devuelve como un diccionario de Python
        if ruta_archivo:
            with open(ruta_archivo, 'r') as archivo_texto:
                contenido_texto = archivo_texto.read()
        main_masiva.destroy()
    
    def abrir_archivo_afn():
        global contenido_texto
        # Abre el diálogo de buscar archivo y retorna la ruta del archivo seleccionado
        ruta_archivo = filedialog.askopenfilename(filetypes=[('Archivos AFN', '*.afn')])

        # Verifica si se seleccionó un archivo y si es así, lo lee y lo devuelve como un diccionario de Python
        if ruta_archivo:
            with open(ruta_archivo, 'r') as archivo_texto:
                contenido_texto = archivo_texto.read()
        main_masiva.destroy()

    main_masiva = Tk()
    main_masiva.title("Carga Masiva")

    window = ttk.Frame(main_masiva, padding=50)
    window.grid()

    ttk.Label(window, text="Por favor, elija qué tipo de archivo desea cargar").grid(column=0, row=0, pady=30)

    ttk.Button(window, text="AFD", command=abrir_archivo_afd).grid(column=0, row=1, padx=20, pady=10)
    ttk.Button(window, text="AFN", command=abrir_archivo_afn).grid(column=0, row=2, padx=20, pady=10)
    ttk.Button(window, text="Cerrar", command=main_masiva.destroy).grid(column=0, row=3, padx=20, pady=10)

#Menu AFN
def menu_afn():
    global contenido_texto

    #Funcion para crear un archivo AFN
    def crear_afn():

        main_afn.destroy()

        def guardar_datos():

            nombre = entry_nombre.get()
            estados = entry_estados.get()
            alfabeto = entry_alfabeto.get()
            inicial = entry_inicial.get()
            aceptados = entry_aceptados.get()
            transiciones = entry_transiciones.get().split(' ')

            contenido = f"{nombre}\n"
            contenido += f"{estados}\n"
            contenido += f"{alfabeto}\n"
            contenido += f"{inicial}\n"
            contenido += f"{aceptados}\n"
            for transicion in transiciones:
                contenido += f"{transicion}\n"

            nombre_archivo = f"{nombre}.afn"

            file = open(nombre_archivo, 'w')
            file.write(contenido)
            file.close()

            create_afn.destroy()

            messagebox.showinfo("¡Éxito!", "Datos guardados correctamente")

        create_afn = Tk()
        create_afn.title("Crear AFN")

        window = ttk.Frame(create_afn, padding=50)
        window.grid()

        ttk.Label(window, text="Creando AFN (LLenar los siguientes campos)").grid(column=0, row=0)

        # Etiqueta y campo de entrada para el Nombre
        ttk.Label(window, text="Nombre:").grid(column=0, row=1)
        entry_nombre = ttk.Entry(window)
        entry_nombre.grid(column=1, row=1)

        # Etiqueta y campo de entrada para los Estados
        ttk.Label(window, text="Estados:").grid(column=0, row=2)
        entry_estados = ttk.Entry(window)
        entry_estados.grid(column=1, row=2)

        # Etiqueta y campo de entrada para el Alfabeto
        ttk.Label(window, text="Alfabeto:").grid(column=0, row=3)
        entry_alfabeto = ttk.Entry(window)
        entry_alfabeto.grid(column=1, row=3)

        # Etiqueta y campo de entrada para el Estado Inicial
        ttk.Label(window, text="Estado Inicial:").grid(column=0, row=4)
        entry_inicial = ttk.Entry(window)
        entry_inicial.grid(column=1, row=4)

        # Etiqueta y campo de entrada para los Estados de Aceptación
        ttk.Label(window, text="Estados de Aceptación:").grid(column=0, row=5)
        entry_aceptados = ttk.Entry(window)
        entry_aceptados.grid(column=1, row=5)

        # Etiqueta y campo de entrada para las Transiciones
        ttk.Label(window, text="Transiciones:").grid(column=0, row=6)
        entry_transiciones = ttk.Entry(window)
        entry_transiciones.grid(column=1, row=6)

        ttk.Button(window, text="Aceptar", command=guardar_datos).grid(column=0, row=7, padx=20, pady=10)
        ttk.Button(window, text="Cerrar", command=create_afn.destroy).grid(column=1, row=7, padx=20, pady=10)

    def evaluar_afn():
        main_afn.destroy()

        main_evaluar = Tk()
        main_evaluar.title("Evaluar Cadena")

        window = ttk.Frame(main_evaluar, padding=50)
        window.grid()

        ttk.Label(window, text="Seleccione una de las siguientes").grid()

        ttk.Button(window, text="Solo Evaluar").grid(pady=10)
        ttk.Button(window, text="Ruta").grid(pady=10)
        ttk.Button(window, text="Cerrar", command=main_evaluar.destroy).grid(pady=10)

    #Ventana que despliega información de un autómata AFN
    def ayuda_afn():

        info_afn = Tk()
        info_afn.title("Ayuda")

        window = ttk.Frame(info_afn, padding=50)
        window.grid()

        info = "Un autómata finito no determinista (AFN) es un modelo matemático utilizado en el campo de la teoría de autómatas y lenguajes formales."
        info2 = "Es una variante del autómata finito (AF) que permite transiciones no deterministas,"
        info3 = "lo que significa que en un estado dado puede haber múltiples transiciones posibles para un símbolo de entrada determinado."

        ttk.Label(window, text="¿Qué es un Autómata AFN?").grid()
        ttk.Label(window, text=info).grid()
        ttk.Label(window, text=info2).grid()
        ttk.Label(window, text=info3).grid()

        ttk.Button(window, text="Cerrar", command=info_afn.destroy).grid(pady=10)

    main_afn = Tk()
    main_afn.title("Menu AFN")

    window = ttk.Frame(main_afn, padding=50)
    window.grid()

    ttk.Label(window, text="Sección: A").grid(column=0, row=0)
    ttk.Label(window, text="Carné: 201901815").grid(column=1, row=0)
    ttk.Label(window, text="Ivan de Jesus Pisquiy Escobar").grid(column=0, row=1)

    ttk.Button(window, text="Crear AFN", command=crear_afn).grid(column=0, row=2, padx=20, pady=10)
    ttk.Button(window, text="Evaluar Cadena", command=evaluar_afn).grid(column=1, row=2, padx=20, pady=10)
    ttk.Button(window, text="Generar Reporte AFN", command=reporte).grid(column=0, row=3, padx=20, pady=10)
    ttk.Button(window, text="Ayuda", command=ayuda_afn).grid(column=1, row=3, padx=20, pady=10)
    ttk.Button(window, text="Cerrar", command=main_afn.destroy).grid(column=0, row=4, padx=20, pady=10)

def menu_afd():
    global contenido_texto

    #Funcion para crear un archivo AFN
    def crear_afd():

        main_afn.destroy()

        def guardar_datos_afd():

            nombre = entry_nombre.get()
            estados = entry_estados.get()
            alfabeto = entry_alfabeto.get()
            inicial = entry_inicial.get()
            aceptados = entry_aceptados.get()
            transiciones = entry_transiciones.get().split(' ')

            contenido = f"{nombre}\n"
            contenido += f"{estados}\n"
            contenido += f"{alfabeto}\n"
            contenido += f"{inicial}\n"
            contenido += f"{aceptados}\n"
            for transicion in transiciones:
                contenido += f"{transicion}\n"

            nombre_archivo = f"{nombre}.afd"

            file = open(nombre_archivo, 'w')
            file.write(contenido)
            file.close()

            create_afn.destroy()

            messagebox.showinfo("¡Éxito!", "Datos guardados correctamente")

        create_afn = Tk()
        create_afn.title("Crear AFD")

        window = ttk.Frame(create_afn, padding=50)
        window.grid()

        ttk.Label(window, text="Creando AFD (LLenar los siguientes campos)").grid(column=0, row=0)

        # Etiqueta y campo de entrada para el Nombre
        ttk.Label(window, text="Nombre:").grid(column=0, row=1)
        entry_nombre = ttk.Entry(window)
        entry_nombre.grid(column=1, row=1)

        # Etiqueta y campo de entrada para los Estados
        ttk.Label(window, text="Estados:").grid(column=0, row=2)
        entry_estados = ttk.Entry(window)
        entry_estados.grid(column=1, row=2)

        # Etiqueta y campo de entrada para el Alfabeto
        ttk.Label(window, text="Alfabeto:").grid(column=0, row=3)
        entry_alfabeto = ttk.Entry(window)
        entry_alfabeto.grid(column=1, row=3)

        # Etiqueta y campo de entrada para el Estado Inicial
        ttk.Label(window, text="Estado Inicial:").grid(column=0, row=4)
        entry_inicial = ttk.Entry(window)
        entry_inicial.grid(column=1, row=4)

        # Etiqueta y campo de entrada para los Estados de Aceptación
        ttk.Label(window, text="Estados de Aceptación:").grid(column=0, row=5)
        entry_aceptados = ttk.Entry(window)
        entry_aceptados.grid(column=1, row=5)

        # Etiqueta y campo de entrada para las Transiciones
        ttk.Label(window, text="Transiciones:").grid(column=0, row=6)
        entry_transiciones = ttk.Entry(window)
        entry_transiciones.grid(column=1, row=6)

        ttk.Button(window, text="Aceptar", command=guardar_datos_afd).grid(column=0, row=7, padx=20, pady=10)
        ttk.Button(window, text="Cerrar", command=create_afn.destroy).grid(column=1, row=7, padx=20, pady=10)

    def evaluar_afd():
        main_afn.destroy()

        main_evaluar = Tk()
        main_evaluar.title("Evaluar Cadena")

        window = ttk.Frame(main_evaluar, padding=50)
        window.grid()

        ttk.Label(window, text="Seleccione una de las siguientes").grid()

        ttk.Button(window, text="Solo Evaluar").grid(pady=10)
        ttk.Button(window, text="Ruta").grid(pady=10)
        ttk.Button(window, text="Cerrar", command=main_evaluar.destroy).grid(pady=10)

    #Ventana que despliega información de un autómata AFN
    def ayuda_afd():

        info_afn = Tk()
        info_afn.title("Ayuda")

        window = ttk.Frame(info_afn, padding=50)
        window.grid()

        info = "Un autómata AFD (Autómata Finito Determinista) es un modelo matemático utilizado en el campo de la teoría de autómatas y lenguajes formales."
        info2 = "Es una variante del autómata finito (AF) que sigue un conjunto de reglas estrictas y deterministas para su funcionamiento."

        ttk.Label(window, text="¿Qué es un Autómata AFD?").grid()
        ttk.Label(window, text=info).grid()
        ttk.Label(window, text=info2).grid()

        ttk.Button(window, text="Cerrar", command=info_afn.destroy).grid(pady=10)

    main_afn = Tk()
    main_afn.title("Menu AFD")

    window = ttk.Frame(main_afn, padding=50)
    window.grid()

    ttk.Label(window, text="Sección: A").grid(column=0, row=0)
    ttk.Label(window, text="Carné: 201901815").grid(column=1, row=0)
    ttk.Label(window, text="Ivan de Jesus Pisquiy Escobar").grid(column=0, row=1)

    ttk.Button(window, text="Crear AFD", command=crear_afd).grid(column=0, row=2, padx=20, pady=10)
    ttk.Button(window, text="Evaluar Cadena", command=evaluar_afd).grid(column=1, row=2, padx=20, pady=10)
    ttk.Button(window, text="Generar Reporte AFD", command=reporte).grid(column=0, row=3, padx=20, pady=10)
    ttk.Button(window, text="Ayuda", command=ayuda_afd).grid(column=1, row=3, padx=20, pady=10)
    ttk.Button(window, text="Cerrar", command=main_afn.destroy).grid(column=0, row=4, padx=20, pady=10)

def menu_oe():

    def minimizar():
        global contenido_texto
        main_oe.destroy
        main_minimizar = Tk()
        main_minimizar.title("OE")

        window = ttk.Frame(window, padding=50)
        window.grid()

        ttk.Label(window, text="Llenar los siguientes campos")

    def ayuda_oe():

        info_afn = Tk()
        info_afn.title("Ayuda")

        window = ttk.Frame(info_afn, padding=50)
        window.grid()

        info = "se refiere a reducir una gramática regular a su forma más simple o compacta."
        info2 = "El objetivo de la minimización es eliminar cualquier redundancia o información innecesaria en la gramática."

        ttk.Label(window, text="¿Qué es un Modulo OE?").grid()
        ttk.Label(window, text=info).grid()
        ttk.Label(window, text=info2).grid()

        ttk.Button(window, text="Cerrar", command=info_afn.destroy).grid(pady=10)

    main_oe = Tk()
    main_oe.title("Menu OE")

    window = ttk.Frame(main_oe, padding=50)
    window.grid()

    ttk.Label(window, text="Elija una opción a continuación").grid(pady=20)
    ttk.Button(window, text="Seleccionar AFD").grid(pady=10)
    ttk.Button(window, text="Generar reporte OE").grid(pady=10)
    ttk.Button(window, text="Ayuda", command=ayuda_oe).grid(pady=10)
    ttk.Button(window, text="Cerrar", command=main_oe.destroy).grid(pady=10)

#Ventana principal
def main_window():
    main = Tk()
    main.title("Gramáticas Regulares")

    window = ttk.Frame(main, padding=50)
    window.grid()

    ttk.Label(window, text="Lenguajes formales y de Programación").grid(column=0, row=0)
    ttk.Label(window, text="Sección: A").grid(column=1, row=0)
    ttk.Label(window, text="Carné: 201901815").grid(column=0, row=1)
    ttk.Label(window, text="Ivan de Jesus Pisquiy Escobar").grid(column=1, row=1)

    ttk.Button(window, text="AFN", command=menu_afn).grid(column=0, row=4, padx=20, pady=10)
    ttk.Button(window, text="AFD", command=menu_afd).grid(column=1, row=4, padx=20, pady=10)
    ttk.Button(window, text="OE", command=menu_oe).grid(column=0, row=5, padx=20, pady=10)
    ttk.Button(window, text="Carga Masiva", command=carga_masiva).grid(column=1, row=5, padx=20, pady=10)
    ttk.Button(window, text="Cerrar", command=main.quit).grid(column=0, row=6, padx=20, pady=10)
    main.mainloop()

main_window()