import PySimpleGUI as sg
import os
import os.path
import pandas as pd
from matplotlib import colors, pyplot as plt


# La Ruta de la carpeta donde estan los archivos csv
path_files = "stats"
path_files2 = "assets"
# La ruta actual y le marco la carpeta donde estan los archivos que quiero acceder
path_arch = os.path.join(os.getcwd(),path_files)
path_arch2 = os.path.join(os.getcwd(),path_files2)



def rank1():
    """ Función que devuelve el raking de usuarios del nivel 1 """

    df_usuarios1 = pd.read_csv(os.path.join(os.getcwd(),path_arch,"eventos.csv"))
    # Me quedo con los usuarios del Nivel 1
    nivel1 = df_usuarios1[df_usuarios1['nivel'] == 'Nivel 1: 4x2']

    # Quito las partidas abandonadas
    abandonados = nivel1[nivel1['estado'] == 'abandonado']
    fila = list(abandonados['partida'])
    nivel1 = nivel1[~nivel1['partida'].isin(fila)]
    
    # Agrupo el usuario con el nivel 1 y cuento sus puntos
    nivel1 = nivel1.groupby(["nick"])["puntaje"].sum()
    # Ordeno la estructura de forma descendiente
    nivel1 = nivel1.sort_values(ascending= False).head(10)
    return nivel1


def rank2():
    """ Función que devuelve el raking de usuarios del nivel 2 """
    df_usuarios2 = pd.read_csv(os.path.join(os.getcwd(),path_arch,"eventos.csv"))
    # Me quedo con los usuarios del Nivel 2
    nivel2 = df_usuarios2[df_usuarios2["nivel"] == "Nivel 2: 4x3"]
    #nivel2 = df_usuarios2[df_usuarios2["nivel"] == "Nivel 2: 4x3"]

    # Quito las partidas abandonadas
    abandonados = nivel2[nivel2['estado'] == 'abandonado']
    fila = list(abandonados['partida'])
    nivel2 = nivel2[~nivel2['partida'].isin(fila)]

    # Agrupo el usuario con el nivel 2 y cuento sus puntos
    nivel2 = nivel2.groupby(["nick"])["puntaje"].sum()
    # Ordeno la estructura de forma descendente
    nivel2 = nivel2.sort_values(ascending= False).head(10)
    return nivel2

def rank3():
    """ Función que devuelve el ranking de usuarios del nivel 3 """
    df_usuarios3 = pd.read_csv(os.path.join(os.getcwd(),path_arch,"eventos.csv"))
    # Me quedo con los usuarios del Nivel 3
    nivel3 = df_usuarios3[df_usuarios3["nivel"] == "Nivel 3: 4x4"]

    # Quito las partidas abandonadas
    abandonados = nivel3[nivel3['estado'] == 'abandonado']
    fila = list(abandonados['partida'])
    nivel3 = nivel3[~nivel3['partida'].isin(fila)]

    #nivel3 = df_usuarios3[df_usuarios3["nivel"] == "Nivel 3: 4x4"]
    # Agrupo el usuario con el nivel 3 y cuento sus puntos
    nivel3 = nivel3.groupby(["nick"])["puntaje"].sum()
    # Ordeno la estructura de forma descendente
    nivel3 = nivel3.sort_values(ascending= False).head(10)
    return nivel3
    


def score():
    """ Función de puntajes del juego """
    # Tamaño de los botones
    tam_button = (8,2)

    # Defino elementos gráficos: Textos, input, botones.
    ranking1 = rank1()
    ranking1 = ranking1.to_string()
    ranking1 = ranking1.replace("nick", " ")
    print()
    ranking2 = rank2()
    ranking2 = ranking2.to_string()
    ranking2 = ranking2.replace("nick", " ")
    print()
    ranking3 = rank3()
    ranking3 = ranking3.to_string()
    ranking3 = ranking3.replace("nick", " ")
    print()


    layout = [
                [sg.Image(os.path.join(os.getcwd(),path_files2,"puntajes.png"), pad = (230,8))],
                [sg.T('')],
                [sg.Text("Ranking nivel 1", size=(15,1)), sg.VerticalSeparator(pad=None), sg.Text("Ranking nivel 2", size=(15,1)), sg.VerticalSeparator(pad=None), sg.Text("Ranking nivel 3", size=(15,1))],
                [sg.Text(ranking1, size=(15,15)), sg.VerticalSeparator(pad=None), sg.Text(ranking2, size=(15,15), visible= True), sg.VerticalSeparator(pad=None), sg.Text(ranking3, size=(15,15), visible= True)],
                [sg.Button('Volver', size = tam_button, key = '-BACK-', pad=((0,0),(20,0)))]
    ]

    # Creo la ventana con el layout definido
    windows = sg.Window('Puntajes', layout, margins=(50,50), element_justification='c')
    while True:
     event,values = windows.read()
     print(f"EVENTO: {event}")
     print(f"VALORES: {values}")
    
     if event == sg.WINDOW_CLOSED or event == '-BACK-':
         break
   
    windows.close()

