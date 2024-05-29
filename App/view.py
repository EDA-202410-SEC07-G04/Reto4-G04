﻿"""
 * Copyright 2020, Departamento de sistemas y Computación, Universidad
 * de Los Andes
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
import sys
import controller
from DISClib.ADT import list as lt
from DISClib.ADT import stack as st
from DISClib.ADT import queue as qu
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me
from DISClib.ADT import graph as gr
assert cf
from tabulate import tabulate
import traceback

"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""


def new_controller():
    """
        Se crea una instancia del controlador
    """
    #TODO: Llamar la función del controlador donde se crean las estructuras de datos
    control = controller.new_controller()
    return control

def print_menu():
    print("Bienvenido")
    print("1- Cargar información")
    print("2- Ejecutar Requerimiento 1")
    print("3- Ejecutar Requerimiento 2")
    print("4- Ejecutar Requerimiento 3")
    print("5- Ejecutar Requerimiento 4")
    print("6- Ejecutar Requerimiento 5")
    print("7- Ejecutar Requerimiento 6")
    print("8- Ejecutar Requerimiento 7")
    print("9- Ejecutar Requerimiento 8")
    print("0- Salir")


def load_data(control):
    """
    Carga los datos
    """
    #TODO: Realizar la carga de datos
    controller.load_data(control)
    espe = mp.get(control["vuelos"], "SKMD-SKVP")
    #print(control["aeropuertos"])
    cr7 = gr.numEdges(control["aeropuertos"])
    print(cr7)
    #print(mp.size(control["vuelos"]))
    #print(mp.get(control["vuelos"], "BIKF-SKCL"))
    #print(espe)
    vertices = gr.numVertices(control["aeropuertos"])
    m10 = gr.getEdge(control["aeropuertos"], "BIKF", "SKCL")
    m11 = gr.getEdge(control["aeropuertosHaversine"], "BIKF", "SKCL")
    m12 = gr.getEdge(control["aeropuertosHaversine"], "SKCL", "BIKF")
    m13 = gr.getEdge(control["aeropuertosHaversineNodiri"], "BIKF", "SKCL")
    m14 = gr.getEdge(control["aeropuertosHaversineNodiri"], "SKCL", "BIKF")
    print(mp.get(control["vuelos"], "SKUA-SKPB"))

    print(m10)
    print(m11)
    print(m12)
    print(m13)
    print(m14)
    print(len(eliminar_copias(pruebas(control))))
    #print(mp.keySet(control["mapadistancias"]))
    #print(mp.get(control["mapadistancias"], "MYAM"))
    #print(vertices)

def pruebas(control):
    #BOG 74
    #SMT 34
    #APIAY 85
    #print(lt.size(control["listaVuelos"]))
    fn1 = lt.newList("ARRAY_LIST")
    for i in lt.iterator(control["listaVuelos"]):
        #print(i)
        if i["TIPO_VUELO"] == "MILITAR":
            if i["ORIGEN"] == "SKAP" or i["DESTINO"]=="SKAP":
                lt.addLast(fn1, i)
    
    return fn1

def eliminar_copias(lista):
    sin_copias = []
    elementos_vistos = set()
    for diccionario in lt.iterator(lista):
        items_tuple = tuple(sorted(diccionario.items()))
        if items_tuple not in elementos_vistos:
            sin_copias.append(diccionario)
            elementos_vistos.add(items_tuple)
    return sin_copias


def print_data(control, id):
    """
        Función que imprime un dato dado su ID
    """
    #TODO: Realizar la función para imprimir un elemento
    pass

def print_req_1(control):
    """
        Función que imprime la solución del Requerimiento 1 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 1
    pass


def print_req_2(control):
    """
        Función que imprime la solución del Requerimiento 2 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 2
    pass


def print_req_3(control):
    """
        Función que imprime la solución del Requerimiento 3 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 3
    pass


def print_req_4(control):
    """
        Función que imprime la solución del Requerimiento 4 en consola
    """
    ICAO_busc, tot_busc, dist_busc, nom_busc, ciudad_busc, pais_busc, trayectos_posibles_tot, lista_vert_relacionados, r1 = controller.req_4(control)
    print("El tiempo de ejecución es: "+ str(r1))
    print("Datos del aeropuerto más importante e la categoría AVIÓN_CARGA:")
    print("      ICAO:", ICAO_busc)
    print("      Nombre:", nom_busc)
    print("      Ciudad:", ciudad_busc)
    print("      País:", pais_busc)
    print("      Concurrencia de carga:", tot_busc)
    print("      Distancia total (arcos relacionados con ",ICAO_busc, "): ", dist_busc)
    print("      Total trayectos posibles: ", trayectos_posibles_tot)
    print("Información secuencia de trayectos:")
    #info por trayecto
    for ii in lt.iterator(lista_vert_relacionados):
            llave = ICAO_busc + "-" + ii["key"]
            eiu = gr.getEdge(control["aeropuertosHaversine"],ICAO_busc, ii["key"])
            valor = mp.get(control["vuelos"], llave)
            if valor is not None:
                valor2 = valor["value"]
                #en valor están los encabezados de flights
                print("       Aeropuerto origen: ", valor2["ORIGEN"])
                print("       Aeropuerto destino: ", valor2["DESTINO"])
                print("       Distancia recorrida: ", ii["index"])
                print("       Tiempo trayecto: ", valor2["TIEMPO_VUELO"])
                print("       Tipo aeronave: ", valor2["TIPO_AERONAVE"])
                print("----------------------------")



def print_req_5(control):
    """
        Función que imprime la solución del Requerimiento 5 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 5
    r1, r2, r3, r4, r5, cant = controller.req_5(control)
    print("Tiempo: "+ str(r1))
    print("Aeropuerto mas importante: " + str(r2["value"])+ " cantidad de vuelos saliendo y llegando: "+ str(cant))
    print("distancia total de los trayectos sumados: " + str(r3))
    print("Numero total de trayectos posibles: " + str(r4))
    for i in lt.iterator(r5):
        print("--------------------------------")
        var2 = mp.get(control["mapadistancias"], r2["value"]["ICAO"])["value"]
        var3 = mp.get(control["mapadistancias"], i["key"])["value"]
        llave = str(r2["value"]["ICAO"]) + "-" + str(i["key"])
        vuelo = mp.get(control["vuelos"], llave)
        #print(var2)
        print("Aeropuerto de origen: " + str(r2["value"]["ICAO"])+" " + str(var2["CIUDAD"])+" " + str(var2["PAIS"])+" " + str(var2["NOMBRE"]))
        print("Aeropuerto de destino: " + str(var3["ICAO"])+" " + str(var3["CIUDAD"])+" " + str(var3["PAIS"])+" " + str(var3["NOMBRE"]))
        print("Distancia recorrida: " + str(i["index"]) + "km")
        if vuelo == None:
            print("escala - sin vuelo directo")
        else:
            print("timepo del vuelo: " + str(vuelo["value"]["TIEMPO_VUELO"]) + " min. Tipo de aeronave: "+ str(vuelo["value"]["TIPO_AERONAVE"]))
        print("--------------------------------")


def print_req_6(control):
    """
        Función que imprime la solución del Requerimiento 6 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 6
    c_aereo = int(input("Cantidad de aeropuertos: "))
    r1, r2 = controller.req_6(control, c_aereo)


def print_req_7(control, long1, lat1, long2, lat2):
    """
        Función que imprime la solución del Requerimiento 7 en consola
    """
    controller.req_7(control, long1, lat1, long2, lat2)


def print_req_8(control):
    """
        Función que imprime la solución del Requerimiento 8 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 8
    pass


# Se crea el controlador asociado a la vista
control = new_controller()

# main del reto
if __name__ == "__main__":
    """
    Menu principal
    """
    default_limit = 2000
    sys.setrecursionlimit(default_limit*10)
    working = True
    #ciclo del menu
    while working:
        print_menu()
        inputs = input('Seleccione una opción para continuar\n')
        if int(inputs) == 1:
            print("Cargando información de los archivos ....\n")
            data = load_data(control)
        elif int(inputs) == 2:
            print_req_1(control)

        elif int(inputs) == 3:
            print_req_2(control)

        elif int(inputs) == 4:
            print_req_3(control)

        elif int(inputs) == 5:
            print("A continuación, los resultados encontrados: ")
            print_req_4(control)

        elif int(inputs) == 6:
            print_req_5(control)

        elif int(inputs) == 7:
            print_req_6(control)

        elif int(inputs) == 8:
            long1 = float(input("Por favor, digite la longitud del punto de origen: "))
            lat1 = float(input("Por favor, digite la latitud del punto de origen: "))
            long2 = float(input("Por favor, digite la longitud del punto de destino: "))
            lat2 = float(input("Por favor, digite la latitud del punto de destino: "))
            print_req_7(control, long1, lat1, long2, lat2)

        elif int(inputs) == 9:
            print_req_8(control)

        elif int(inputs) == 0:
            working = False
            print("\nGracias por utilizar el programa")
            
        else:
            print("Opción errónea, vuelva a elegir.\n")
    sys.exit(0)
