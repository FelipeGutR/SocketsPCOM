##import threading
##
##num = 0
##
##def sumar_a_num(sumando):
##    global num
##    print("[SUMANDO]")
##    print(f"numerito: {num}")
##    num += sumando
##    print(f"nuevo numerito: {num}")
##
##def restar_a_num(sustraendo):
##    global num
##    print("[RESTANDO]")
##    print(f"numerito: {num}")
##    num -= sustraendo
##    print(f"nuevo numerito: {num}")
##
##for i in range(3):
##    t1 = threading.Thread(target=sumar_a_num, args=(1,))
##    t1.start()
##    t2 = threading.Thread(target=restar_a_num, args=(1,))
##    t2.start()

import threading

num = 0
mutex = threading.Lock()

def sumar_a_num(sumando, nom):
    global num
    print(f"Ejecutando thread de suma {nom}")
    with mutex:
        print("[SUMANDO]")
        print(f"numerito: {num}")
        num += sumando
        print(f"nuevo numerito: {num}")
    print(f"Thread {nom} de suma termina")

def restar_a_num(sustraendo, nom):
    global num
    print(f"Ejecutando thread de resta {nom}")
    with mutex:
        print("[RESTANDO]")
        print(f"numerito: {num}")
        num -= sustraendo
        print(f"nuevo numerito: {num}")
    print(f"Thread {nom} de resta termina")

for i in range(3):
    t1 = threading.Thread(target=sumar_a_num, args=(1, i))
    t1.start()
    t2 = threading.Thread(target=restar_a_num, args=(1, i))
    t2.start()
