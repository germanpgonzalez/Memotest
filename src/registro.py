import PySimpleGUI as sg
import json, os
from src import newuser, menu

def users_path():
    return os.path.join(os.getcwd(), 'users', 'users.json')

def start():
    # Tema
    sg.theme('DarkAmber')
    username, exitoso = reg()
    #Si se pudo iniciar sesión, se continúa al menú.
    if exitoso:
        menu.start(username)

def update_reg(dicc):

    """ Actualiza la lista de usuarios """
    try:
        archivo = open(users_path(),'r')
        data = json.load(archivo)
    except FileNotFoundError:
        archivo = open(users_path(),'x')
        data = []   
    finally:
        archivo.close()
        #Reescribo el archivo con los nuevos datos.
        with open(users_path(),'w') as archivo:
            data.append(dicc)
            json.dump(data, archivo, indent = 4)

def check_login(username, password):
    """ Función que checkea si el usuario se encuentra en el archivo de usuarios. """
    ok_username = False
    ok_password = False
    try:
        archivo = open(users_path(),'r')
        data = json.load(archivo)
        archivo.close()
    except FileNotFoundError:
        return ok_password, ok_username
    else:
        #Chequeo si el usuario existe y en el archivo y si la contraseña ingresada es correcta.
        
        for elem in data:
            if username == elem['Nickname']:
                ok_username = True
                ok_password = elem['Password'] == password
                break
        return ok_password, ok_username

def reg():
    """ Función de registro de usuarios """
    # Tamaño de los botones
    tam_button = (8,2)

    # Defino los elementos gráficos: Textos,input, botones.

    layout =    [
                    [sg.Text("Nickname", size = (10, 1)), sg.Input(key = '-NICK-')],
                    [sg.Text("Contraseña", size = (10,1)), sg.Input(key = '-PASS-',password_char='*')],
                    [sg.T('')],
                    [sg.Button('Aceptar', size = tam_button, key = '-ACEPTAR-', bind_return_key=True),
                    sg.Button('Borrar', size = tam_button, key = '-DELETE-'),
                    sg.Button('Cancelar', size = tam_button, key = '-CANCEL-')],
                    [sg.T('\n'*2)],
                    [sg.Text('¿No tienes una cuenta? ¡Registrate!')],
                    [sg.Button('Registrarse', size = tam_button, key = '-NEW_USER-')]
                ]

    # Creo la ventana con el layout definido
    windows = sg.Window('Inicio de Sesión', layout, margins=(20,40))

    username = ''
    exitoso = False
    while True:
        event, values = windows.read()
        print(f"EVENTO: {event}")
        print(f"VALORES: {values}")

    # El evento por defecto para cerrar la ventana es Cancelar.
        if event == sg.WINDOW_CLOSED or event == '-CANCEL-':
            break
        if event == '-DELETE-':
            # Limpio los InputText, al no tener las Keys ya no funciona
            windows.find_element('-NICK-').Update('')
            windows.find_element('-PASS-').Update('')
        if event == '-ACEPTAR-':
            #Checkeo los datos de inicio de sesion
            ok_password, ok_username = check_login(values['-NICK-'], values['-PASS-'])
            if ok_password and ok_username:
                username = values['-NICK-']
                exitoso = True
                break
            elif ok_username: 
                sg.PopupError('Contraseña incorrecta')
            else:
                sg.PopupError('El usuario no se encuentra registrado')
        if event == '-NEW_USER-':
            newuser.new_user()
            
    # Cierre de la ventana
    windows.close()
    return username, exitoso
