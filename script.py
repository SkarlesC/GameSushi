import json
import os
import db
DB = db

def cargar(nombre):
    result = DB.query("select * from user where nombre = %s", [nombre])
    if len(result) > 0:
        return nombre
    else:
        return None

def nuevo(nombre):
    if not nombre or nombre.strip() == "":
        nombre = "Cocinero"
    DB.query("INSERT INTO user (nombre) VALUES(%s)", [nombre])
    return nombre
    
def inicio():
    print("1: [ NUEVA PARTIDA ]")
    print("2: [ CARGAR PARTIDA ]")

    try:
        opcion = int(input('seleccione una opcion: '))
        if opcion == 1:
            nuevo()
        elif opcion == 2:
            cargar()
        else:
            print("Opción no válida")
    except ValueError:
        print("Error: Por favor, ingresa solo números.")

if __name__=="__main__":
    inicio()