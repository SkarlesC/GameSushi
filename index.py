

import pygame
import sys
import script
from cliente import Cliente 


# Configuración inicial
pygame.init()
ANCHO, ALTO = 800, 600
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Papa's Sushi")


BLANCO = (255, 255, 255)
NARANJA_PAPA = (255, 128, 0)
fuente_titulo = pygame.font.SysFont("Arial", 60, bold=True)
fuente_boton = pygame.font.SysFont("Arial", 30)
boton_nuevo_rect = pygame.Rect(200, 200, 250, 50)
boton_cargar_rect = pygame.Rect(200, 300, 250, 50)

def dibujar_texto(texto, fuente, color, x, y):
    img = fuente.render(texto, True, color)
    pantalla.blit(img, (x, y))

def menu_principal():
    reloj = pygame.time.Clock()
    
    while True:
        pantalla.fill((200, 230, 255)) # Un azul cielo de fondo
        
        # Obtener posición del mouse
        mouse_pos = pygame.mouse.get_pos()
        
        # Título del Juego
        dibujar_texto("PAPA'S SUSHI", fuente_titulo, (50, 50, 50), 180, 150)
        
        # Botón "PLAY"
        boton_rect = pygame.Rect(300, 350, 200, 60)
        
        # Efecto "hover" (si el mouse está encima, cambia de color)
        color_boton = (200, 100, 0) if boton_rect.collidepoint(mouse_pos) else NARANJA_PAPA
        
        pygame.draw.rect(pantalla, color_boton, boton_rect, border_radius=17)
        dibujar_texto("START GAME", fuente_boton, BLANCO, 320, 365)

        # Manejo de eventos
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if boton_rect.collidepoint(mouse_pos):
                    # Aquí es donde llamarías a la función de la cocina o selección de personaje
                    # print("Cargando juego...")
                    iniciar_juego()

        pygame.display.update()
        reloj.tick(60)

def iniciar_juego():
    corriendo = True
    while corriendo:
        mouse_pos = pygame.mouse.get_pos()
        pantalla.fill((255, 255, 255))
        
        # Dibujamos los botones
        dibujar_boton(pantalla, "NUEVA PARTIDA", boton_nuevo_rect, (50, 150, 50), (70, 200, 70), mouse_pos)
        dibujar_boton(pantalla, "CARGAR PARTIDA", boton_cargar_rect, (50, 50, 150), (70, 70, 200), mouse_pos)
        
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                corriendo = False
                pygame.quit()
                exit()
            
            # --- DETECCIÓN POR CLIC ---
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if evento.button == 1: # Clic izquierdo
                    if boton_nuevo_rect.collidepoint(mouse_pos):
                        # Lógica de NUEVA PARTIDA
                        nombre = pedir_valor_en_pantalla("Introduce tu nombre:")
                        username = pedir_valor_en_pantalla("Introduce tu username de jugador:")
                        result = script.nuevo(nombre, username)

                        if (result): 
                            mostrar_mensaje(pantalla, f"¡Bienvenido {nombre}! Guardando...", (0, 0, 150))
                        else:
                            mostrar_mensaje(pantalla, "Error: Ese nombre de usuario ya existe.", (200, 0, 0))
                        corriendo = False
                        
                    elif boton_cargar_rect.collidepoint(mouse_pos):
                        # Lógica de CARGAR PARTIDA
                        username = pedir_valor_en_pantalla("Usuario a cargar:")
                        result = script.cargar(username)
                        if result is None:
                            mostrar_mensaje(pantalla, "Error: Ese usuario no es válido.", (200, 0, 0))
                        else:
                            mostrar_mensaje(pantalla, f"Cargando partida de {username}...", (0, 128, 0))
                            bucle_restaurante()                                                             #  cambios en la fila 102  
                            corriendo = False









            # --- DETECCIÓN POR TECLADO ---
            # if evento.type == pygame.KEYDOWN:
            #     if evento.key == pygame.K_1:
            #         username = pedir_valor_en_pantalla("Introduce tu username de jugador:")
            #         script.nuevo(username)
            #         mostrar_mensaje(pantalla, f"¡Bienvenido {username}! Guardando...", (0, 0, 150))
            #         corriendo = False
            #     elif evento.key == pygame.K_2:
            #         username = pedir_valor_en_pantalla("Usuario a cargar:")
            #         result = script.cargar(username)
            #         if result is None:
            #             mostrar_mensaje(pantalla, "Error: Ese usuario no es válido.", (200, 0, 0))
            #         else:
            #             mostrar_mensaje(pantalla, f"Cargando partida de {username}...", (0, 128, 0))
            #             corriendo = False
        

        pygame.display.update()

def pedir_valor_en_pantalla(titulo):
    username = ""
    escribiendo = True
    fuente = pygame.font.Font(None, 40)
    
    while escribiendo:
        pantalla.fill((255, 255, 255)) # Fondo blanco
        
        # Dibujar las instrucciones y lo que el usuario va escribiendo
        txt_titulo = fuente.render(titulo, True, (0, 0, 0))
        txt_username = fuente.render(username + "|", True, (0, 0, 255)) # Azul para el username
        
        pantalla.blit(txt_titulo, (100, 150))
        pantalla.blit(txt_username, (100, 200))
        
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()
            
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN: # Al presionar ENTER
                    escribiendo = False
                elif evento.key == pygame.K_BACKSPACE: # Borrar letra
                    username = username[:-1]
                else:
                    # Solo agregar si es un caracter imprimible (letras/números)
                    if len(evento.unicode) > 0:
                        username += evento.unicode
        
        pygame.display.update()
    
    return username if username != "" else "Cocinero"

def mostrar_mensaje(pantalla, texto, color=(0, 0, 0)):
    """Función auxiliar para dibujar texto centrado rápidamente"""
    fuente = pygame.font.Font(None, 36)
    pantalla.fill((255, 255, 255))  # Limpia la pantalla (puedes usar una imagen de fondo)
    
    superficie_texto = fuente.render(texto, True, color)
    rect_texto = superficie_texto.get_rect(center=(pantalla.get_width() // 2, pantalla.get_height() // 2))
    
    pantalla.blit(superficie_texto, rect_texto)
    pygame.display.flip()
    pygame.time.delay(2000) # Pausa de 2 segundos para que el usuario lea

def dibujar_boton(pantalla, texto, rect, color_reposo, color_hover, mouse_pos):
    # Cambia de color si el mouse está encima
    color = color_hover if rect.collidepoint(mouse_pos) else color_reposo
    
    # Dibujar el rectángulo del botón
    pygame.draw.rect(pantalla, color, rect, border_radius=12)
    pygame.draw.rect(pantalla, (0, 0, 0), rect, 2, border_radius=12) # Borde negro
    
    # Renderizar y centrar el texto
    txt_surface = fuente_boton.render(texto, True, (255, 255, 255))
    txt_rect = txt_surface.get_rect(center=rect.center)
    pantalla.blit(txt_surface, txt_rect)

def bucle_restaurante():
    
    reloj = pygame.time.Clock()
    fuente_juego = pygame.font.SysFont("Arial", 18)
    fuente_dinamica = pygame.font.SysFont(["Segoe UI", "Helvetica", "Arial"], 18)
   
    cola_clientes = []

    X_MOSTRADOR = 150
    DISTANCIA_ENTRE_CLIENTES = 70

    tarjeta_seleccionada = None  
    offset_x = 0                
    offset_y = 0                
    
    # Dimensiones fijas del panel contenedor original
    X_PANEL = 450
    Y_PANEL = 50
    ANCHO_PANEL = 320
    ALTO_PANEL = 280
    
    # NUEVAS NUEVAS MEDIDAS PARA LA TARJETA (¡Ahora más anchas!)
    ANCHO_TARJETA = 380 
    ANCHO_MAX_TEXTO_TARJETA = ANCHO_TARJETA - 24 # Margen interno de 12px a cada lado
    
    X_BOTON_VOLVER = 20
    Y_BOTON_VOLVER = 20
    ANCHO_BOTON_VOLVER = 150
    ALTO_BOTON_VOLVER = 35
    
    color_amarillo_oscuro = (180, 140, 10)
    color_borde = (60, 50, 5)

    jugando = True
    while jugando:
        pantalla.fill((240, 240, 240))
        
        # SOLUCIÓN MOSTRADOR NATIVO
        pygame.draw.rect(pantalla, (139, 69, 19), (0, 400, 300, 20))
        texto_mostrador = fuente_juego.render("MOSTRADOR DE PEDIDOS", True, (100, 100, 100))
        pantalla.blit(texto_mostrador, (20, 430))
        
        dibujar_texto("Presiona [C] para un Cliente | Arrastra los pedidos con el Ratón", fuente_juego, (50, 50, 50), 380, 20)

        pygame.draw.rect(pantalla, color_amarillo_oscuro, (X_BOTON_VOLVER, Y_BOTON_VOLVER, ANCHO_BOTON_VOLVER, ALTO_BOTON_VOLVER), border_radius=17)
        # Dibujamos el borde del botón
        pygame.draw.rect(pantalla, color_borde, (X_BOTON_VOLVER, Y_BOTON_VOLVER, ANCHO_BOTON_VOLVER, ALTO_BOTON_VOLVER), width=2, border_radius=17)
    
        texto_volver = fuente_juego.render("VOLVER AL MENÚ", True, (0, 0, 0))
        pantalla.blit(texto_volver, (X_BOTON_VOLVER + 15, Y_BOTON_VOLVER + 7))
        
        # PANEL CONTENEDOR DE PEDIDOS (Fondo de la zona inicial)
        pygame.draw.rect(pantalla, (255, 255, 240), (X_PANEL, Y_PANEL, ANCHO_PANEL, ALTO_PANEL))
        pygame.draw.rect(pantalla, (180, 180, 180), (X_PANEL, Y_PANEL, ANCHO_PANEL, ALTO_PANEL), 3)
        
        texto_titulo = fuente_juego.render("PEDIDOS EN COLA", True, (0, 0, 0))
        pantalla.blit(texto_titulo, (X_PANEL + 15, Y_PANEL + 12))
        
        # OBTENER LA POSICIÓN EN TIEMPO REAL DEL RATÓN
        pos_raton = pygame.mouse.get_pos()
        
        # ACTUALIZAR LA POSICIÓN DE LA TARJETA QUE SE ESTÁ ARRASTRANDO
        if tarjeta_seleccionada is not None:
            tarjeta_seleccionada.tarjeta_x = pos_raton[0] - offset_x
            tarjeta_seleccionada.tarjeta_y = pos_raton[1] - offset_y
        
        # === DIBUJAR TARJETAS EN ORDEN CRONOLÓGICO (Una debajo de otra) ===
        # Iteramos de forma normal (0, 1, 2...) para mantener el orden secuencial estricto
        for idx_real, cliente in enumerate(cola_clientes):
            
        #     # Si el cliente está siendo arrastrado, saltamos su renderizado temporalmente
        #     # para dibujarlo al final (así siempre quedará por encima de las demás tarjetas)

            if cliente == tarjeta_seleccionada:
                continue
                
            # ➔ 1. SEPARAR EL TEXTO DEL PEDIDO EN LÍNEAS
            texto_pedido_completo = f"Pedido: {cliente.pedido}"
            palabras = texto_pedido_completo.split(' ')
            lineas_pedido = []
            linea_actual = ""
            
            for palabra in palabras:
                test_linea = linea_actual + palabra + " "
                if fuente_dinamica.size(test_linea)[0] < ANCHO_MAX_TEXTO_TARJETA:
                    linea_actual = test_linea
                else:
                    lineas_pedido.append(linea_actual.strip())
                    linea_actual = palabra + " "
            lineas_pedido.append(linea_actual.strip())
            
            # ➔ 2. CALCULAR EL ALTO DE LA TARJETA
            total_lineas = 1 + len(lineas_pedido)
            alto_t = (fuente_dinamica.get_linesize() * total_lineas) + 12
            
            # Fondo blanco puro del papel
            pygame.draw.rect(pantalla, (255, 255, 255), (cliente.tarjeta_x, cliente.tarjeta_y, ANCHO_TARJETA, alto_t))
            
            # Borde del papel (Gris normal)
            pygame.draw.rect(pantalla, (210, 210, 210), (cliente.tarjeta_x, cliente.tarjeta_y, ANCHO_TARJETA, alto_t), 1)
            
            # ➔ 3. ESTAMPAR EL NOMBRE
            texto_nombre = f"{idx_real + 1}. {cliente.nombre}"
            render_nombre = fuente_dinamica.render(texto_nombre, True, (40, 40, 40))
            pantalla.blit(render_nombre, (cliente.tarjeta_x + 12, cliente.tarjeta_y + 6))
            
            # ➔ 4. ESTAMPAR LAS LÍNEAS DEL PEDIDO
            y_renglon = cliente.tarjeta_y + 6 + fuente_dinamica.get_linesize()
            for linea in lineas_pedido:
                render_pedido = fuente_dinamica.render(linea, True, (90, 90, 90))
                pantalla.blit(render_pedido, (cliente.tarjeta_x + 12, y_renglon))
                y_renglon += fuente_dinamica.get_linesize()

        # ➔ 4B. DIBUJAR LA TARJETA SELECCIONADA POR ENCIMA DE TODO
        if tarjeta_seleccionada is not None:
            texto_pedido_completo = f"Pedido: {tarjeta_seleccionada.pedido}"
            palabras = texto_pedido_completo.split(' ')
            lineas_pedido = []
            linea_actual = ""
            
            for palabra in palabras:
                test_linea = linea_actual + palabra + " "
                if fuente_dinamica.size(test_linea)[0] < ANCHO_MAX_TEXTO_TARJETA:
                    linea_actual = test_linea
                else:
                    lineas_pedido.append(linea_actual.strip())
                    linea_actual = palabra + " "
            lineas_pedido.append(linea_actual.strip())
            
            total_lineas = 1 + len(lineas_pedido)
            alto_t = (fuente_dinamica.get_linesize() * total_lineas) + 12
            
            pygame.draw.rect(pantalla, (255, 255, 255), (tarjeta_seleccionada.tarjeta_x, tarjeta_seleccionada.tarjeta_y, ANCHO_TARJETA, alto_t))
            pygame.draw.rect(pantalla, (150, 150, 250), (tarjeta_seleccionada.tarjeta_x, tarjeta_seleccionada.tarjeta_y, ANCHO_TARJETA, alto_t), 2)
            
            texto_nombre = f"{cola_clientes.index(tarjeta_seleccionada) + 1}. {tarjeta_seleccionada.nombre}"
            render_nombre = fuente_dinamica.render(texto_nombre, True, (40, 40, 40))
            pantalla.blit(render_nombre, (tarjeta_seleccionada.tarjeta_x + 12, tarjeta_seleccionada.tarjeta_y + 6))
            
            y_renglon = tarjeta_seleccionada.tarjeta_y + 6 + fuente_dinamica.get_linesize()
            for linea in lineas_pedido:
                render_pedido = fuente_dinamica.render(linea, True, (90, 90, 90))
                pantalla.blit(render_pedido, (tarjeta_seleccionada.tarjeta_x + 12, y_renglon))
                y_renglon += fuente_dinamica.get_linesize()
                
        # === MANEJO DE EVENTOS ===
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if evento.button == 1:

                    rect_boton_volver = pygame.Rect(X_BOTON_VOLVER, Y_BOTON_VOLVER, ANCHO_BOTON_VOLVER, ALTO_BOTON_VOLVER)
                    if rect_boton_volver.collidepoint(pos_raton):
                        jugando = False  # Rompe el bucle while y permite regresar al menú
                        continue

                    # Buscamos de adelante hacia atrás para agarrar la tarjeta que esté más arriba en pantalla
                    for cliente in cola_clientes:
                        texto_p = f"Pedido: {cliente.pedido}"
                        palabras = texto_p.split(' ')
                        lineas_count = 1
                        l_act = ""
                        for p in palabras:
                            if fuente_dinamica.size(l_act + p + " ")[0] < ANCHO_MAX_TEXTO_TARJETA:
                                l_act += p + " "
                            else:
                                lineas_count += 1
                                l_act = p + " "
                        
                        alto_t = (fuente_dinamica.get_linesize() * (1 + lineas_count)) + 12
                        rect_tarjeta = pygame.Rect(cliente.tarjeta_x, cliente.tarjeta_y, ANCHO_TARJETA, alto_t)
                        
                        if rect_tarjeta.collidepoint(pos_raton):
                            tarjeta_seleccionada = cliente
                            offset_x = pos_raton[0] - cliente.tarjeta_x
                            offset_y = pos_raton[1] - cliente.tarjeta_y
                            break
            
            if evento.type == pygame.MOUSEBUTTONUP:
                if evento.button == 1:
                    tarjeta_seleccionada = None
                
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_c:
                    nuevo_cliente = Cliente(800, 300)
                    posicion_en_cola = len(cola_clientes)
                    nuevo_cliente.posicion_destino = X_MOSTRADOR + (posicion_en_cola * DISTANCIA_ENTRE_CLIENTES)
                    
                    # ➔ 5. CÁLCULO DINÁMICO DE POSICIÓN VERTICAL INICIAL (Evita que se pisen)
                    # Calculamos cuánto espacio ocupan las tarjetas que ya están en la lista
                    y_acumulado = Y_PANEL + 45
                    for c_existente in cola_clientes:
                        texto_p = f"Pedido: {c_existente.pedido}"
                        palabras = texto_p.split(' ')
                        lineas_count = 1
                        l_act = ""
                        for p in palabras:
                            if fuente_dinamica.size(l_act + p + " ")[0] < ANCHO_MAX_TEXTO_TARJETA:
                                l_act += p + " "
                            else:
                                lineas_count += 1
                                l_act = p + " "
                        alto_t = (fuente_dinamica.get_linesize() * (1 + lineas_count)) + 12
                        y_acumulado += alto_t + 10 # 10px de separación entre tarjetas
                    
                    nuevo_cliente.tarjeta_x = X_PANEL + 10
                    nuevo_cliente.tarjeta_y = y_acumulado
                    
                    cola_clientes.append(nuevo_cliente)
                    
        # Actualizar y dibujar a cada cliente físico 
        for cliente in cola_clientes:
            cliente.actualizar()
            cliente.dibujar(pantalla, fuente_juego)
            
            if cliente.estado == "enojado":
                print(f"{cliente.nombre} se cansó de esperar y se fue.")
                cola_clientes.remove(cliente)
                
                # Reajustar destinos de fila física
                for i, c_restante in enumerate(cola_clientes):
                    c_restante.posicion_destino = X_MOSTRADOR + (i * DISTANCIA_ENTRE_CLIENTES)

        pygame.display.update()
        reloj.tick(60)

if __name__ == "__main__":
    menu_principal()









