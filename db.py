

import mysql.connector 

def get_connection():
    config = {
        'host': 'localhost',
        'user': 'root',
        'password': '',
        'database': 'sushi',
        'raise_on_warnings': True
    }
    try: 
        connection = mysql.connector.connect(**config)
        return connection
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None 
    
def query(sql, parametros):
    """
    Ejecuta una consulta SQL utilizando parámetros para prevenir inyecciones.
    'sql' debe contener placeholders (e.g., %s) y 'parametros' debe ser una tupla o lista.
    """
    connection = get_connection()
    cursor = None # Inicializamos para evitar errores en el bloque 'finally'

    if connection is None:
        print("No se pudo conectar a la base de datos")
        return None
    
    try: 
        cursor = connection.cursor()
        
        # Pasamos los parámetros por separado. 
        # El conector se encarga de sanitizarlos automáticamente.
        cursor.execute(sql, parametros)
        
        results = cursor.fetchall()
        return results

    except mysql.connector.Error as err:       
        print(f"Error: {err}")
        return None
        
    finally:
        # Cerramos recursos de forma segura
        if cursor:
            cursor.close()
        if connection:
            connection.close()

if __name__=="__main__":
    query()


