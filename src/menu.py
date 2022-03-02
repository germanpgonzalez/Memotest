import PySimpleGUI as sg
from src import configuracion,estadisticas,puntajes,registro, tablero
import os

def start(username):
  """ Función de inicio el juego """
  menu(username)

def menu(username):
 """ Función del menú principal del juego """
 # Tamaño de los botones
 tam_button = (10,2)

 # Defino los elementos gráficos: Textos, input, botones.

 layout = [[sg.Image(os.path.join(os.getcwd(), 'assets', 'memotest.png'))],
   [sg.T('')],
   [sg.T('')],
   [sg.Button('Jugar', size = tam_button, key = '-PLAY-'), 
   sg.Button('Configuración', size = tam_button , key = '-CONFIG-'),
   sg.Button('Puntajes', size = tam_button , key = '-SCORE-'),
   sg.Button('Estadísticas', size = tam_button, key = '-STATISTICS-'),
   sg.Button('Salir', size = tam_button, key = '-EXIT-')]]

 # Creo la ventana con el layout definido
 windows = sg.Window('MemoTest', layout, margins=(30,30), element_justification='c')


 while True:
   # Puedo leer eventos y valores de la ventana
   event, values = windows.read()
   print(f"EVENTO: {event}")
   print(f"VALORES: {values}")

   # El evento por defecto para cerrar la ventana es Salir.
   if event == sg.WINDOW_CLOSED or event == '-EXIT-':
     break

   # El evento de Jugar primero te lleva al registro.
   if event == '-PLAY-':
     #windows.hide()
     tablero.play(username)
   
   # Evento de Configuración.
   if event == '-CONFIG-':
     configuracion.config(username)
   
   # Evento de Puntajes.
   if event == '-SCORE-':
     puntajes.score()
    
   # Evento de Estadísticas.
   if event == '-STATISTICS-':
      estadisticas.statistics()

      

    
 # Cierre de la ventana
 windows.close()

