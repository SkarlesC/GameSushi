import json
import os

SAVE_FILE = "save_data.json"

def cargar_partidas():
    if os.path.exists(SAVE_FILE):
        with open(SAVE_FILE, "r") as f:
            return json.load(f)
        
    else:
     return {
       "slot1": None,
       "slot2": None,
       "slot3": None,
       "slot4": None
 }

def guardar_partida(slot, datos):
     partidas = cargar_partidas()
     partidas[slot] = datos
     with open(SAVE_FILE, "w") as f:
        json.dump(partidas, f, indent=4)



partidas = cargar_partidas()

# 1. Mostrar todos los slots disponibles
for slot, datos in partidas.items():
    if datos is None:
        print(f"{slot}: [ NUEVA PARTIDA ]")
    else:
        print(f"{slot}: {datos['nombre']} - Dia {datos['dia']}")

# 2. Pedir selección UNA sola vezclsc
seleccion = input("Elige un slot (slot1, slot2, slot3, slot4): ")
if seleccion in partidas:
    if partidas[seleccion] is None:
        # --- EL CAMBIO ESTÁ AQUÍ ---
        # En lugar de un nombre fijo, le pedimos al usuario que lo escriba
        nombre_usuario = input("Introduce tu nombre para la nueva partida: ")
        
        # Si el usuario no escribe nada, le ponemos un nombre por defecto
        if not nombre_usuario:
            nombre_usuario = "Cocinero"

        nuevo_jugador = {
            "nombre": nombre_usuario, 
            "dia": 1, 
            "puntos": 0
        }
        
        guardar_partida(seleccion, nuevo_jugador)
        print(f"¡Bienvenido {nombre_usuario}! Partida creada en {seleccion}")
        # ----------------------------
    else: 
        print(f"Cargando partida de {partidas[seleccion]['nombre']}...")
else:
    print("Ese slot no es válido.")