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

def validar_cadena(cadena, automata):
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

    # Obtener la información del archivo AFN
    estados = grupos[automata][1].strip().split(',')
    alfabeto = grupos[automata][2].strip().split(',')
    estado_inicial = grupos[automata][3].strip()
    estados_aceptacion = grupos[automata][4].strip().split(',')
    transiciones = grupos[automata][5:]
    for transicion in transiciones:
            fase = transicion.split(';')
            inicial = fase[0].split(',')

    # Función recursiva para realizar la validación
    def validar_rec(estado_actual, subcadena):
        # Caso base: no quedan símbolos en la subcadena
        if len(subcadena) == 0:
            # Verificar si el estado actual es un estado de aceptación
            if estado_actual in estados_aceptacion:
                return messagebox.showinfo("¡Éxito!", "La cadena ingresada es válida")
            else:
                return messagebox.showinfo("¡Lo siento!", "La cadena ingresada no es válida")

        # Caso recursivo: buscar transiciones para el símbolo actual
        simbolo_actual = subcadena[0]
        subcadena_restante = subcadena[1:]
        for transicion in transiciones:
            fase = transicion.split(';')
            inicial = fase[0].split(',')
            estado_origen = inicial[0]
            simbolo = inicial[1]
            estado_destino = fase[1]
            if estado_origen == estado_actual and simbolo == simbolo_actual:
                # Realizar transición y continuar con la validación recursiva
                if validar_rec(estado_destino, subcadena_restante):
                    return messagebox.showinfo("¡Éxito!", "La cadena ingresada es válida")

        # No se encontró ninguna transición válida para el símbolo actual
        return messagebox.showinfo("¡Lo siento!", "La cadena ingresada no es válida")

    # Iniciar la validación recursiva desde el estado inicial
    return validar_rec(estado_inicial, cadena)

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
        grafica.graph_attr['size'] = '5,4'
        conexiones = {}
        
        for j in range(len(estados)):
            grafica.node(estados[j], color='red')
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
    combobox.current(0)
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

        def sub_evaluar():
            cadena = entry_cadena.get()
            automata = combobox.current()

            def validar_cadena_aux():
                validar_cadena(cadena, automata)

            main_evaluar = Tk()
            main_evaluar.title("Evaluar Cadena")

            window = ttk.Frame(main_evaluar, padding=50)
            window.grid()

            ttk.Label(window, text="Seleccione una de las siguientes").grid()

            ttk.Button(window, text="Solo Evaluar", command=validar_cadena_aux).grid(pady=10)
            ttk.Button(window, text="Ruta").grid(pady=10)
            ttk.Button(window, text="Cerrar", command=main_evaluar.destroy).grid(pady=10)
            cadena_afn.destroy()

        cadena_afn = Tk()
        cadena_afn.title("Evaluar AFN")

        window = ttk.Frame(cadena_afn, padding=50)
        window.grid()

        ttk.Label(window, text="Ingrese una cadena a evaluar").grid()

        combobox = ttk.Combobox(window, values=nombres)
        combobox.current(0)
        combobox.grid()

        # Etiqueta y campo de entrada para el Nombre
        ttk.Label(window, text="Cadena").grid()
        entry_cadena = ttk.Entry(window)
        entry_cadena.grid()

        ttk.Button(window, text="Siguiente", command=sub_evaluar).grid()
        

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

        def sub_evaluar():
            cadena = entry_cadena.get()
            automata = combobox.current()

            def validar_cadena_aux():
                validar_cadena(cadena, automata)

            main_evaluar = Tk()
            main_evaluar.title("Evaluar Cadena")

            window = ttk.Frame(main_evaluar, padding=50)
            window.grid()

            ttk.Label(window, text="Seleccione una de las siguientes").grid()

            ttk.Button(window, text="Solo Evaluar", command=validar_cadena_aux).grid(pady=10)
            ttk.Button(window, text="Ruta").grid(pady=10)
            ttk.Button(window, text="Cerrar", command=main_evaluar.destroy).grid(pady=10)
            cadena_afn.destroy()

        cadena_afn = Tk()
        cadena_afn.title("Evaluar AFD")

        window = ttk.Frame(cadena_afn, padding=50)
        window.grid()

        ttk.Label(window, text="Ingrese una cadena a evaluar").grid()

        combobox = ttk.Combobox(window, values=nombres)
        combobox.current(0)
        combobox.grid()

        # Etiqueta y campo de entrada para el Nombre
        ttk.Label(window, text="Cadena").grid()
        entry_cadena = ttk.Entry(window)
        entry_cadena.grid()

        ttk.Button(window, text="Siguiente", command=sub_evaluar).grid()

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

        def minimizar_afd():

            automata = combobox.current()

            nombre_optimizado = entry_nombre.get()
            nombre = grupos[automata][0]
            estados = grupos[automata][1].split(',')
            alfabeto = grupos[automata][2].split(',')
            estado_inicial = grupos[automata][3]
            estados_aceptacion = grupos[automata][4]
            transiciones = grupos[automata][5:]

            main_minimizar.destroy()

            # Paso 1: Encontrar estados equivalentes
            grupos_equivalentes = []
            estados_no_aceptacion = [estado for estado in estados if estado not in estados_aceptacion]
            grupos_equivalentes.append(estados_aceptacion)
            grupos_equivalentes.append(estados_no_aceptacion)

            estados_equivalentes_actualizados = True
            while estados_equivalentes_actualizados:
                nuevos_grupos_equivalentes = []
                for grupo in grupos_equivalentes:
                    nuevos_grupos = []
                    for estado in grupo:
                        encontrado = False
                        for nuevo_grupo in nuevos_grupos:
                            # Verificar si el estado es equivalente a algún estado del nuevo grupo
                            if all(transiciones[estado][i] == transiciones[nuevo_grupo[0]][i] for i in range(len(alfabeto))):
                                encontrado = True
                                nuevo_grupo.append(estado)
                                break
                        if not encontrado:
                            nuevos_grupos.append([estado])
                    nuevos_grupos_equivalentes.extend(nuevos_grupos)
                if len(nuevos_grupos_equivalentes) == len(grupos_equivalentes):
                    estados_equivalentes_actualizados = False
                grupos_equivalentes = nuevos_grupos_equivalentes

            # Paso 2: Anular estados equivalentes y actualizar la tabla de transiciones
            estados_minimizados = []
            transiciones_minimizadas = {}
            for grupo in grupos_equivalentes:
                estado_minimizado = grupo[0]
                estados_minimizados.append(estado_minimizado)
                for estado in grupo[1:]:
                    transiciones_minimizadas[estado] = estado_minimizado

            # Paso 3: Actualizar los estados de aceptación y la tabla de transiciones
            estados_aceptacion_minimizados = [estado for estado in estados_aceptacion if estado in estados_minimizados]
            estado_inicial_minimizado = transiciones_minimizadas[estado_inicial] if estado_inicial in transiciones_minimizadas else None
            for estado_origen, transiciones_origen in transiciones.items():
                transiciones_minimizadas[estado_origen] = {simbolo: transiciones_minimizadas.get(estado_destino) for simbolo, estado_destino in transiciones_origen.items()}

            contenido = f"{nombre_optimizado}\n"
            contenido += f"{estados_minimizados}\n"
            contenido += f"{alfabeto}\n"
            contenido += f"{estado_inicial_minimizado}\n"
            contenido += f"{estados_aceptacion_minimizados}\n"
            for transicion in transiciones_minimizadas:
                contenido += f"{transicion}\n"

            nombre_archivo = f"{nombre_optimizado}.afd"

            file = open(nombre_archivo, 'w')
            file.write(contenido)
            file.close()
        
        main_minimizar = Tk()
        main_minimizar.title("OE")

        window = ttk.Frame(main_minimizar, padding=50)
        window.grid()

        ttk.Label(window, text="Llenar los siguientes campos")

        combobox = ttk.Combobox(window, values=nombres)
        combobox.current(0)
        combobox.grid()

        # Etiqueta y campo de entrada para el Nombre
        ttk.Label(window, text="Nombre").grid()
        entry_nombre = ttk.Entry(window)
        entry_nombre.grid()

        ttk.Button(window, text="Optimizar", command=minimizar_afd).grid()

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
    ttk.Button(window, text="Seleccionar AFD", command=minimizar).grid(pady=10)
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