import time, json, os, random, csv
import PySimpleGUI as sg
import pandas as pd
from PySimpleGUI.PySimpleGUI import TimerStop, timer_stop
from src import criterios

# La Ruta de la carpeta donde estan las imagenes
path_files = "datasets"
path_files2 = "assets"
# La ruta actual y le marco la carpeta donde estan los archivos que quiero acceder
path_arch = os.path.join(os.getcwd(),path_files, "pokemon")
path_arch2 = os.path.join(os.getcwd(), path_files2)

pokebola = "pokebola.png"

def load_config(username):
    """ Carga de la configuración del usuario. """

    #Utilizo el módulo "os" para obtener el path del archivo de las configuraciones.
    archivo = open(os.path.join(os.getcwd(), 'config', 'config.json'),'r')
    data = json.load(archivo)

    #Busco la clave que coincida con el nombre del usuario.
    for elem in data:
        if username in elem:
            data = elem[username]
            break
    return data

def elementos_tablero(tablero_size, button_color, b_color, username, cant, button_text, nivel):
    """ Definición de la estructura de la ventana. """
    layout =    [
                    [sg.Text(f'Usuario: {username}', font=('Helvetica', 12), background_color= b_color)],
                    [sg.Text(nivel, font=('Helvetica', 8), pad=((0,0),(0,10)))],
                    [sg.Button('Iniciar',size=(10,1), key='-PLAY-', button_color=button_color)],
                    [sg.Text('',size=(10, 1), key='-MENSAJE_TIEMPO-', font=('Helvetica', 10), background_color= b_color)],
                    [sg.Text('00:00:00',size=(10, 1), pad=((0,0),(0, 10)),font=('Helvetica', 20), key='-TIMER-', background_color= b_color, justification='center')],
                    [[sg.Button(pad=(0,0), size= (6,2), key=f'Cell-{index2}-{index}', button_color=button_color,image_filename=(os.path.join(os.getcwd(),path_files2,pokebola))) for index in range(tablero_size)] for index2 in range(4)],
                    [sg.Text('Elementos encontrados: '), sg.Text(f'0/{cant}', key='-CANT_ELEM-')],
                    [sg.Button(button_text, key='-HELP-')],
                    [sg.Button('Cancelar', size = (10,1), pad=((0,1),(60,30)), key = '-CANCEL-' , button_color=button_color),
                    sg.Button('Volver', size = (10,1), pad=((1,0),(60,30)), key = '-BACK-' , button_color=button_color)]
                    
                ]

    return layout

def time_as_int():
    return int(round(time.time()* 100))

def play(username):
    """ Creación y control de la ventana del tablero. """

    def obtain_personal_data(username):
        with open(os.path.join(os.getcwd(), 'users', 'users.json'),'r', encoding='utf-8') as file:
            data = json.load(file)
            for elem in data:
                if elem['Nickname'] == username:
                    return elem['Edad'], elem['Genero']  

    def checkear_jugada(data, window, jugada, coincidencias):
        print(data)
        
        if data not in jugada:
            jugada.append(data)
            if len(jugada) != 1:
                if jugada[-2][2] == jugada[-1][2]: 
                    if len(jugada) == coincidencias:
                        for x, y, _elem in jugada:
                            window[f'Cell-{x}-{y}'].update(disabled=sg.BUTTON_DISABLED_MEANS_IGNORE)
                        return True, True
                else:
                    return True, False
        return False, True

    def guardar_eventos(datos):
        """ Guarda en un cvs los eventos del usuario """

        # Recibo una lista de eventos del usuario y la agrego por fila al archivo csv.
        try:
            # Verifico si el archivo csv existe
            file = open(os.path.join(os.getcwd(),'stats',"eventos.csv"), 'r+', newline='', encoding= 'utf-8')
            print("El archivo existe")
        except FileNotFoundError:
            # Si no existe creo el archivo csv con la cabecera
            encabezado = ['tiempo', 'partida', 'cant_palabras', 'evento', 'nick', 'genero', 'edad', 'estado', 'palabra', 'nivel','puntaje']
            with open(os.path.join(os.getcwd(),'stats',"eventos.csv"), 'w', newline= '', encoding= 'utf-8') as file:
                writer = csv.writer(file, delimiter = ',')
                # De esta forma agrego en una misma fila los datos de los eventos del usuario.
                writer.writerow(encabezado)
                writer.writerow(datos)
        else:
            # Si el archivo csv existe guardo información en él.
            file.seek(0,2)
            writer = csv.writer(file, delimiter = ',')
            print('GUARDANDO')
            writer.writerow(datos)
            file.close()


    def numero_partida():
        try:
            data = pd.read_csv(os.path.join(os.getcwd(),'stats',"eventos.csv"), encoding='utf-8')
            print('Listo')
            return int(data['partida'][len(data)-1])+1
        except:
            print('No listo')
            return 1

    def get_board_data(coincidencias, tipo_elementos, tamaño):
        """ Función que genera una lista con los elementos a incluir al tablero según el tipo de tablero. """
         
        poke, path_images_board = criterios.select_criteria(tipo_elementos)
        # El método shuffle me desordenada la lista poke, asi las imagenes estan en forma aleatoria
        random.shuffle(poke)
        # Calculo la cantidad de imágenes/palabras necesarias.
        cant = (int(tamaño) * 4) // coincidencias
        # De esta forma me quedo sólo con "cant" imagenes/palabras de la lista y la duplico para sus coincidencias
        poke = poke[0:cant] * coincidencias

        return poke, path_images_board, cant

    def generate_image_board(window, start_time, wasted_time, total_jugadas, jugada, espera, username, partida, genero, edad, nivel, cant, ayudas):
        bonus_time = 0
        while True:
            event, _values = window.read(timeout=10)
            if event == '-HELP-':
                if ayudas and (((current_time // 100) % 60) >= 50):
                    window['-HELP-'].update('Ayuda utilizada')
                    window['-HELP-'].update(disabled=sg.BUTTON_DISABLED_MEANS_IGNORE)
                    bonus_time = 1000
            if not espera:
                current_time = (time_as_int() - start_time) - wasted_time - bonus_time
                if ((current_time //100) // 60) != int(data['-TIEMPO-']):
                    window['-TIMER-'].update('{:02d}:{:02d}:{:02d}'.format((current_time // 100) // 60 , (current_time // 100) % 60, current_time % 100))

                    if ((int(data['-TIEMPO-'])) - ((current_time // 100) // 60)) < 1:
                        window['-MENSAJE_TIEMPO-'].update(data['-T_TIEMPO-'])

                    if event == sg.WIN_CLOSED or event == '-CANCEL-':
                        if total_jugadas != cant:
                             guardar_eventos([(current_time *10),partida,cant,'fin', username, genero, edad, 'abandonado', '', nivel,10])
                        break
                    if event.startswith('Cell'):
                        prefix, x, y = event.split("-")
                        print(f"Celda: {x},{y}")
                        print()
                        window[event].update(image_filename = (os.path.join(path_images_board, tablero_logico[int(x)][int(y)])))
                        jugada_terminada, correcta = checkear_jugada((x, y, tablero_logico[int(x)][int(y)]), window, jugada, coincidencias)
                        print(jugada)
                        if jugada_terminada:
                            if correcta:
                                # Guardo el evento de la jugada correcta.
                                guardar_eventos([(current_time *10),partida,cant,'intento', username, genero, edad, 'ok', jugada[0][2], nivel,5])
                                jugada = []
                                total_jugadas+=1
                                window['-CANT_ELEM-'].update(f'{total_jugadas}/{cant}')
                                if total_jugadas == cant:
                                    sg.popup(data['-T_VICTORIA-'])
                                    # Guardo el evento de victoria.
                                    guardar_eventos([(current_time *10),partida,cant,'fin', username, genero, edad, 'victoria', '', nivel,10])
                                    break
                            else:
                                # Guardo el evento de la jugada incorrecta.
                                guardar_eventos([(current_time *10),partida,cant,'intento', username, genero, edad, 'error', jugada[0][2], nivel,0])
                                espera = True
                                seconds = 0
                                start_second = time_as_int()
                else:
                    sg.popup(data['-T_DERROTA-'])
                    # Guardo el evento de timeout.
                    guardar_eventos([(current_time *10),partida,cant,'fin', username, genero, edad, 'timeout', '', nivel,0])
                    break

            else:
                if ((seconds //100) % 60) < 1:
                    seconds = time_as_int() - start_second
                else:
                    espera = False
                    for x, y, _elem in jugada:
                        window[f'Cell-{x}-{y}'].update(image_filename = (os.path.join(os.getcwd(),path_files2,pokebola)))
                    jugada = []
                    wasted_time = wasted_time + time_as_int() - start_second

    def generate_word_board(window, start_time, wasted_time, total_jugadas, jugada, espera, username, partida, genero, edad, nivel, cant, ayudas):
        bonus_time = 0
        while True:
            event, _values = window.read(timeout=10)

            if event == '-HELP-':
                if ayudas and (((current_time // 100) % 60) >= 50):
                    window['-HELP-'].update('Ayuda utilizada')
                    window['-HELP-'].update(disabled=sg.BUTTON_DISABLED_MEANS_IGNORE)
                    bonus_time = 1000

            if not espera:
                current_time = (time_as_int() - start_time) - wasted_time
                if ((current_time //100) // 60) != int(data['-TIEMPO-']):
                    window['-TIMER-'].update('{:02d}:{:02d}:{:02d}'.format((current_time // 100) // 60 , (current_time // 100) % 60, current_time % 100))
                    
                    if ((int(data['-TIEMPO-'])) - ((current_time // 100) // 60)) < 1:
                        window['-MENSAJE_TIEMPO-'].update(data['-T_TIEMPO-'])
                    
                    if event == sg.WIN_CLOSED or event == '-CANCEL-':
                        if total_jugadas != cant:
                             guardar_eventos([(current_time *10),partida,cant,'fin', username, genero, edad, 'abandonado', '', nivel,10])
                        break
                    if event.startswith('Cell'):
                        prefix, x, y = event.split("-")
                        print(f"Celda: {x},{y}")
                        print()
                        window[event].update(image_filename= os.path.join(os.getcwd(), 'assets', 'casilla_vacía.png'))
                        window[event].update(tablero_logico[int(x)][int(y)])
                        jugada_terminada, correcta = checkear_jugada((x, y, tablero_logico[int(x)][int(y)]), window, jugada, coincidencias)
                        print(jugada)
                        if jugada_terminada:
                            if correcta:
                                # Guardo el evento de la jugada correcta.
                                guardar_eventos([(current_time *10),partida,cant,'intento', username, genero, edad, 'ok', jugada[0][2], nivel,5])
                                jugada = []
                                total_jugadas+=1
                                window['-CANT_ELEM-'].update(f'{total_jugadas}/{cant}')
                                if total_jugadas == cant:
                                    sg.popup(data['-T_VICTORIA-'])
                                    # Guardo el evento de victoria.
                                    guardar_eventos([(current_time *10),partida,cant,'fin', username, genero, edad, 'victoria', '', nivel,10])
                                    break
                            else:
                                # Guardo el evento de la jugada incorrecta.
                                guardar_eventos([(current_time *10),partida,cant,'intento', username, genero, edad, 'error', jugada[0][2], nivel,0])
                                espera = True
                                seconds = 0
                                start_second = time_as_int()
                else:
                    sg.popup(data['-T_DERROTA-'])
                    # Guardo el evento de timeout.
                    guardar_eventos([(current_time *10),partida,cant,'fin', username, genero, edad, 'timeout', '', nivel,0])
                    break
            else:
                if ((seconds //100) % 60) < 1:
                    seconds = time_as_int() - start_second
                else:
                    espera = False
                    for x, y, _elem in jugada:
                        window[f'Cell-{x}-{y}'].update('')
                        window[f'Cell-{x}-{y}'].update(image_filename = (os.path.join(os.getcwd(),path_files2,pokebola)))
                    jugada = []
                    wasted_time = wasted_time + time_as_int() - start_second

    #Cargo la configuración del usuario.
    data = load_config(username)

    #Obtengo el tamaño del tablero y lo envío al layout.
    tamaño = data['-CASILLAS-'][data['-CASILLAS-'].find('x')+1:]
    
    #Verifico el color elegido.
    if data['-COLORES-'] == 'Marrón y Amarillo':
        colors = {'-COLOR1-': '#2C2825', '-COLOR2-':'#FDCB52'}

    elif data['-COLORES-'] == 'Verde y Amarillo':
        colors = {'-COLOR1-': '#009900', '-COLOR2-': '#CCCC00'}

    else:
        colors = {'-COLOR1-': '#000000' , '-COLOR2-': '#FF8000'}

    # Checkeo si la ayuda está habilitada
    if data['-C_AYUDAS-']:
        ayudas = True
        button_text = 'Bonus de tiempo'
    else:
        ayudas = False
        button_text = 'Ayudas desactivadas'

    # Obtengo los elementos a incluir al tablero.
    tipo_elementos = data['-ELEMENTOS-']
    coincidencias = int(data['-COINCIDENCIAS-'])
    poke, path_images_board, cant = get_board_data(coincidencias, tipo_elementos, tamaño)    
    
    # Creo que tablero lógico
    tamaño_alto = 4
    tamaño_largo = int(tamaño)

    tablero_logico = []

    for index in range(tamaño_alto):
        columna = []
        for index_col in range(tamaño_largo):
            index_elemento = random.randrange(len(poke))
            columna.append(poke[index_elemento])
            poke.pop(index_elemento)
        tablero_logico.append(columna)

    #-COLOR1-: Color del tablero.
    #-COLOR2-: Color de los botones.
    layout = elementos_tablero(int(tamaño), colors['-COLOR2-'], colors['-COLOR1-'], username, cant, button_text, data['-CASILLAS-'])


    espera = False
    window = sg.Window('Mem_py', layout, margins=(50,50), element_justification='center', background_color= colors['-COLOR1-'],disable_close= True)
    while True:
        event, values = window.read()
        
        if event == '-PLAY-':
            window['-PLAY-'].update(visible=False)
            start_time = time_as_int()
            total_jugadas = 0
            jugada = []
            wasted_time = 0
            edad, genero = obtain_personal_data(username)
            #Obtengo el número de la partida actual.
            partida = numero_partida()
            #Guardo el evento "inicio_partida".
            guardar_eventos([0,partida,cant,'inicio_partida', username, genero, edad, '', '', data['-CASILLAS-'],0])
            if tipo_elementos == 'Imágenes':
                generate_image_board(window, start_time, wasted_time, total_jugadas, jugada, espera, username, partida, genero, edad, data['-CASILLAS-'], cant, ayudas)
            else:
                generate_word_board(window, start_time, wasted_time, total_jugadas, jugada, espera, username, partida, genero, edad, data['-CASILLAS-'], cant, ayudas)

        if event == sg.WIN_CLOSED or event == '-BACK-':
            break
    window.close()