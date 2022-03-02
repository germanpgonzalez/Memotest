from json import decoder
import PySimpleGUI as sg
import json, os
from PySimpleGUI.PySimpleGUI import DecodeRadioRowCol

def config_path():
    return os.path.join(os.getcwd(), 'config', 'config.json')

def default_values():  
    """ Definicióon de diccionario de configuración con valores predeterminados."""

    dicc =      {'-CASILLAS-': 'Nivel 1: 4x2',
                '-ELEMENTOS-': 'Palabras',
                '-S_AYUDAS-': True,
                '-C_AYUDAS-': False,
                '-TIEMPO-': 15,
                '-COINCIDENCIAS-': '2',
                '-COLORES-': 'Marrón y Amarillo',
                '-T_VICTORIA-': '¡Ganaste!',
                '-T_DERROTA-': '¡Perdiste!',
                '-T_TIEMPO-': '¡Queda poco tiempo!'}
    return dicc

def default_config(username):
    """ Creación de configuraciones con valores predeterminados para nuevos usuarios. """

    #Leo el archivo, en caso de no existir, lo creo.
    try:
        archivo = open(config_path(),'r')
        data = json.load(archivo)
    except FileNotFoundError:
        archivo = open(config_path(),'x')
        data = []   
    finally:
        archivo.close()

        #Reescribo el archivo con los nuevos datos.
        with open(config_path(),'w') as archivo:
            data.append({username:default_values()})
            json.dump(data, archivo, ensure_ascii= False)

def config_update(username, values):
    """ Actualización de la configuración del usuario. """

    archivo = open(config_path(),'r')
    data = json.load(archivo)
    archivo.close()

    #Busco la clave que coincida con el nombre del usuario.
    for elem in data:
        if username in elem:
            #Asigno la nueva configuración al usuario.
            elem[username] = values
            break
    
    #Actualizo el archivo.
    with open(config_path(),'w') as archivo:
            json.dump(data, archivo, ensure_ascii =False, indent = 4)

def get_actual_config(username):
    """ Función para obtener los valores de configuración actual de un usuario """
    archivo = open(config_path(),'r')
    data = json.load(archivo)
    archivo.close()

    for elem in data:
        if username in elem:
            dicc = elem[username]
            break
    return dicc

def config(username):
    """ Función de configuración del juego """
    # Tamaño de los botones
    tam_button = (11,2)

    #Obtengo la configuración actual del usuario.
    dicc = get_actual_config(username)

    # Defino elementos gráficos: Textos, input, botones.
    im_path = os.path.join(os.getcwd(), 'assets', 'configs')

    layout = [
        [sg.Image(os.path.join(im_path, 'Configuraciones.png'), pad=((172,0),(6,6)))],
        [sg.T('')],
        [sg.Image(os.path.join(im_path, 'Casillas.png'), pad=((0,148),(0,0))),sg.Image(os.path.join(im_path, 'Elementos.png')), sg.Image(os.path.join(im_path, 'Ayudas.png'), pad=((153,0),(0,0)))],
        [sg.Combo(['Nivel 1: 4x2', 'Nivel 2: 4x3','Nivel 3: 4x4'], default_value=dicc['-CASILLAS-'], pad=((6,143),(0,0)), size=(11,5), key='-CASILLAS-'),sg.Combo(['Palabras', 'Imágenes'], default_value=dicc['-ELEMENTOS-'], pad= (0,5), size=(16,5), key='-ELEMENTOS-'),sg.Radio('Sin ayudas', "RADIO1", key= '-S_AYUDAS-', default=dicc['-S_AYUDAS-'], pad=((150,0),(0,0)))],
        [sg.Radio('Con ayudas', "RADIO1",default=dicc['-C_AYUDAS-'], key='-C_AYUDAS-', pad=((522,0),(0,0)))],

        [sg.T('\n'*3)],
        [sg.Image(os.path.join(im_path, 'Tiempo.png'), pad=((0,137),(0,0))), sg.Image(os.path.join(im_path, 'Coincidencias.png')), sg.Image(os.path.join(im_path, 'Tema.png'), pad=((153,0),(0,0)))],
        [sg.Slider(range=(1,3), default_value=dicc['-TIEMPO-'], size=(8,15), orientation='horizontal',font=('Helvetica', 12), key= '-TIEMPO-', pad=((6,165),(0,0))),sg.Combo(['2','4'], default_value=dicc['-COINCIDENCIAS-'], size=(11,5), key='-COINCIDENCIAS-', pad=((0,0),(17,0))) , sg.Combo(['Marrón y Amarillo', 'Verde y Amarillo','Negro y Naranja'], default_value=dicc['-COLORES-'], size=(11,5), key='-COLORES-', pad=((178,0),(17,0)))],

        [sg.T('\n'*3)],
        [sg.Image(os.path.join(im_path, 'Mensajes.png'), pad=((0,0),(2,10)))],
        [sg.Text('Mesaje de victoria '),sg.InputText(dicc['-T_VICTORIA-'], size=(51,1), font=('Helvetica', 12), key='-T_VICTORIA-')],
        [sg.Text('Mesaje de derrota '),sg.InputText(dicc['-T_DERROTA-'], size=(51,1), font=('Helvetica', 12), key='-T_DERROTA-')],
        [sg.Text('Mesaje de tiempo '),sg.InputText(dicc['-T_TIEMPO-'], size=(51,1), font=('Helvetica', 12), key='-T_TIEMPO-')],

        [sg.T('')],
        [sg.Button('Aplicar', size = tam_button, key = '-APPLY-', pad=(3,8)), sg.Button('Acerda de la ayuda', size = tam_button, key = '-HELP-', pad=(3,8))]
        ]

    # Creo la ventana con el layout definido
    windows = sg.Window('Configuración', layout, margins= (60,36))
    while True:
        event,values = windows.read()

        if event == sg.WIN_CLOSED:
            break
        if event == '-APPLY-':
            #Actualiza la configuración del usuario.
            config_update(username, values)
            break
        if event == '-HELP-':
            sg.popup('La ayuda en el juego consistirá de un botón que se podrá presionar al pasar al menos 50 segundos de juego y que restará 10 segundos al contador.', title='Acerca de la ayuda')
    windows.close()