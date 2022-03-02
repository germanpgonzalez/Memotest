import csv, os, datetime
import pandas as pd
import PySimpleGUI as sg

# Ruta de la carpeta donde estan los datasets
path_files = "datasets"
# La ruta actual y le marco la carpeta donde estan los archivos que quiero acceder
path_arch = os.path.join(os.getcwd(), path_files)


def pokemon_data(tipo):
    """ Función que devuelve 10 nombres de pokemones de agua """
    try:
        archivo_pokemon = open(os.path.join(path_arch, "pokemon.csv"), 'r', encoding= 'utf-8')
    except FileNotFoundError:
        sg.popup_error("El archivo CSV no fue encontrado")
    else:
        csvreader = csv.reader(archivo_pokemon, delimiter = ',')
        next(csvreader)
        
        #Analisis del archivo CSV
        data = []
        bandera = True
        cant = 0
        max = 20
        while bandera:
            for linea in csvreader:
                if linea[2] == tipo:
                    data.append(linea[1])
                    cant += 1
                    if cant == max:
                        bandera = False
                        break
        archivo_pokemon.close()
        return data

def get_days_data(tablero_tipo):

    dias_semana = ['lunes', 'martes', 'miercoles', 'jueves', 'viernes', 'sabado', 'domingo']
    mañana, tarde = [(0, 12),(13, 23)]
    criteria_data = {}

    if tablero_tipo == 'Palabras':    
        criteria_name = ['agua', 'fuego', 'hoja', 'electrico', 'tierra', 'roca',
                        'fantasma', 'bicho', 'luchador', 'psíquico', 'normal',
                        'acero', 'venenoso', 'dragón'
                        ]

        criteria_type = ['Water', 'Fire', 'Grass', 'Electric', 'Ground', 'Rock',
                        'Ghost', 'Bug', 'Fighter', 'Psychic', 'Normal', 'Steel',
                        'Poison', 'Dragon'
                        ]

        for index in range(len(dias_semana)):
            criteria_m =    {   f'criterio' : ' 10 pokemones de {criteria_name[index]}',
                                'funcion' : pokemon_data,
                                'parámetro' : criteria_type[index]
                            }

            criteria_t =    {   f'criterio' : '10 pokemones de {criteria[index*2]}',
                                'funcion' : pokemon_data,
                                'parámetro' : criteria_type[index*2]
                            }
            criteria_data[dias_semana[index]] = {mañana: criteria_m, tarde: criteria_t}
    else:
        criteria_name = os.listdir(os.path.join(path_arch,'pokemon'))
        criteria_name_reversed = criteria_name[:]
        criteria_name_reversed.reverse()
        for index in range(len(criteria_name)):
            criteria_data[dias_semana[index]] = {mañana: criteria_name[index], tarde: criteria_name_reversed[index]}

    return dias_semana, criteria_data

def select_criteria(tablero_tipo):
    
    dias_semana, criteria_data = get_days_data(tablero_tipo)
    dia_actual = datetime.datetime.today().weekday()

    hora_actual = datetime.datetime.now()

    path_images_board = ''
    if tablero_tipo == 'Palabras':
        if hora_actual.hour < 13:       
            data_hoy = criteria_data[dias_semana[dia_actual]][(0, 12)]
            data_hoy = data_hoy['funcion'](data_hoy['parámetro'])
        else:
            data_hoy = criteria_data[dias_semana[dia_actual]][(13, 23)]
            data_hoy = data_hoy['funcion'](data_hoy['parámetro'])

    else:
        if hora_actual.hour < 13: 
            data_hoy = criteria_data[dias_semana[dia_actual]][(0, 12)]
        else:
            data_hoy = criteria_data[dias_semana[dia_actual]][(13, 23)]
        path_images_board = os.path.join(path_arch, 'pokemon', data_hoy)
        data_hoy = os.listdir(path_images_board)
    
    return data_hoy, path_images_board