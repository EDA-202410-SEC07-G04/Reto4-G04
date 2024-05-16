"""
 * Copyright 2020, Departamento de sistemas y Computación,
 * Universidad de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along withthis program.  If not, see <http://www.gnu.org/licenses/>.
 *
 * Contribuciones:
 *
 * Dario Correal - Version inicial
 """


import config as cf
from DISClib.ADT import list as lt
from DISClib.ADT import stack as st
from DISClib.ADT import queue as qu
from DISClib.ADT import map as mp
from DISClib.ADT import minpq as mpq
from DISClib.ADT import indexminpq as impq
from DISClib.ADT import orderedmap as om
from DISClib.DataStructures import mapentry as me
from DISClib.ADT import graph as gr
from DISClib.Algorithms.Graphs import scc
from DISClib.Algorithms.Graphs import dijsktra as djk
from DISClib.Algorithms.Graphs import bellmanford as bf
from DISClib.Algorithms.Graphs import bfs
from DISClib.Algorithms.Graphs import dfs
from DISClib.Algorithms.Graphs import prim
from DISClib.Algorithms.Sorting import shellsort as sa
from DISClib.Algorithms.Sorting import insertionsort as ins
from DISClib.Algorithms.Sorting import selectionsort as se
from DISClib.Algorithms.Sorting import mergesort as merg
from DISClib.Algorithms.Sorting import quicksort as quk
from DISClib.Utils import error as error
from datetime import datetime as dt
import folium
import webbrowser
import sys
import time
import math
from haversine import haversine, Unit
assert cf

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá
dos listas, una para los videos, otra para las categorias de los mismos.
"""

# Construccion de modelos


#ALGORITMO PRIM(EAGER) MAS EFICIENTE 

def new_data_structs():
    """
    Inicializa las estructuras de datos del modelo. Las crea de
    manera vacía para posteriormente almacenar la información.
    """
    #TODO: Inicializar las estructuras de datos
    try: 
        control = {
            "aeropuertos": None,
            "vuelos": None,
            "costos": None
        }
    
        control["vuelos"] = mp.newMap(numelements=3020,
                                     maptype='PROBING',
                                     cmpfunction=compararorigen)

        control["aeropuertos"] = gr.newGraph(datastructure="ADJ_LIST",
                                             directed=True,
                                             size=428,
                                             cmpfunction=compararAeropuertos)

        return control
    except Exception as exp:
        error.reraise(exp, 'model:new_data_structs')


# Funciones para agregar informacion al modelo

def add_data(data_structs, data):
    """
    Función para agregar nuevos elementos a la lista
    """
    #TODO: Crear la función para agregar elementos a una lista
    pass


# Funciones para creacion de datos

def new_data(id, info):
    """
    Crea una nueva estructura para modelar los datos
    """
    #TODO: Crear la función para estructurar los datos
    pass
def load_flights():
    pass


def addAeropuertoConnection(control, ultimovuelo, vuelo):
    try:
        origen = formatVertex(ultimovuelo)
        destino = formatVertex(vuelo)
        #int(distancialimpia(ultimovuelo, origen))
        llave = str(origen) + "-" + str(destino)
        #print(llave)
        #print(control["vuelos"])
        espe = mp.get(control["vuelos"], "BIKF-CYHM")
        #print(espe)
        #BIKF-CYHM llave
        #BIKF-SKCL 
        var1 = mp.get(control["vuelos"], llave)
        #print(var1)
        
        if var1 == None: 
            distancia = 0
        else:
            distancia = var1["value"]["TIEMPO_VUELO"]
            #print(distancia)
        addAeropuerto(control, origen)
        addAeropuerto(control, destino)
        addConeccion(control, origen, destino, distancia)
        return control
    except Exception as exp:
        error.reraise(exp, 'model:addAeropuertoConnection')
        
def crearmapa(control, icaoida, icaodevuelta, elemento):
    try:
        llave = str(icaoida) + "-" + str(icaodevuelta)
        #print(llave)
        if not mp.contains(control["vuelos"], llave):
            mp.put(control["vuelos"], llave, elemento)
        return control
    except Exception as exp:
        error.reraise(exp, 'model:crearmapa') 

def addAeropuerto(control, name):
    try: 
        if gr.containsVertex(control["aeropuertos"], name) is False:
            gr.insertVertex(control["aeropuertos"], name)
        return control
    except Exception as exp:
        error.reraise(exp, 'model:addAeropuerto')

def formatVertex(vuelo):
    name = vuelo["ICAO"]
    return name

def distancialimpia(ultimovuelo, vuelo):
    if vuelo['TIEMPO_VUELO'] == '':
        vuelo['TIEMPO_VUELO'] = 0
    if ultimovuelo['TIEMPO_VUELO'] == '':
        ultimovuelo['TIEMPO_VUELO'] = 0

def distanciakm(control):
    ultimovuelo["ORIGEN"]
    vuelo["ORIGEN"]
    ultimovuelo["DESTINO"]
    vuelo["DESTINO"]
        
    for i in lt.iterator(control):
        if ultimovuelo["ORIGEN"] == i["ICAO"]:
            longi = i["LONGITUD"]
            lati = I["LATITUD"]
            var1 = (lati, longi)
            if ultimovuelo["DESTINO"] == i["ICAO"]:
                longi2 = i["LONGITUD"]
                lati2 = I["LATITUD"]
                var2 = (lati2, longi2)
        if vuelo["ORIGEN"] == i["ICAO"]:
            longi = i["LONGITUD"]
            lati = I["LATITUD"]
            var1 = (lati, longi)
            if vuelo["DESTINO"] == i["ICAO"]:
                longi2 = i["LONGITUD"]
                lati2 = I["LATITUD"]
                var2 = (lati2, longi2)

    return haversine(var1, var2, unit=Unit.KILOMETERS)      


"""
def haversine(lat1, lon1, lat2, lon2):
     
    # distance between latitudes
    # and longitudes
    dLat = (lat2 - lat1) * math.pi / 180.0
    dLon = (lon2 - lon1) * math.pi / 180.0
 
    # convert to radians
    lat1 = (lat1) * math.pi / 180.0
    lat2 = (lat2) * math.pi / 180.0
 
    # apply formulae
    a = (pow(math.sin(dLat / 2), 2) +
         pow(math.sin(dLon / 2), 2) *
             math.cos(lat1) * math.cos(lat2));
    rad = 6371
    c = 2 * math.asin(math.sqrt(a))
    return rad * c
"""

# Funciones de consulta


def addConeccion(control, origen, destino, distancia):
    edge = gr.getEdge(control["aeropuertos"], origen, destino)
    if edge is None:
        gr.addEdge(control["aeropuertos"], origen, destino, distancia)
    return control


def get_data(data_structs, id):
    """
    Retorna un dato a partir de su ID
    """
    #TODO: Crear la función para obtener un dato de una lista
    pass


def data_size(data_structs):
    """
    Retorna el tamaño de la lista de datos
    """
    #TODO: Crear la función para obtener el tamaño de una lista
    pass


def req_1(data_structs):
    """
    Función que soluciona el requerimiento 1
    """
    # TODO: Realizar el requerimiento 1
    pass


def req_2(data_structs):
    """
    Función que soluciona el requerimiento 2
    """
    # TODO: Realizar el requerimiento 2
    pass


def req_3(data_structs):
    """
    Función que soluciona el requerimiento 3
    """
    # TODO: Realizar el requerimiento 3
    pass


def req_4(data_structs):
    """
    Función que soluciona el requerimiento 4
    """
    # TODO: Realizar el requerimiento 4
    pass


def req_5(data_structs):
    """
    Función que soluciona el requerimiento 5
    """
    # TODO: Realizar el requerimiento 5
    pass


def req_6(data_structs):
    """
    Función que soluciona el requerimiento 6
    """
    # TODO: Realizar el requerimiento 6
    pass


def req_7(data_structs):
    """
    Función que soluciona el requerimiento 7
    """
    # TODO: Realizar el requerimiento 7
    pass


def req_8(lst):
    """
    Función que soluciona el requerimiento 8
    """
    # TODO: Realizar el requerimiento 8
    start_time = get_time()
    mapa = folium.Map(location=[0,0], zoom_start=2)

    for i in lt.iterator(lst):
        longi = i["LONGITUD"]
        lati= i["LATITUD"]

        loca = (lati, longi)
        folium.Marker(location=loca, 
                        popup=f"<b>{i['NOMBRE']}</b><br>Ciudad: {i['CIUDAD']}").add_to(mapa)

    mapa.save("mapa.html")
    webbrowser.open("mapa.html")
    end_time = get_time()
    deltaTime = delta_time(start_time, end_time)
    return deltaTime


# Funciones utilizadas para comparar elementos dentro de una lista

def compare(data_1, data_2):
    """
    Función encargada de comparar dos datos
    """
    #TODO: Crear función comparadora de la lista
    pass

# Funciones de ordenamiento


def sort_criteria(data_1, data_2):
    """sortCriteria criterio de ordenamiento para las funciones de ordenamiento

    Args:
        data1 (_type_): _description_
        data2 (_type_): _description_

    Returns:
        _type_: _description_
    """
    #TODO: Crear función comparadora para ordenar
    pass


def sort(data_structs):
    """
    Función encargada de ordenar la lista con los datos
    """
    #TODO: Crear función de ordenamiento
    pass

def compararorigen(date1, date2):
    #print(date1, date2)
    date2 = date2["key"]
    if (date1 == date2):
        return 0
    elif (date1 > date2):
        return 1
    else:
        return -1

def compararAeropuertos(date1, date2): 
    date2 = date2["key"]
    if (date1 == date2):
        return 0
    elif (date1 > date2):
        return 1
    else:
        return -1