﻿"""
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
 """

import config as cf
import model
import time
import csv
import tracemalloc

"""
El controlador se encarga de mediar entre la vista y el modelo.
"""


def new_controller():
    """
    Crea una instancia del modelo
    """
    #TODO: Llamar la función del modelo que crea las estructuras de datos
    control = model.new_data_structs()
    return control


# Funciones para la carga de datos

def load_data(control):
    """
    Carga los datos del reto
    """
    # TODO: Realizar la carga de datos
    load_flights(control)
    load_airports(control)
    control, militar_defi, carga_defi, comerciales_defi = model.addAeropuertoConnection(control)
    return control, militar_defi, carga_defi, comerciales_defi
    

def load_airports(control):
    servicesfile = cf.data_dir + "airports-2022.csv"
    input_file = csv.DictReader(open(servicesfile, encoding="utf-8"),
                                delimiter=";")
    lastservice = None
    for service in input_file:
        model.crearmapadistancia(control, service) 
        model.add_data(control, service)
        if lastservice is not None:
            #print(lastservice['ICAO'])
            sameservice = lastservice['ICAO'] == service['ICAO']
            samedirection = lastservice['CIUDAD'] == service['CIUDAD']
            samebusStop = lastservice['PAIS'] == service['PAIS']
            
        lastservice = service
    #model.addRouteConnections(analyzer)
    return control

def load_flights(control):
    servicesfile = cf.data_dir + "fligths-2022.csv"
    input_file = csv.DictReader(open(servicesfile, encoding="utf-8"),
                                delimiter=";")
    for flight in input_file:
        sameservice = flight['ORIGEN']
        sameservice2 = flight['DESTINO']
        #print(sameservice, sameservice2)
        elemento = flight
        model.crearmapa(control, sameservice, sameservice2, elemento) 
        model.add_data_flights(control, flight)
    return control


# Funciones de ordenamiento

def sort(control):
    """
    Ordena los datos del modelo
    """
    #TODO: Llamar la función del modelo para ordenar los datos
    pass


# Funciones de consulta sobre el catálogo

def get_data(control, id):
    """
    Retorna un dato por su ID.
    """
    #TODO: Llamar la función del modelo para obtener un dato
    pass


def req_1(control, p_origen, p_destino):
    """
    Retorna el resultado del requerimiento 1
    """
    # TODO: Modificar el requerimiento 1
    start_time = get_time()
    km_tot, tot_aero_en_camino, lst_vuelos, tm_tot, ae_ori, ae_des = model.req_1(control, p_origen, p_destino)
    end_time = get_time()
    r1 = delta_time(start_time, end_time)
    return r1, km_tot, tot_aero_en_camino, lst_vuelos, tm_tot, ae_ori, ae_des


def req_2(control, origen, destino):
    """
    Retorna el resultado del requerimiento 2
    """
    # TODO: Modificar el requerimiento 2
    start_time = get_time()
    distancia_total, aeropuertos_visitados, info_origen, info_destino, lista_vert_relacionados = model.req_2(control, origen, destino)
    end_time = get_time()
    deltaTime = delta_time(start_time, end_time)
    return distancia_total, aeropuertos_visitados, info_origen, info_destino, lista_vert_relacionados, deltaTime


def req_3(control):
    """
    Retorna el resultado del requerimiento 3
    """
    # TODO: Modificar el requerimiento 3
    start_time = get_time()
    informacion_ae, suma_recorridos, total_tayectos, aero_conectados = model.req_3(control)
    end_time = get_time()
    deltaTime = delta_time(start_time, end_time)
    return informacion_ae, suma_recorridos, total_tayectos,aero_conectados, deltaTime
    pass


def req_4(control):
    """
    Retorna el resultado del requerimiento 4
    """
    start_time = get_time()
    ICAO_busc, tot_busc, dist_busc, nom_busc, ciudad_busc, pais_busc, trayectos_posibles_tot, lista_vert_relacionados = model.req_4(control)
    end_time = get_time()
    r1 = delta_time(start_time, end_time)
    return ICAO_busc, tot_busc, dist_busc, nom_busc, ciudad_busc, pais_busc, trayectos_posibles_tot, lista_vert_relacionados, r1


def req_5(control):
    """
    Retorna el resultado del requerimiento 5
    """
    # TODO: Modificar el requerimiento 5
    start_time = get_time()
    r2, r3, r4, r5, cant = model.req_5(control)
    end_time = get_time()
    r1 = delta_time(start_time, end_time)
    return r1, r2, r3, r4, r5, cant

def req_6(control, c_aereo):
    """
    Retorna el resultado del requerimiento 6
    """
    # TODO: Modificar el requerimiento 6
    start_time = get_time()
    r2, concurrencia_comercial, finali = model.req_6(control, c_aereo)
    end_time = get_time()
    r1 = delta_time(start_time, end_time)
    return r1, r2, concurrencia_comercial, finali


def req_7(control, long1, lat1, long2, lat2):
    """
    Retorna el resultado del requerimiento 7
    """
    start_time = get_time()
    rtaa, d_ini, d_fin, tiempo_tot, dist_tot, cant, lst_secuencia, nom_ini_fin = model.req_7(control, long1, lat1, long2, lat2)
    end_time = get_time()
    r1 = delta_time(start_time, end_time)
    return r1, rtaa, d_ini, d_fin, tiempo_tot, dist_tot, cant, lst_secuencia, nom_ini_fin

def req_8(control):
    """
    Retorna el resultado del requerimiento 8
    """
    # TODO: Modificar el requerimiento 8
    pass


# Funciones para medir tiempos de ejecucion

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

def get_memory():
    """
    toma una muestra de la memoria alocada en instante de tiempo
    """
    return tracemalloc.take_snapshot()


def delta_memory(stop_memory, start_memory):
    """
    calcula la diferencia en memoria alocada del programa entre dos
    instantes de tiempo y devuelve el resultado en bytes (ej.: 2100.0 B)
    """
    memory_diff = stop_memory.compare_to(start_memory, "filename")
    delta_memory = 0.0

    # suma de las diferencias en uso de memoria
    for stat in memory_diff:
        delta_memory = delta_memory + stat.size_diff
    # de Byte -> kByte
    delta_memory = delta_memory/1024.0
    return delta_memory
