#!/usr/bin/env python
#-*- coding: utf-8 -*-
database_name = 'datatest.txt'

def n_lineas(database_name):
    database = open(database_name,"r")
    databases = str(database.readlines())
    new = databases.rstrip().split(";")
    return len(new)



def read():
    data = open(database_name,'r')
    datos = data.readlines()
    print(datos)
    data.close()
    return datos

def N_solicitudes(nombre, database_name):
        database = open(database_name,"r")
        databases = str(database.readlines())
        new = databases.rstrip().split(";")
        c = 0
        for i in range(len(new)):
            if nombre in new[i]:
                c +=1
        return c

def Mostrar_solicitudes(rut, database_name):
        datalist = listar(database_name)
        your_data = []
        a = ['\n Elija la solicitud que desea revisar']
        b = []
        c = 0
        for i in range(len(datalist)):
            if rut in datalist[i]:
                datos = isolate(datalist[i])
                n_sol = datos[1]
                hist = datos[3]
                est = datos[4] 
                if est == 'abierto':
                    b.append(datos)
                    c +=1
                    msg = f'({c}) Solicitud N°{n_sol}: {datos[2]}'
                    msg.replace('\n','')
                    a.append(msg)
                else:
                   pass
        return a,b
            
def Mostrar_especifico(eleccion, datos):
    return datos[eleccion-1][2]


def Registrar_solicitud(nombre, database_name):
        database = open(database_name,"a")
        nsolicitud = N_solicitudes(nombre, database_name)+1
        database.write(f'{nsolicitud},{nombre};')

def clear(database_name):
    open(database_name, "w").close()

def listar(database_name):
    data = open(database_name,'r')
    datos = str(data.readlines()).replace('[','').replace("']",'').replace("'",'')[:-1]
    data.close()
    return datos.rstrip().split(";")

def isolate(datos):
    lista = datos.rstrip().split(",")
    return lista
