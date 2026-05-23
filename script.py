import json
import os
import db
DB = db
 

def cargar(username):

    result = DB.query("select * from user where username = %s", [username])
    if result and len(result) > 0:
        return username
    else:
        return None

def nuevo(nombre,username):
    if not username or username.strip() == "":
        return False
    
    resultado = DB.query("SELECT COUNT(*) as total FROM user WHERE username = %s", [username])

    if resultado and len(resultado) > 0:
        existe = resultado[0].get('total', 0) if isinstance(resultado[0], dict) else resultado[0][0]
        if existe > 0:
            return     False
             
    if not username or username.strip() == "":
        username = "Cocinero"
    DB.query("INSERT INTO user (nombre, username) VALUES(%s, %s)", [nombre, username])

    return True 
    


















    
# def inicio():
    
#     print("1: [ NUEVA PARTIDA ]")
#     print("2: [ CARGAR PARTIDA ]")

#     try:
#         opcion = int(input('seleccione una opcion: '))
#         if opcion == 1:
#             nuevo()
#         elif opcion == 2:
#             cargar()
#         else:
#             print("Opción no válida")
#     except ValueError:
#         print("Error: Por favor, ingresa solo números.")

# if __name__=="__main__":
#     inicio()