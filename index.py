

import pygame
import sys
import script
from cliente import Cliente
from style import styles as style

# Configuración inicial
pygame.init()
style.init_fonts()
ANCHO, ALTO = 800, 600
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Papa's Sushi")

boton_nuevo_rect = pygame.Rect(200, 200, 250, 50)
boton_cargar_rect = pygame.Rect(200, 300, 250, 50)

def dibujar_texto(texto, fuente, color, x, y):
    style.draw_text(pantalla, texto, fuente, color, x, y)

def menu_principal():
    reloj = pygame.time.Clock()
    
    while True:
        pantalla.fill(style.SKY_BLUE)
        
        # Obtener posición del mouse
        mouse_pos = pygame.mouse.get_pos()
        
        # Título del Juego
        dibujar_texto("PAPA'S SUSHI", style.FONT_TITLE, style.TEXT_DARK, 180, 150)
        
        # Botón "PLAY"
        boton_rect = pygame.Rect(300, 350, 200, 60)
        
        style.draw_button(pantalla, "START GAME", boton_rect, style.SUSHI_ORANGE, style.SUSHI_ORANGE_HOVER, mouse_pos)

        # Manejo de eventos
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if boton_rect.collidepoint(mouse_pos):
                    iniciar_juego()

        pygame.display.update()
        reloj.tick(60)

def iniciar_juego():
    corriendo = True
    while corriendo:
        mouse_pos = pygame.mouse.get_pos()
        pantalla.fill(style.WHITE)
        
        # Dibujamos los botones
        style.draw_button(pantalla, "NUEVA PARTIDA", boton_nuevo_rect, style.BUTTON_GREEN, style.BUTTON_GREEN_HOVER, mouse_pos)
        style.draw_button(pantalla, "CARGAR PARTIDA", boton_cargar_rect, style.BUTTON_GREEN, style.BUTTON_GREEN_HOVER, mouse_pos)
        
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
    fuente = style.FONT_INPUT
    
    while escribiendo:
        pantalla.fill(style.WHITE) # Fondo blanco
        
        # Dibujar las instrucciones y lo que el usuario va escribiendo
        txt_titulo = fuente.render(titulo, True, style.BLACK)
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

def mostrar_mensaje(pantalla, texto, color=style.BLACK):
    """Función auxiliar para dibujar texto centrado rápidamente"""
    fuente = pygame.font.Font(None, 36)
    pantalla.fill(style.WHITE)  # Limpia la pantalla (puedes usar una imagen de fondo)
    
    superficie_texto = fuente.render(texto, True, color)
    rect_texto = superficie_texto.get_rect(center=(pantalla.get_width() // 2, pantalla.get_height() // 2))
    
    pantalla.blit(superficie_texto, rect_texto)
    pygame.display.flip()
    pygame.time.delay(2000) # Pausa de 2 segundos para que el usuario lea

def bucle_restaurante():
    
    reloj = pygame.time.Clock()
    fuente_juego = style.FONT_GAME
    fuente_dinamica = style.FONT_DYNAMIC
   
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
    
    # MEDIDAS PARA LA TARJETA
    ANCHO_TARJETA = 380 
    
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
        pygame.draw.rect(pantalla, color_borde, (X_BOTON_VOLVER, Y_BOTON_VOLVER, ANCHO_BOTON_VOLVER, ALTO_BOTON_VOLVER), width=2, border_radius=17)
    
        texto_volver = fuente_juego.render("VOLVER AL MENÚ", True, (0, 0, 0))
        pantalla.blit(texto_volver, (X_BOTON_VOLVER + 15, Y_BOTON_VOLVER + 7))
        
        # PANEL CONTENEDOR DE PEDIDOS
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
        
        # === DIBUJAR TARJETAS EN ORDEN CRONOLÓGICO ===
        for idx_real, cliente in enumerate(cola_clientes):
            if cliente == tarjeta_seleccionada:
                continue
                
            # ➔ 1. PROCESAR EL PEDIDO DESDE EL DICCIONARIO
            # Convertimos el diccionario en líneas legibles estilo factura (ej: "1x Arroz" o solo "Arroz")
            lineas_pedido = []
            if isinstance(cliente.pedido, dict):
                for ingrediente, cantidad in cliente.pedido.items():
                    lineas_pedido.append(f"{cantidad}x {ingrediente}")
            else:
                # Por si acaso algún cliente viejo aún tiene formato string
                lineas_pedido = [str(cliente.pedido)]
            
            # ➔ 2. CALCULAR EL ALTO DE LA TARJETA
            total_lineas = 2 + len(lineas_pedido)
            alto_t = (fuente_dinamica.get_linesize() * total_lineas) + 20
            
            # Fondo blanco del ticket
            pygame.draw.rect(pantalla, (255, 255, 255), (cliente.tarjeta_x, cliente.tarjeta_y, ANCHO_TARJETA, alto_t))
            pygame.draw.rect(pantalla, (210, 210, 210), (cliente.tarjeta_x, cliente.tarjeta_y, ANCHO_TARJETA, alto_t), 1)
            
            # Línea punteada decorativa superior
            pygame.draw.line(pantalla, (180, 180, 180), (cliente.tarjeta_x + 10, cliente.tarjeta_y + 30), (cliente.tarjeta_x + ANCHO_TARJETA - 10, cliente.tarjeta_y + 30), 1)
            
            # ➔ 3. ESTAMPAR EL NOMBRE / ID DEL TICKET
            texto_nombre = f"TICKET #{idx_real + 1} - {cliente.nombre.upper()}"
            render_nombre = fuente_dinamica.render(texto_nombre, True, (0, 0, 0))
            pantalla.blit(render_nombre, (cliente.tarjeta_x + 12, cliente.tarjeta_y + 8))
            
            # Encabezado del detalle
            render_detalle = fuente_dinamica.render("DETALLE DEL PEDIDO:", True, (120, 120, 120))
            pantalla.blit(render_detalle, (cliente.tarjeta_x + 12, cliente.tarjeta_y + 38))
            
            # ➔ 4. ESTAMPAR CADA ELEMENTO DEL DICCIONARIO ABAJO DEL ANTERIOR
            y_renglon = cliente.tarjeta_y + 38 + fuente_dinamica.get_linesize()
            for linea in lineas_pedido:
                render_pedido = fuente_dinamica.render(f"  • {linea}", True, (50, 50, 50))
                pantalla.blit(render_pedido, (cliente.tarjeta_x + 12, y_renglon))
                y_renglon += fuente_dinamica.get_linesize()

        # ➔ 4B. DIBUJAR LA TARJETA SELECCIONADA POR ENCIMA DE TODO (ARRASTRÁNDOSE)
        if tarjeta_seleccionada is not None:
            lineas_pedido = []
            if isinstance(tarjeta_seleccionada.pedido, dict):
                for ingrediente, cantidad in tarjeta_seleccionada.pedido.items():
                    lineas_pedido.append(f"{cantidad}x {ingrediente}")
            else:
                lineas_pedido = [str(tarjeta_seleccionada.pedido)]
            
            total_lineas = 2 + len(lineas_pedido)
            alto_t = (fuente_dinamica.get_linesize() * total_lineas) + 20
            
            pygame.draw.rect(pantalla, (255, 255, 255), (tarjeta_seleccionada.tarjeta_x, tarjeta_seleccionada.tarjeta_y, ANCHO_TARJETA, alto_t))
            pygame.draw.rect(pantalla, (100, 149, 237), (tarjeta_seleccionada.tarjeta_x, tarjeta_seleccionada.tarjeta_y, ANCHO_TARJETA, alto_t), 2)
            
            pygame.draw.line(pantalla, (100, 149, 237), (tarjeta_seleccionada.tarjeta_x + 10, tarjeta_seleccionada.tarjeta_y + 30), (tarjeta_seleccionada.tarjeta_x + ANCHO_TARJETA - 10, tarjeta_seleccionada.tarjeta_y + 30), 1)
            
            texto_nombre = f"TICKET #{cola_clientes.index(tarjeta_seleccionada) + 1} - {tarjeta_seleccionada.nombre.upper()}"
            render_nombre = fuente_dinamica.render(texto_nombre, True, (0, 0, 0))
            pantalla.blit(render_nombre, (tarjeta_seleccionada.tarjeta_x + 12, tarjeta_seleccionada.tarjeta_y + 8))
            
            render_detalle = fuente_dinamica.render("DETALLE DEL PEDIDO:", True, (120, 120, 120))
            pantalla.blit(render_detalle, (tarjeta_seleccionada.tarjeta_x + 12, tarjeta_seleccionada.tarjeta_y + 38))
            
            y_renglon = tarjeta_seleccionada.tarjeta_y + 38 + fuente_dinamica.get_linesize()
            for linea in lineas_pedido:
                render_pedido = fuente_dinamica.render(f"  • {linea}", True, (50, 50, 50))
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
                        jugando = False
                        continue

                    for cliente in cola_clientes:
                        if isinstance(cliente.pedido, dict):
                            lineas_count = len(cliente.pedido)
                        else:
                            lineas_count = 1
                        
                        alto_t = (fuente_dinamica.get_linesize() * (2 + lineas_count)) + 20
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
                    
                    # ➔ 5. CÁLCULO DINÁMICO DE POSICIÓN VERTICAL INICIAL PARA DICCIONARIOS
                    y_acumulado = Y_PANEL + 45
                    for c_existente in cola_clientes:
                        if isinstance(c_existente.pedido, dict):
                            lineas_count = len(c_existente.pedido)
                        else:
                            lineas_count = 1
                        alto_t = (fuente_dinamica.get_linesize() * (2 + lineas_count)) + 20
                        y_acumulado += alto_t + 12 
                    
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









