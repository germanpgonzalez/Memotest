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

def stats_genero():
    """"" Función que devuelve el porcentaje de victorias por género """

    # Abro y leo el csv con información de usuarios
    df_usuarios = pd.read_csv(os.path.join(os.getcwd(),path_arch,"eventos.csv"))
    # CREA EL GRAFICO DE PARTIDAS FINALIZADAS SEGUN EL GENERO
    genero = df_usuarios[df_usuarios["evento"] == "fin"] ["genero"].value_counts()
    etiquetas = genero.keys()
    
    plt.pie(genero, explode= None, autopct= '%1.1f%%', shadow= False, startangle= 90, labeldistance= 1.1)
    plt.axis('equal')
    plt.legend(etiquetas)
    plt.title("Cantidad de partidas finalizadas por género")
    # Cambio el tamaño de la imagen
    fig = plt.gcf()
    fig.set_size_inches(4,2)
    plt.savefig(os.path.join(os.getcwd(),path_arch, "genero.png"))
    # Borro caché
    plt.clf()

def stats_estado():
    """"" Función que muestra el porcentaje de partidas por estado (terminada, cancelada, abandonadas) """

    # Abro y leo el csv con información de usuarios
    df_estado = pd.read_csv(os.path.join(os.getcwd(),path_arch,"eventos.csv"))
    # CREA EL GRAFICO DE PARTIDAS POR ESTADO
    partida = df_estado["estado"].value_counts()
    etiquetas = partida.keys()
    colores = ["#EE6055","#60D394","#AAF683","#FFD97D","#e84393"]

    plt.pie(partida, explode= None, autopct= '%1.1f%%', shadow= False, startangle= 90, labeldistance= 1.1, colors = colores)
    plt.axis('equal')
    plt.legend(etiquetas)
    plt.title("Porcentaje de partidas por estado")
    # Le agrego un circulo blanco para transformarlo en una dona
    my_circle=plt.Circle( (0,0), 0.5, color='white')
    p=plt.gcf()
    p.gca().add_artist(my_circle)
    # Cambio el tamaño de la imagen
    fig = plt.gcf()
    fig.set_size_inches(4,2)
    plt.savefig(os.path.join(os.getcwd(),path_arch, "estado.png"))
    # Borro caché
    plt.clf()

def top10():
    """ Función que devuelve una lista con las primeras 10 palabras que se encuentan primero en todas las partidas """

    # Abro y leo el csv con información de usuarios
    df_estado = pd.read_csv(os.path.join(os.getcwd(),path_arch,"eventos.csv"))
    
    # Me quedo con el máximo de partidas para utilizar de índice.
    indice = df_estado[df_estado["estado"] == "ok"].tail(1)['partida'].iloc[0]

    partida = 1
    bandera = True
    lista = []
    if indice >= 10:
        max = 10
    else:
        max = indice
    while True:
        top10 = df_estado[(df_estado["partida"] == partida) & (df_estado["estado"] == "ok")]["palabra"].to_list()
        
        # Si la lista no está vacía agrego a la lista
        if len(top10) >= 1:
            lista.append(top10[0])
        
        elif (max+1) <= indice:
            max+=1
        partida += 1
            
        if partida > max:
            bandera = False
            break
    return lista


def statistics():
    """ Función de estadísticas del juego """
    # Tamaño de los botones
    tam_button = (8,2)

    # Defino elementos gráficos: Textos, input, botones.
    stats_genero()
    stats_estado()
    lista = top10()
    layout = [[sg.Image(os.path.join(os.getcwd(),path_files2,"estadisticas.png"), pad = (230,8))],
    [sg.T('')],
    [sg.Image(os.path.join(os.getcwd(), path_files, 'genero.png'))],
    [sg.T('')],
    [sg.Image(os.path.join(os.getcwd(), path_files, 'estado.png'))],
    [sg.T('')],
    [sg.Text(" Top 10 de palabras ")],
    [sg.T('')],
    [sg.Multiline(default_text= top10(), size=(35, 3))],
    [sg.Button('Volver', size = tam_button, key = '-BACK-')]]

    # Creo la ventana con el layout definido
    windows = sg.Window('Estadísticas', layout, margins=(30,30), element_justification='c')

    while True:
     event,values = windows.read()
     print(f"EVENTO: {event}")
     print(f"VALORES: {values}")
    
     if event == sg.WINDOW_CLOSED or event == '-BACK-':
         break
   
    windows.close()

