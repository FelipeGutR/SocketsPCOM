# -*- coding: utf-8 -*-
import socket
import sys
import os
from _thread import *

HOST = socket.gethostname()
HOST = '192.168.56.1'
#HOST = '181.75.92.206'
PORT = 2500

database_name = 'datatest.txt'

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    server.bind((HOST, PORT))
except socket.error as e:
    print(str(e))
    
print('Esperando conexiones...')

server.listen(10)

ruts_clientes = ['10.356.693-2', '9.965.572-0', '20.682.453-0', '20.668.440-2']
ruts_ejecutivos = ['19.785.556-8', '19.431.982-7']
nombres_clientes = ['Lilian', 'Marco', 'Santi', 'Seba']
nombres_ejecutivos = ['Felipe', 'Matías']
queue = []
ejec_disp = []

def threaded_client(conn):
    global ruts_clientes
    global nombres_clientes
    global ruts_ejecutivos
    global nombres_ejecutivos
    global queue
    global ejec_disp
    
    conn.send(str.encode('Asistente: Hola! Bienvenido, Ingrese su RUT'))
    data = conn.recv(1024).decode("utf-8")

    while (data not in ruts_clientes) and (data not in ruts_ejecutivos):
        conn.sendall(str.encode("\n Asistente: RUT no registrado, intente otra vez \
                                o contáctese con la compañía."))
        data = conn.recv(1024).decode("utf-8")

    if data in ruts_ejecutivos:
        nombre = nombres_ejecutivos[ruts_ejecutivos.index(data)]
        print(f"[SERVER] Ejecutivo {nombre} conectado")
        queue_msg = f"""Hola {nombre}, hay {len(queue)} clientes en la lista de espera
                     ¿Desea cambiar a modo Disponible?"""
        conn.sendall(str.encode(queue_msg))
        disp = conn.recv(1024).decode("utf-8")
        if disp == 'si':
            eject_disp.append(nombre)
        


    elif data in ruts_clientes:
        nombre = nombres_clientes[ruts_clientes.index(data)]

    print(f"[SERVER] Cliente {nombre} conectado")
    main_menu = f"""\n Asistente: Hola {nombre}, en qué te podemos ayudar?.
        (1) Revisar atenciones anteriores.
        (2) Reiniciar servicios.
        (3) Contactar a un ejecutivo
        (4) Salir"""
    conn.sendall(main_menu.encode())
        
    main_menu2 = f"""\n Asistente: ¿En qué más te podemos ayudar?.
    (1) Revisar atenciones anteriores.
    (2) Reiniciar servicios.
    (3) Contactar a un ejecutivo
    (4) Salir"""

    response = conn.recv(1024).decode("utf-8")
    
    first = True

    if response == '4':
        msg = f'Asistente: Gracias por preferir nuestros servicios Señor@ {nombre}, hasta pronto!'
        conn.sendall(msg.encode())
        print(f'[SERVER] Cliente {nombre} desconectado.')
        conn.close() 


    def listar(database_name):
        data = open(database_name,'r')
        datos = str(data.readlines()).replace('[','').replace("']",'').replace("'",'')[:-1]
        data.close()
        return datos.rstrip().split(";")

    def isolate(datos):
        lista = datos.rstrip().split(",")
        return lista

    def N_solicitudes(nombre, database_name):
        database = open(database_name,"r")
        databases = str(database.readlines())
        new = databases.rstrip().split(";")
        c = 0
        for i in range(len(new)):
            if nombre in new[i]:
                c +=1
        return c
    
    def Registrar_solicitud(nombre, descr, hist, est, database_name):
        database = open(database_name,"a")
        rut = ruts_clientes[nombres_clientes.index(nombre)]
        nsolicitud = N_solicitudes(nombre, database_name)
        database.write(f'{rut},{nsolicitud},{descr},{hist},{est};')

    def Mostrar_solicitudes(rut, database_name):
        datalist = listar(database_name)
        your_data = []
        a = ['\n Asistente: Elija la solicitud que desea revisar']
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


    resp = Mostrar_solicitudes(nombre, database_name)
    print(resp)
                       
    while response != '4':

        if first == True:
            pass
        else:
            response = conn.recv(1024).decode("utf-8")
            
        if response == '1':
            rut = ruts_clientes[nombres_clientes.index(nombre)]
            conn.sendall(str.encode('\n'.join(Mostrar_solicitudes(rut, database_name)[0])))
            
            eleccion = int(conn.recv(1024).decode("utf-8"))
            conn.sendall(str.encode('Asistente: ')+str.encode(Mostrar_solicitudes(rut, database_name)[1][eleccion-1][3] \
                                                              +'\n'+main_menu2))
            
        
        elif response == '2':
            msg = 'Asistente: Su módem será reiniciado, por favor, espere un momento \n' + main_menu2
            conn.sendall(msg.encode())
            print(f"[SERVER] Reinicio Servicios Cliente {nombre}")
            
        elif response == '3':
            rut = ruts_clientes[nombres_clientes.index(nombre)]
            queue.append(rut)
            while queue[0] != rut:
                wait_msg = f"Estamos redirigiendo a un asistente, usted está número {len(queue)} en la fila."
                conn.sendall(wait_msg.encode())
            if queue[0] == rut and ejec_disp != []:
                del queue[0]
                ##Implemenar comuniación con ejecutivo

                ####
            conn.sendall(main_menu2.encode())
            
        
        elif response == '4':
            msg = f'Asistente: Gracias por preferir nuestros servicios Señor@ {nombre}, hasta pronto!'
            conn.sendall(msg.encode())
            print(f'[SERVER] Cliente {nombre} desconectado.')
            conn.close()

        first = False    
    
    

while True:
    Client, address = server.accept()
    #print('Connected to: ' + address[0] + ':' + str(address[1]))
    start_new_thread(threaded_client, (Client, ))
    #print('Thread Number: ' + str(ThreadCount))
server.close()
