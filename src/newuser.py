import PySimpleGUI as sg
from src import registro, menu, configuracion
from src import *
import json

def check_users(username):
    """ Checkea si el usuario ya se encuentra registrado. """
    
    try:
        archivo = open(registro.users_path(),'r')
        data = json.load(archivo)
        archivo.close()
    except FileNotFoundError:
        return False
    else:
        #Chequeo si el usuario existe y en el archivo.
        ok = False
        for elem in data:
            if username == elem['Nickname']:
                ok = True
                break
        return ok

def check_data(values):
    print(values)
    ok = len(values['-NICK-']) >= 5 and len(values['-PASSWORD-']) >= 6 
    if isinstance(values['-EDAD-'], str):
        ok = False
    return ok

def new_user():
    # Tamaño de los botones
    tam_button = (8,2)

    # Defino los elementos gráficos: Textos, input, botones.

    layout = [
        [sg.Text("Nickname", size = (20,1)), sg.Input(key = '-NICK-')],
        [sg.Text("El usuario debe contener mínimo 5 caracteres", pad=((177,0),(0,0)))],
        [sg.Text("Contraseña", size = (20,1)), sg.Input(key = '-PASSWORD-', password_char='*')],
        [sg.Text("La contraseña debe contener mínimo 6 caracteres", pad=((177,0),(0,0)))],
        [sg.Text("Vuelva a ingresar su contraseña", size = (20,0)), sg.Input(key = '-PASSWORD2-',password_char='*')],
        [sg.Text("Edad", size = (20,1)), sg.Spin([i for i in range(1,110)], initial_value=0,size= (3,3), key = '-EDAD-')],
        [sg.Text("Género", size = (20,1)), sg.Combo(['Masculino', 'Femenino', 'Otro'], key = '-GENERO-')],
        [sg.T('')],
        [sg.Button('Aceptar', size = tam_button, key = '-ACEPTAR-'),
        sg.Button('Borrar', size = tam_button, key = '-BORRAR-'),
        sg.Button('Volver', size = tam_button, key = '-VOLVER-')]
    ]
        
    # Creo la ventana con el layout definido
    windows = sg.Window('Registro', layout, margins=(20,20))
     
    while True:
        # Puedo leer eventos y valores de la ventana
        event, values = windows.read()
        print(f"EVENTO: {event}")
        print(f"VALORES: {values}")

    # El evento por defecto para cerrar la ventana es Volver
        if event == sg.WIN_CLOSED or event == '-VOLVER-':
             break
        if event == '-ACEPTAR-':
            repetido = check_users(values['-NICK-'])
            if not repetido:
                if values['-PASSWORD-'] == values['-PASSWORD2-']:
                    if check_data(values):
                        sg.popup('¡Registro Existoso!')

                        #Actualizo la lista de usuarios.
                        nuevo_usuario = ({"Nickname": values['-NICK-'], "Password": values['-PASSWORD-'], "Edad": values['-EDAD-'], "Genero": values['-GENERO-'] })
                        registro.update_reg(nuevo_usuario)
                
                        #Asigno la configuración inicial al usuario.
                        configuracion.default_config(values['-NICK-'])
                        break
                    else:
                        sg.PopupError('Algo salió mal. Verifique los datos ingresados.')
                else:
                    sg.PopupError('¡Las contraseñas no coinciden!')
            else:
                sg.popup('El nombre de usuario ya está en uso')
        if event =='-BORRAR-':
            windows.find_element('-NICK-').Update('')
            windows.find_element('-PASSWORD-').Update('')
            windows.find_element('-EDAD-').Update('')
          


    # Cierre de la ventana
    windows.close()
