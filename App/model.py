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
from DISClib.ADT import stack
from DISClib.Utils import error as error
from datetime import datetime as dt
import folium
import webbrowser
import sys
import time
import math
from math import sin,cos,sqrt,asin,pi
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
            "costos": None,
            "listaAeropuertos": None,
            "aeropuertosHaversine": None,
            "listaVuelos": None,
            "caminos5": None,
            "caminos6": None,
            "caminos7": None,
            "caminos1": None

        }
    
        control["vuelos"] = mp.newMap(numelements=3020,
                                     maptype='PROBING',
                                     cmpfunction=compararorigen)
        
        control["mapadistancias"] = mp.newMap(numelements=428,
                                     maptype='PROBING',
                                     cmpfunction=compararorigen)

        control["aeropuertos"] = gr.newGraph(datastructure="ADJ_LIST",
                                             directed=True,
                                             size=428,
                                             cmpfunction=compararAeropuertos)

        control["aeropuertosHaversine"] = gr.newGraph(datastructure="ADJ_LIST",
                                             directed=True,
                                             size=428,
                                             cmpfunction=compararAeropuertos)

        control["aeropuertosHaversineNodiri"] = gr.newGraph(datastructure="ADJ_LIST",
                                             directed=False,
                                             size=428,
                                             cmpfunction=compararAeropuertos)

        control["listaAeropuertos"] = lt.newList("ARRAY_LIST")

        control["listaVuelos"] = lt.newList("ARRAY_LIST")

        control["grafo_no_dirigido_3"] = gr.newGraph(datastructure="ADJ_LIST",
                                                     directed=False,
                                                     size = 428,
                                                     cmpfunction=compararAeropuertos)
        control["mapa_vuelos"] = mp.newMap(numelements=428, 
                                           maptype="PROBING")

        return control
    except Exception as exp:
        error.reraise(exp, 'model:new_data_structs')


# Funciones para agregar informacion al modelo

def add_data(data_structs, data):
    """
    Función para agregar nuevos elementos a la lista
    """
    #TODO: Crear la función para agregar elementos a una lista
    lt.addLast(data_structs["listaAeropuertos"], data)
    return data_structs

def add_data_flights(data_structs, data):
    lt.addLast(data_structs["listaVuelos"], data)
    return data_structs



# Funciones para creacion de datos

def new_data(id, info):
    """
    Crea una nueva estructura para modelar los datos
    """
    #TODO: Crear la función para estructurar los datos
    pass

def load_flights():
    pass


def addAeropuertoConnection(control):
    #BIKF-SKCL 
    llave2 = mp.keySet(control["vuelos"])
    for i in lt.iterator(llave2):
        llave = i
        var1 = mp.get(control["vuelos"], llave)
        nombre = llave.split("-")
       
        n1 = nombre[0]
        #print(mp.keySet(control["mapadistancias"]))
        var2 = mp.get(control["mapadistancias"], n1)
        aero1 = var2["value"]
        var3 = mp.get(control["mapadistancias"], nombre[1])
        aero2 = var3["value"]
        dhaver = conversion(aero1, aero2)
        distancia = int(var1["value"]["TIEMPO_VUELO"])
        #print(distancia)
        nodoida = var1["value"]["ORIGEN"]
        nodovuelta = var1["value"]["DESTINO"]
        addAeropuerto(control, nodoida)
        addAeropuerto(control, nodovuelta)
        addConeccion(control, nodoida, nodovuelta, distancia)
        addAeropuertoHaversine(control, nodoida)
        addAeropuertoHaversine(control, nodovuelta)
        addConeccionHaversine(control, nodoida, nodovuelta, dhaver)
        addAeropuertoHaversineNodiri(control, nodoida)
        addAeropuertoHaversineNodiri(control, nodovuelta)
        addConeccionHaversineNodiri(control, nodoida, nodovuelta, dhaver)
    
    ## prints carga de datos 
    #comerciales
    comerciales = lt.newList(datastructure="ARRAY_LIST")
    nombre = gr.vertices(control["aeropuertos"])
    for i in lt.iterator(nombre):
        #size = lt.size(control["listaAeropuertos"])
        #nombre = lt.getElement(control["listaAeropuertos"], i+1)
        numero = lt.size(gr.adjacents(control["aeropuertos"], i))
        ltt = [i, numero,]
        lt.addLast(comerciales, ltt)
    #definir ahora que sean vuelos comerciales
    #usar listaVuelos y comprobar que el vértice de de ORIGEN o DESTINO sea alguno de los que se filtraron y 
    #comprobar el número de vuelos comerciales 
    comerciales1 = mp.newMap(numelements=428, maptype='PROBING',cmpfunction=compararorigen)
    for j in lt.iterator(control["listaVuelos"]):
        if j["TIPO_VUELO"] == "AVIACION_COMERCIAL":
            origen = j["ORIGEN"]
            destino = j["DESTINO"]

            #verificar que destino y origen estén en el mapa, primero agregarlos al mapa

            if mp.contains(comerciales1,origen) is False:
                cont_origen = 1
                mp.put(comerciales1,origen,cont_origen)
            else:
                #ya está la info en el mapa, actualizar valor
                cont_origen2 = mp.get(comerciales1, origen)
                cont_origen3 = me.getValue(cont_origen2)
                cont_origen3 += 1
                mp.put(comerciales1,origen,cont_origen3)

            # Lo mismo para el destino 

            if mp.contains(comerciales1,destino) is False:
                cont_destino = 1
                mp.put(comerciales1,destino,cont_destino)
            else:
                #ya está la info en el mapa, actualizar valor
                cont_destino2 = mp.get(comerciales1, destino)
                cont_destino3 = me.getValue(cont_destino2)
                cont_destino3 += 1
                mp.put(comerciales1,destino,cont_destino3)

    # ya con los datos en el map, pasarlos a una lista para encontrar los 5 primeros y los 5 últimos

    comerciales_lista = mp.keySet(comerciales1)
    comerciales_defi = lt.newList(datastructure="ARRAY_LIST")
    for nn in lt.iterator(comerciales_lista):
        
        concurrencia = mp.get(comerciales1, nn) 
        concurrencia2 = me.getValue(concurrencia)
        lt_comerciales = [nn, concurrencia2]
        lt.addLast(comerciales_defi,lt_comerciales )
    
    #hacer merge para encontrar los buscados 

    merg.sort(comerciales_defi, cmp_carga) #comerciales_defi son los organizados 

    #Carga
    carga = lt.newList(datastructure="ARRAY_LIST")
    nombre = gr.vertices(control["aeropuertos"])
    for i in lt.iterator(nombre):
        #size = lt.size(control["listaAeropuertos"])
        #nombre = lt.getElement(control["listaAeropuertos"], i+1)
        numero = lt.size(gr.adjacents(control["aeropuertos"], i))
        ltt = [i, numero,]
        lt.addLast(carga, ltt)
    #definir ahora que sean vuelos comerciales
    #usar listaVuelos y comprobar que el vértice de de ORIGEN o DESTINO sea alguno de los que se filtraron y 
    #comprobar el número de vuelos comerciales 
    carga1 = mp.newMap(numelements=428, maptype='PROBING',cmpfunction=compararorigen)
    for j in lt.iterator(control["listaVuelos"]):
        if j["TIPO_VUELO"] == "AVIACION_CARGA":
            origen = j["ORIGEN"]
            destino = j["DESTINO"]

            #verificar que destino y origen estén en el mapa, primero agregarlos al mapa

            if mp.contains(carga1,origen) is False:
                cont_origen = 1
                mp.put(carga1,origen,cont_origen)
            else:
                #ya está la info en el mapa, actualizar valor
                cont_origen2 = mp.get(carga1, origen)
                cont_origen3 = me.getValue(cont_origen2)
                cont_origen3 += 1
                mp.put(carga1,origen,cont_origen3)

            # Lo mismo para el destino 

            if mp.contains(carga1,destino) is False:
                cont_destino = 1
                mp.put(carga1,destino,cont_destino)
            else:
                #ya está la info en el mapa, actualizar valor
                cont_destino2 = mp.get(carga1, destino)
                cont_destino3 = me.getValue(cont_destino2)
                cont_destino3 += 1
                mp.put(carga1,destino,cont_destino3)

    # ya con los datos en el map, pasarlos a una lista para encontrar los 5 primeros y los 5 últimos

    carga_lista = mp.keySet(carga1)
    carga_defi = lt.newList(datastructure="ARRAY_LIST")
    for nn in lt.iterator(carga_lista):
        
        concurrencia = mp.get(carga1, nn) 
        concurrencia2 = me.getValue(concurrencia)
        lt_comerciales = [nn, concurrencia2]
        lt.addLast(carga_defi,lt_comerciales )
    
    #hacer merge para encontrar los buscados 

    merg.sort(carga_defi, cmp_carga) #carga_defi son los organizados 


    #Militar


    militar = lt.newList(datastructure="ARRAY_LIST")
    nombre = gr.vertices(control["aeropuertos"])
    for i in lt.iterator(nombre):
        #size = lt.size(control["listaAeropuertos"])
        #nombre = lt.getElement(control["listaAeropuertos"], i+1)
        numero = lt.size(gr.adjacents(control["aeropuertos"], i))
        ltt = [i, numero,]
        lt.addLast(militar, ltt)
    #definir ahora que sean vuelos comerciales
    #usar listaVuelos y comprobar que el vértice de de ORIGEN o DESTINO sea alguno de los que se filtraron y 
    #comprobar el número de vuelos comerciales 
    militar1 = mp.newMap(numelements=428, maptype='PROBING',cmpfunction=compararorigen)
    for j in lt.iterator(control["listaVuelos"]):
        if j["TIPO_VUELO"] == "MILITAR":
            origen = j["ORIGEN"]
            destino = j["DESTINO"]

            #verificar que destino y origen estén en el mapa, primero agregarlos al mapa

            if mp.contains(militar1,origen) is False:
                cont_origen = 1
                mp.put(militar1,origen,cont_origen)
            else:
                #ya está la info en el mapa, actualizar valor
                cont_origen2 = mp.get(militar1, origen)
                cont_origen3 = me.getValue(cont_origen2)
                cont_origen3 += 1
                mp.put(militar1,origen,cont_origen3)

            # Lo mismo para el destino 

            if mp.contains(militar1,destino) is False:
                cont_destino = 1
                mp.put(militar1,destino,cont_destino)
            else:
                #ya está la info en el mapa, actualizar valor
                cont_destino2 = mp.get(militar1, destino)
                cont_destino3 = me.getValue(cont_destino2)
                cont_destino3 += 1
                mp.put(militar1,destino,cont_destino3)

    # ya con los datos en el map, pasarlos a una lista para encontrar los 5 primeros y los 5 últimos

    militar_lista = mp.keySet(militar1)
    militar_defi = lt.newList(datastructure="ARRAY_LIST")
    for nn in lt.iterator(militar_lista):
        
        concurrencia = mp.get(militar1, nn) 
        concurrencia2 = me.getValue(concurrencia)
        lt_comerciales = [nn, concurrencia2]
        lt.addLast(militar_defi,lt_comerciales )
    
    #hacer merge para encontrar los buscados 

    merg.sort(militar_defi, cmp_carga) #militar_defi son los organizados 

    # dejar los 5 primeros y úlimos por cada tipo de vuelo
    mili_defi = lt.newList(datastructure="ARRAY_LIST")
    crg_defi = lt.newList(datastructure="ARRAY_LIST")
    com_defi = lt.newList(datastructure="ARRAY_LIST")
    len_mili = lt.size(militar_defi)
    len_crg = lt.size(carga_defi)
    len_com = lt.size(comerciales_defi)
    for i in range(5): #primeros 5 
        lt.addLast(mili_defi, lt.getElement(militar_defi, i+1))
        lt.addLast(crg_defi, lt.getElement(carga_defi, i+1))
        lt.addLast(com_defi, lt.getElement(comerciales_defi, i+1))
    
    for k in range(5):
        lt.addLast(mili_defi, lt.getElement(militar_defi, len_mili-4+k))
        lt.addLast(crg_defi, lt.getElement(carga_defi, len_crg-4+k))
        lt.addLast(com_defi, lt.getElement(comerciales_defi, len_com-4+k))

        
    return control, mili_defi, crg_defi, com_defi


def cmp_carga(da, db)  :
    di = da[1]
    df = db[1]
    if di < df:
        return False
    elif di > df:
        return True
    else:
        True
   
def conversion(v1, v2):
    #print(v1)
    v1l = (v1["LATITUD"])
    #print(v1l)
    arre = v1l.replace(",", ".")
    v1lat = float(arre)

    v1lo = (v1["LONGITUD"])
    arre1 = v1lo.replace(",", ".")
    v1lon = float(arre1)

    v2l = (v2["LATITUD"])
    arre2 = v2l.replace(",", ".")
    v2lat = float(arre2)


    v2lo = (v2["LONGITUD"])
    arre3 = v2lo.replace(",", ".")
    v2lon = float(arre3)

    final = haversine((v1lat, v1lon), (v2lat, v2lon), unit=Unit.KILOMETERS)
    

    return math.ceil(final)

def crearmapadistancia(control, aeropuerto):
    try:
        llave = aeropuerto["ICAO"]
        #print(llave)
        if not mp.contains(control["mapadistancias"], llave):
            mp.put(control["mapadistancias"], llave, aeropuerto)
        return control
    except Exception as exp:
        error.reraise(exp, 'model:crearmapa') 
        
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

def addAeropuertoHaversine(control, name):
    try: 
        if gr.containsVertex(control["aeropuertosHaversine"], name) is False:
            gr.insertVertex(control["aeropuertosHaversine"], name)
        return control
    except Exception as exp:
        error.reraise(exp, 'model:addAeropuertoHaversine')

def addAeropuertoHaversineNodiri(control, name):
    try: 
        if gr.containsVertex(control["aeropuertosHaversineNodiri"], name) is False:
            gr.insertVertex(control["aeropuertosHaversineNodiri"], name)
        return control
    except Exception as exp:
        error.reraise(exp, 'model:addAeropuertoHaversineNodiri')

# Funciones de consulta


def addConeccion(control, origen, destino, distancia):
    edge = gr.getEdge(control["aeropuertos"], origen, destino)
    if edge is None:
        gr.addEdge(control["aeropuertos"], origen, destino, distancia)
    return control

def addConeccionHaversine(control, origen, destino, distancia):
    edge = gr.getEdge(control["aeropuertosHaversine"], origen, destino)
    if edge is None:
        gr.addEdge(control["aeropuertosHaversine"], origen, destino, distancia)
    return control

def addAeropuerto_no (control, aeropuerto):
    gr.insertVertex(control["grafo_no_dirigido_3"], aeropuerto["ICAO"])
    return control

def addVuelo_no_dirigido (control, origen, destino, distancia):
    tupla = origen, destino
    mp.put(control["mapa_vuelos"], tupla, distancia)

    tuplainver= destino, origen
    

    if mp.contains(control["mapa_vuelos"], tuplainver ):
        gr.addEdge(control["grafo_no_dirigido_3"], origen, destino, distancia)
    
    return control

def addConeccionHaversineNodiri(control, origen, destino, distancia):
    edge = gr.getEdge(control["aeropuertosHaversineNodiri"], origen, destino)
    if edge is None:
        gr.addEdge(control["aeropuertosHaversineNodiri"], origen, destino, distancia)
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


def req_1(data_structs, p_origen, p_destino):
    """
    Función que soluciona el requerimiento 1
    """
    # TODO: Realizar el requerimiento 1
    aero_ori_cer, aero_des_cer = aero_cercano(data_structs, p_origen, p_destino)
    ae_ori = aero_ori_cer[0]
    ae_des = aero_des_cer[0]
    caminitor1(data_structs, aero_ori_cer[0]["ICAO"])
    tot_aero_en_camino, lst_vuelos = destinitor1(data_structs, aero_des_cer[0]["ICAO"])
    #print(tot_aero_en_camino)
    #print(lst_vuelos)
    tm_tot = 0
    km_tot = int(aero_ori_cer[1]) + int(aero_des_cer[1])
    listica = lt.newList("ARRAY_LIST")
    if tot_aero_en_camino >= 2:
        for i in lt.iterator(lst_vuelos):
            km_tot += i["weight"]
            llave = i["vertexA"] +"-"+ i["vertexB"]
            vuelo = mp.get(data_structs["vuelos"], llave)["value"]
            aer = mp.get(data_structs["mapadistancias"], i["vertexB"])["value"]
            lt.addLast(listica, aer)
            tm_tot += int(vuelo["TIEMPO_VUELO"])

    elif tot_aero_en_camino < 2:
        i = lt.firstElement(lst_vuelos)
        km_tot += i["weight"]
        llave = i["vertexA"] +"-"+ i["vertexB"]
        vuelo = mp.get(data_structs["vuelos"], llave)["value"]
        aer = mp.get(data_structs["mapadistancias"], i["vertexB"])["value"]
        lt.addLast(listica, aer)
        tm_tot += int(vuelo["TIEMPO_VUELO"]) 

    tiempo = req_82(listica, ae_ori)
    print(tiempo)

    return km_tot, tot_aero_en_camino, lst_vuelos, tm_tot, ae_ori, ae_des

    
    

def aero_cercano(data_structs, p_origen, p_destino, rango=30):
    latitud_origen = p_origen[0]
    longitud_origen = p_origen[1]
    latitud_destino = p_destino[0]
    longitud_destino = p_destino[1]

    ori = (latitud_origen, longitud_origen)
    des = (latitud_destino, longitud_destino)

    aeros_ori = lt.newList("ARRAY_LIST")
    aeros_des = lt.newList("ARRAY_LIST")
    for i in lt.iterator(data_structs["listaAeropuertos"]):
        #print(i)
        cord_aero = (float(i["LATITUD"].replace(",", ".")), float(i["LONGITUD"].replace(",", ".")))
        distancia_origen = haversine(ori, cord_aero, unit=Unit.KILOMETERS)
        distancia_destino = haversine(des, cord_aero, unit=Unit.KILOMETERS)

        if distancia_origen <= rango:
            lt.addLast(aeros_ori, (i, distancia_origen))
        
        if distancia_destino <= rango:
            lt.addLast(aeros_des, (i, distancia_destino))

        merg.sort(aeros_ori, sort_r1)
        merg.sort(aeros_des, sort_r1)

        tama1 = lt.size(aeros_ori)
        tama2 = lt.size(aeros_des)
        if tama1 == 0 or tama2 == 0:
            aero_ori_cer = (0,0)
            aero_des_cer = (0,0)
        else:
            aero_ori_cer = lt.getElement(aeros_ori, 1)
            aero_des_cer = lt.getElement(aeros_des, 1)

    return aero_ori_cer, aero_des_cer

def caminitor1(data_structs, ae):
    data_structs["caminos1"] = djk.Dijkstra(data_structs["aeropuertosHaversine"], ae)
    return data_structs

def destinitor1(data_structs, ae):
    #caminito(data_structs, ae)
    path = djk.pathTo(data_structs["caminos1"], ae)
    #print(path)
    lst = lt.newList("ARRAY_LIST")
    if path is not None:
        #print("messi")
        pathlen = stack.size(path)
        #print('El camino es de longitud: ' + str(pathlen))
        while (not stack.isEmpty(path)):
            stop = stack.pop(path)
            lt.addLast(lst, stop)
            #print(stop)
            #print("------------------")
    else:
        pathlen = 0
        stop = 0
        print('No hay camino')
    
    return pathlen, lst

def distancia_a_aero (data_structs, origen):
    lista_distancias = lt.newList("ARRAY_LIST")

    for i in lt.iterator(data_structs["listaAeropuertos"]): #para el aeropuerto más cercano de origen
        latitud_aero = i["LATITUD"].replace(',', '.')
        latitud_aero = float(latitud_aero)
        longitud_aero = i["LONGITUD"].replace(',', '.')
        longitud_aero = float(longitud_aero)

        tupla = latitud_aero, longitud_aero

        identificador = haversine(origen, tupla)
        valores = i, identificador #i es el ICAO
        lt.addLast(lista_distancias, valores)
    
    mayor = 99999
    menor_aero = None
    for i in lt.iterator(lista_distancias):
        icao, distancia = i
        if distancia <= mayor:
            mayor = distancia
            menor_aero = icao
        
        if mayor < 30:
            aeropuerto_or = mayor, menor_aero
    #print("Aeropuerto or")
    #print(aeropuerto_or)
    return aeropuerto_or


def req_2(data_structs, origen, destino):
    """
    Función que soluciona el requerimiento 2
    """
    # TODO: Realizar el requerimiento 2

    #distancia del lugar de origen al aeropuerto más cercano
    dist_org_aeroi = distancia_a_aero(data_structs, origen)
    icao_orien = dist_org_aeroi[1]["ICAO"]
    info_origen = dist_org_aeroi[1]
    #distancia destino al aeropuerto más cercano
    dist_des_aerof = distancia_a_aero(data_structs, destino)
    icao_desti = dist_des_aerof[1]["ICAO"]
    info_destino = dist_des_aerof[1]

    #camino entre los dos aeropuertos
    recorrido = bfs.BreathFirstSearch(data_structs['aeropuertosHaversine'], icao_orien) #dict
    recorrido2 = djk.Dijkstra(data_structs['aeropuertosHaversine'], icao_orien)
    recorrido3 = djk.pathTo(recorrido2, icao_desti) #recorrido entre aeropuertos
    lista_vert_relacionados = recorrido2["iminpq"]["elements"]

    lista = recorrido["visited"]
    dict_recorrido = lista["table"]
    lista_recorrido = dict_recorrido["elements"]

    listi = lt.newList("ARRAY_LIST")
    if recorrido3["size"] == 1: #si no hay escalas 
        var = gr.getEdge(data_structs['aeropuertosHaversine'], icao_orien, icao_desti)
        lt.addLast(listi, var)
        aeropuertos_visitados = 2
        distancia_vuelo = var["weight"]
    else:
        var = bfs.pathTo(recorrido, icao_desti)
        lt.addLast(listi, var)
        aeropuertos_visitados = lt.size(var) 


    #print(listi)
    



    distancia_total = dist_org_aeroi[0] + dist_des_aerof[0] + distancia_vuelo

    #print(recorrido3)
    fini = lt.newList("ARRAY_LIST")
    for i in lt.iterator(listi):
        aero = mp.get(data_structs["mapadistancias"], i["vertexB"])["value"]
        lt.addLast(fini, aero)

    
    tiempo = req_82(fini, dist_org_aeroi[1])

    return distancia_total, aeropuertos_visitados, info_origen, info_destino, recorrido3



def req_3(data_structs):
    """
    Función que soluciona el requerimiento 3
    """
    # TODO: Realizar el requerimiento 3

    #Filtrar los vuelos solo comercialaes
    comerciales = r61(data_structs)
    aero, numero_vuelos = r52(comerciales)
    info_aero = mp.get(data_structs["mapadistancias"], str(aero)) #informacion del aeropuerto
   # print(info_aero)
    codigo_ae = info_aero["value"]["ICAO"]
    ruta = djk.Dijkstra(data_structs["aeropuertosHaversine"], codigo_ae)
    aero_conectados = ruta["iminpq"]["elements"] #aeropuertos (vertices) conectados al aeropuerto de mayor importancia
    #print(aero_conectados)
    informacion_ae = info_aero["value"]["ICAO"], info_aero["value"]["NOMBRE"], info_aero["value"]["CIUDAD"], info_aero["value"]["PAIS"], numero_vuelos

    suma_recorridos = 0
    for i in lt.iterator(aero_conectados):
        suma_recorridos+=i["index"]
    

    ae = mp.get(data_structs["mapadistancias"], info_aero["key"])["value"]
    #print(ae)

    lst = lt.newList("ARRAY_LIST")
    for i in lt.iterator(aero_conectados):
        ele = mp.get(data_structs["mapadistancias"], i["key"])["value"]
        lt.addLast(lst, ele)

    req8 = req_8(lst, ae)


    return  informacion_ae, suma_recorridos, lt.size(aero_conectados), aero_conectados

def cmp_req4(da, db)  :
    di = da[1]
    df = db[1]
    ppi = da[0]
    ppf = db[0]
    if di < df:
        return False
    elif di > df:
        return True
    else:
        if ppi <= ppf:
            return True
        else:
            return False


def req_4(data_structs):
    """
    Función que soluciona el requerimiento 4
    """

    # toma el tiempo al inicio del proceso
    ##start_time = get_time()

    #encontrar el aeropuerto de mayor importancia 
    #identificar el que más vuelos tiene 
    #crear lista base donde se guardan el # de vuelos (arcos) que salen y entran del aeropuerto 
    mapa_base = mp.newMap(numelements=531, maptype="CHAINING", loadfactor=4.0)
    lista_base = lt.newList(datastructure="ARRAY_LIST")
    lst_ver = lt.newList(datastructure="ARRAY_LIST")
    for ae in lt.iterator(data_structs["listaVuelos"]):
        suma = 0 
        aeropuerto = ae["ORIGEN"]
        if lt.isPresent(lst_ver, aeropuerto) == 0 and ae["TIPO_VUELO"]=="AVIACION_CARGA":
            lt.addLast(lst_ver, aeropuerto)
            datoss = gr.degree(data_structs["aeropuertosHaversine"], aeropuerto)
            datoss2 = gr.adjacentEdges(data_structs["aeropuertosHaversine"], aeropuerto)
            for i in lt.iterator(datoss2):
                suma+= i["weight"] 
        #mp.put(mapa_base,aeropuerto,lt.size(datoss))
            tpl = [aeropuerto, datoss,suma]
            lt.addLast(lista_base,tpl)
        else:
            None

    #con la info guardada, sacar el de mayor conexiones
    merg.sort(lista_base, cmp_req4)
    buscado = lt.getElement(lista_base,1)
    ICAO_busc = buscado[0]
    tot_busc = buscado[1]
    dist_busc = buscado[2]
    #para datos faltantes #identificador ICAO, nombre, ciudad, país, total vuelos ()
    #hacer recorrdio sobre la lisat de aeropuertos 
    for aepr in lt.iterator(data_structs["listaAeropuertos"]):
        nn = aepr["ICAO"]
        if nn == ICAO_busc:
            nom_busc = aepr["NOMBRE"]
            ciudad_busc = aepr["CIUDAD"]
            pais_busc = aepr["PAIS"]

    #buscar # total de trayectos posibles 
    
    #lst_2 = lt.newList(datastructure="ARRAY_LIST")

    #recorridos = djk.distTo(nom_busc, aer)
    recorridos = djk.Dijkstra(data_structs["aeropuertosHaversine"], ICAO_busc)
    #de recorrdios sacar el # de trayectos posibles y la info de cada trayecto usando vuelos 

    #en lista_vert_relacionados se guardan los vértices destino a los que se llegan usando Dijkstra y se usarán para buscar esos trayectos en vuelos 
    lista_vert_relacionados = recorridos["iminpq"]["elements"]
    trayectos_posibles_tot = lt.size(lista_vert_relacionados)
    #usando el map de vuelos sacar la info necesaria

    ##stop_time = time.get_time()
    # calculando la diferencia en tiempo
    ##delta_Time = time.delta_time(start_time, stop_time)
    
    impo = mp.get(data_structs["mapadistancias"], ICAO_busc)["value"]

    fini = lt.newList("ARRAY_LIST")
    for i in lt.iterator(lista_vert_relacionados):
        messi = mp.get(data_structs["mapadistancias"], i["key"])["value"]
        lt.addLast(fini, messi)

    tiempo = req_8(fini, impo)

    return ICAO_busc, tot_busc, dist_busc, nom_busc, ciudad_busc, pais_busc, trayectos_posibles_tot, lista_vert_relacionados

#llave = nom_busc + "-" #+ aer
    #mp.put(mapa_base, llave, recorridos)
    #lt.addLast(lst_2, llave)

    #de aquí sale la distancia, el tiempo del trayecto y el tipo de avión

    #información del aeropuerto base


def req_5(data_structs):
    """
    Función que soluciona el requerimiento 5
    """
    # TODO: Realizar el requerimiento 5


    varsi = r51(data_structs)
    mbappe = r53(varsi)
    variuuu = lt.firstElement(mbappe)
    aeropuerto, cant = variuuu
    r2 = mp.get(data_structs["mapadistancias"], str(aeropuerto))
    data_structs["caminos5"] = djk.Dijkstra(data_structs["aeropuertosHaversine"], r2["value"]["ICAO"])
    r5 = (data_structs["caminos5"]["iminpq"]["elements"])
    
    r3 = 0
    for i in lt.iterator(r5):
        r3 += i["index"]

    r4 = lt.size(r5)
    #print(r2["key"])

    ae = mp.get(data_structs["mapadistancias"], r2["key"])["value"]
    #print(ae)

    lst = lt.newList("ARRAY_LIST")
    for i in lt.iterator(r5):
        ele = mp.get(data_structs["mapadistancias"], i["key"])["value"]
        lt.addLast(lst, ele)

    req8 = req_8(lst, ae)

    return r2, r3, r4, r5, cant

def r51(data_structs):
    dic = {}

    for i in lt.iterator(data_structs["listaVuelos"]):
        if i["TIPO_VUELO"] == "MILITAR":
            ori = i["ORIGEN"]
            des = i["DESTINO"]

            if ori not in dic:
                dic[ori] = {"salidas": 0, "llegadas": 0}
            if des not in dic:
                dic[des] = {"salidas": 0, "llegadas": 0}

            dic[ori]["salidas"] += 1
            dic[des]["llegadas"] += 1
    
    return dic

def r52(salidas):
    max_vuelos = 0
    aero = None

    for x, y in salidas.items():
        tot = y["salidas"] + y["llegadas"]
        if tot > max_vuelos:
            max_vuelos = tot
            aero = x

    return aero, max_vuelos

def r53(salidas):
    final = lt.newList("ARRAY_LIST")
    finalissima = lt.newList("ARRAY_LIST")
    for x, y in salidas.items():
        tot_vue = y["salidas"] + y["llegadas"]
        lt.addLast(final, (x, tot_vue))

    finalissima = merg.sort(final, cmp_req6)
    return finalissima


def req_6(data_structs, c_aero):
    """
    Función que soluciona el requerimiento 6
    """
    # TODO: Realizar el requerimiento 6
    var1 = r62(r61(data_structs))
    var2 = lt.subList(var1, 1, c_aero)
    aero = (lt.getElement(var2, 1))
    concurrencia_comercial = aero[1]
    #print(concurrencia_comercial)
    #print(aero)
    #print(aero[0])
    r2 = mp.get(data_structs["mapadistancias"], aero[0])["value"]
    #print(r2["ICAO"])
    #ae_inicial = 
    caminito(data_structs, r2["ICAO"])
    #print(data_structs["caminos6"])
    #r5 = (data_structs["caminos6"]["visited"])
    #data_structs["caminos6"] = djk.Dijkstra(data_structs["aeropuertosHaversine"], r2["ICAO"])
    lst = lt.newList("ARRAY_LIST")
    for i in lt.iterator(var2):
        ae_destino = i[0]
        #print(ff["value"])
        lt.addLast(lst, ae_destino)

    lt.deleteElement(lst, 1)
    #print(lst)
    #print(r5)

    #print(lst)

    finali = lt.newList("ARRAY_LIST")
    for i in lt.iterator(lst):
        tot_aero_en_camino, lst_vuelos = destinito(data_structs, i)           
        lt.addLast(finali, (tot_aero_en_camino, lst_vuelos["elements"]))

    #destinito(data_structs, "SKRG")  
    lst8 = lt.newList("ARRAY_LIST")
    for i in lt.iterator(lst):
        #print(i)
        ele = mp.get(data_structs["mapadistancias"], i)["value"]
        lt.addLast(lst8, ele) 

    req8 = req_8(lst8, r2)  
    
    return r2, concurrencia_comercial, finali

def caminito(data_structs, ae):
    data_structs["caminos6"] = djk.Dijkstra(data_structs["aeropuertosHaversine"], ae)
    return data_structs

def destinito(data_structs, ae):
    #caminito(data_structs, ae)
    path = djk.pathTo(data_structs["caminos6"], ae)
    #print(path)
    lst = lt.newList("ARRAY_LIST")
    if path is not None:
        #print("messi")
        pathlen = stack.size(path)
        #print('El camino es de longitud: ' + str(pathlen))
        while (not stack.isEmpty(path)):
            stop = stack.pop(path)
            lt.addLast(lst, stop)
            #print(stop)
            #print("------------------")
    else:
        pathlen = 0
        stop = 0
        print('No hay camino')
    
    return pathlen, lst


def r61(data_structs):
    dic = {}

    for i in lt.iterator(data_structs["listaVuelos"]):
        if i["TIPO_VUELO"] == "AVIACION_COMERCIAL":
            ori = i["ORIGEN"]
            des = i["DESTINO"]

            if ori not in dic:
                dic[ori] = {"salidas": 0, "llegadas": 0}
            if des not in dic:
                dic[des] = {"salidas": 0, "llegadas": 0}

            dic[ori]["salidas"] += 1
            dic[des]["llegadas"] += 1
    
    return dic

def r62(salidas):
    final = lt.newList("ARRAY_LIST")
    finalissima = lt.newList("ARRAY_LIST")
    for x, y in salidas.items():
        tot_vue = y["salidas"] + y["llegadas"]
        lt.addLast(final, (x, tot_vue))

    finalissima = merg.sort(final, cmp_req6)
    return finalissima

def cmp_req7(da, db)  :
    di = da[1]
    df = db[1]
    if di < df:
        return True
    elif di > df:
        return False
    else:
        True

def req_7(data_structs, long1, lat1, long2, lat2):
    """
    Función que soluciona el requerimiento 7
    """
    #haversine((v1lat, v1lon), (v2lat, v2lon), unit=Unit.KILOMETERS)
    #Pasar a distancia Haversine cada Aeropuerto dentro de una lista 
    ##Fórmula de haversine
    #d = 2*r*asin(sqrt(sin(c*(lat2-lat1)/2)**2 + cos(c*lat1)*cos(c*lat2)*sin(c*(long2-long1)/2)**2))
    Haversine_ICAO_lst_ini = lt.newList(datastructure="ARRAY_LIST")
    Haversine_ICAO_lst_fin = lt.newList(datastructure="ARRAY_LIST")

    #Haversine_ICAO_map_ini = mp.newMap(numelements=531, maptype="CHAINING", loadfactor=4.0) 
    #Haversine_ICAO_map_fin = mp.newMap(numelements=531, maptype="CHAINING", loadfactor=4.0) 

    # en cada map se guarda el ICAO y la distancia desde el punto ini y fin dados por parámetros 

    lst_ver = lt.newList(datastructure="ARRAY_LIST")

    usuario_ini = (lat1, long1)
    usuario_fin = (lat2, long2)
    for i in lt.iterator(data_structs["listaAeropuertos"]):
        #comparar long1 y lat1 con cada aeropuerto 
        lati = float(i["LATITUD"].replace(",", "."))
        longi = float(i["LONGITUD"].replace(",", "."))
        aeropuerto = (lati, longi)
        
        d_ini = haversine(aeropuerto, usuario_ini)
        d_fin = haversine(aeropuerto, usuario_fin)
        
        val = [i["ICAO"], d_ini]
        lt.addLast(Haversine_ICAO_lst_ini, val)
        val = [i["ICAO"], d_fin]
        lt.addLast(Haversine_ICAO_lst_fin, val)

        #mp.put(Haversine_ICAO_map_ini,i["ICAO"],d_ini)
        #mp.put(Haversine_ICAO_map_fin,i["ICAO"],d_fin)
    #ordenar la info para obtener el de menos distancia en ambos casos
    merg.sort(Haversine_ICAO_lst_ini, cmp_req7) 
    merg.sort(Haversine_ICAO_lst_fin, cmp_req7)
    #confirmar que están a menos de 30 km de distancia 
    #confirmar que hay camino desde cada aeropuerto
    #hacer Dijkstra desde el nombre de origen
    cont = 1
    jnd = lt.getElement(Haversine_ICAO_lst_ini, 1)
    jnd = jnd[1]
    jnd1 = lt.getElement(Haversine_ICAO_lst_fin, 1)
    jnd1 = jnd1[1]
    #así se asegura que la distancia es menor a 30 
    if jnd1 > 30 or jnd > 30:
        rtaa = 0
    else:
        rtaa=1
        nom_ini = lt.getElement(Haversine_ICAO_lst_ini, cont)
        nom_ini = nom_ini[0]
        nom_fin = lt.getElement(Haversine_ICAO_lst_fin, cont)
        nom_fin = nom_fin[0]
        #jnd = lt.getElement(Haversine_ICAO_lst_ini, cont)
        #jnd = jnd[1]
        #Dijkstra desde nom_ini (nombre vértice inicial) 
        #rta = djk.Dijkstra(data_structs["aeropuertos"], nom_ini)

        #retorna info del camino usando aeropuertos
        caminito7(data_structs, nom_ini)
        cant, lst = destinito7(data_structs, nom_fin)

        #retorna info del camino usando aeropuertosHaversine para el trayecto del vuelo

        caminito7_1(data_structs, nom_ini)
        cant1, lst1 = destinito7_1(data_structs, nom_fin)
    
        tiempo_tot = lst["elements"][0]["weight"]
        dist_tot = lst1["elements"][0]["weight"]
        #numero aeropuertos es cant

        #sacar la secuencia de aeropuertos
        lst_secuencia = lt.newList(datastructure="ARRAY_LIST")
        for final in lt.iterator(lst):
            vert_A = final["vertexA"]
            vert_B = final["vertexB"]
            llave = vert_A +"-"+vert_B
            lt.addLast(lst_secuencia,llave)
        nom_ini_fin = nom_ini

    
    fini = lt.newList("ARRAY_LIST")
    for i in lt.iterator(lst_secuencia):
        vuelos = i.split("-")
        aero = mp.get(data_structs["mapadistancias"], vuelos[1])["value"]
        lt.addLast(fini, aero)

    cr7 = mp.get(data_structs["mapadistancias"], nom_ini_fin)["value"]

    tiempo = req_82(fini, cr7)

    return rtaa, d_ini, d_fin, tiempo_tot, dist_tot, cant, lst_secuencia, nom_ini_fin
    
    



        #print(cant)
        #print(lst)
        #confirmar que hya camino desde VerticeA hasta Vertice B (nom_fin)

    #tiempo y distancia total del camino
    #tiempo = djk.distTo()


    """
        camino = djk.hasPathTo(rta, nom_fin)
        if camino is True:
            #significa que hay un camino, entonces tenerlo en cuenta 
            #costo camino
            costoo = djk.distTo(rta, nom_fin)
            #reconstruir el camino
            recorrido = djk.pathTo(rta, nom_fin)
            jnd = 31 #porque encontró la primera opción de camino 
        #comprobar que el vuelo es comercial. Es comercial si durante el camino que recorre ese vuelo es comercial usando las llaves "ORIGEN"
        #for i in lt.iterator(recorrido):
            #a=1



    while jnd  == 0:
        cont += 1
        nom_ini = lt.getElement(Haversine_ICAO_lst_ini, cont)
        nom_ini = nom_ini[0]
        nom_fin = lt.getElement(Haversine_ICAO_lst_fin, cont)
        nom_fin = nom_fin[0]
        rta = djk.Dijkstra(data_structs["aeropuertos"], nom_ini)
        #confirmar que hya camino desde VerticeA hasta Vertice B
        camino = djk.hasPathTo(rta, nom_fin)
        lista_vert_relacionados = rta["iminpq"]["elements"]
        #comprobar que el vertice destino esté dentro del rango 
        jnd = lt.isPresent(lista_vert_relacionados, nom_fin)
    # distancias entre los aeropuertos seleccionados
    dist_aeropuertos = gr.getEdge(data_structs["aeropuertosHaversine"], nom_ini, nom_fin)
    tiempo_aeropuertos = gr.getEdge(data_structs["aeropuertos"], nom_ini, nom_fin)
    # número de aeropuertos que se visitan en el camino encontrado 
    datos = rta["visited"]["table"]["elements"]
    ihiyg = djk.distTo()
    aaa = djk.pathTo(rta, nom_fin)
    pass
    """


"""
    for j in lt.iterator(Haversine_ICAO_lst_fin):
        nom_ini = lt.getElement(Haversine_ICAO_lst_ini, 1)
        nom_fin = lt.getElement(Haversine_ICAO_lst_fin, 1)
        if djk.pathTo()
        if gr.getEdge()
   
"""
def caminito7(data_structs, ae):
    data_structs["caminos7"] = djk.Dijkstra(data_structs["aeropuertos"], ae)
    return data_structs

def destinito7(data_structs, ae):
    #caminito(data_structs, ae)
    path = djk.pathTo(data_structs["caminos7"], ae)
    #print(path)
    lst = lt.newList("ARRAY_LIST")
    if path is not None:
        #print("messi")
        pathlen = stack.size(path)
        #print('El camino es de longitud: ' + str(pathlen))
        while (not stack.isEmpty(path)):
            stop = stack.pop(path)
            lt.addLast(lst, stop)
            #print(stop)
            #print("------------------")
    else:
        pathlen = 0
        stop = 0
        print('No hay camino')
    
    return pathlen, lst


def caminito7_1(data_structs, ae):
    data_structs["caminos7"] = djk.Dijkstra(data_structs["aeropuertosHaversine"], ae)
    return data_structs

def destinito7_1(data_structs, ae):
    #caminito(data_structs, ae)
    path = djk.pathTo(data_structs["caminos7"], ae)
    #print(path)
    lst = lt.newList("ARRAY_LIST")
    if path is not None:
        #print("messi")
        pathlen = stack.size(path)
        #print('El camino es de longitud: ' + str(pathlen))
        while (not stack.isEmpty(path)):
            stop = stack.pop(path)
            lt.addLast(lst, stop)
            #print(stop)
            #print("------------------")
    else:
        pathlen = 0
        stop = 0
        print('No hay camino')
    
    return pathlen, lst

def req_8(lst, ae):
    """
    Función que soluciona el requerimiento 8
    """
    # TODO: Realizar el requerimiento 8
    start_time = get_time()
    
    locacion = (float(ae["LATITUD"].replace(",", ".")), float(ae["LONGITUD"].replace(",", ".")))
    mapa = folium.Map(location=locacion, zoom_start=2)
    
    folium.Marker(
        location=locacion,
        popup=f"<b>{ae['NOMBRE']}</b><br>Ciudad: {ae['CIUDAD']}",
        icon=folium.Icon(color='red')
    ).add_to(mapa)

    for i in lt.iterator(lst): 
        longi = i["LONGITUD"].replace(",", ".")
        lati = i["LATITUD"].replace(",", ".")
        loca = (lati, longi)
        
        folium.Marker(
            location=loca,
            popup=f"<b>{i['NOMBRE']}</b><br>Ciudad: {i['CIUDAD']}"
        ).add_to(mapa)
        
        folium.PolyLine(
            [locacion, loca],
            color='blue',  
            weight=2,      
            opacity=0.6    
        ).add_to(mapa)

    mapa.save("mapa.html")
    webbrowser.open("mapa.html")
    
    end_time = get_time()
    deltaTime = delta_time(start_time, end_time)
    return deltaTime

def req_82(lst, ae):
    """ Función que soluciona el requerimiento 8 """
    start_time = get_time()
    locacion = (float(ae["LATITUD"].replace(",", ".")), float(ae["LONGITUD"].replace(",", ".")))
    mapa = folium.Map(location=locacion, zoom_start=2)

    folium.Marker(
        location=locacion,
        popup=f"<b>{ae['NOMBRE']}</b><br>Ciudad: {ae['CIUDAD']}",
        icon=folium.Icon(color='red')
    ).add_to(mapa)

    prev_loca = locacion
    for i in lt.iterator(lst):

        longi = float(i["LONGITUD"].replace(",", "."))
        lati = float(i["LATITUD"].replace(",", "."))
        loca = (lati, longi)

        folium.Marker(
            location=loca,
            popup=f"<b>{i['NOMBRE']}</b><br>Ciudad: {i['CIUDAD']}"
        ).add_to(mapa)

        folium.PolyLine(
            [prev_loca, loca],
            color='blue',
            weight=2,
            opacity=0.6
        ).add_to(mapa)

        prev_loca = loca

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

def cmp_req6(x1, x2):
    iata1 = x1[0]
    iata2 = x2[0]
    cant1 = x1[1]
    cant2 = x2[1]
    if cant1 > cant2:
        return True
    elif cant1 == cant2:
        if iata1 < iata2:
            return True
        else:
            return False
    else:
        return False

def sort_r1(x1, x2):
    iata1 = x1[0]["ICAO"]
    iata2 = x2[0]["ICAO"]
    cant1 = x1[1]
    cant2 = x2[1]
    if cant1 < cant2:
        return True
    elif cant1 == cant2:
        if iata1 < iata2:
            return True
        else:
            return False
    else:
        return False


def get_time():
    """
    devuelve el instante tiempo de procesamiento en milisegundos
    """
    return float(time.perf_counter()*1000)


def delta_time(start, end):
    """
    devuelve la diferencia entre tiempos de procesamiento muestreados
    """
    elapsed = float(end - start)
    return elapsed