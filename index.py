

import pygame
import sys
import script
from cliente import Cliente, Ticket
from style import styles as style


import estacion_order
import estacion_cook
import estacion_build
import estacion_tea


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
        
        style.draw_button(pantalla, "NUEVA PARTIDA", boton_nuevo_rect, style.BUTTON_BLUE, style.BUTTON_BLUE_HOVER, mouse_pos)
        style.draw_button(pantalla, "CARGAR PARTIDA", boton_cargar_rect, style.BUTTON_GREEN, style.BUTTON_GREEN_HOVER, mouse_pos)
        
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                corriendo = False
                pygame.quit()
                exit()
            
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if evento.button == 1: 
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
    tickets = []
    MAX_TICKETS = 10
    X_MOSTRADOR = 150
    DISTANCIA_ENTRE_CLIENTES = 70

    ticket_arrastrando = None
    ticket_vistiendo = None

    X_BOTON_VOLVER = 20
    Y_BOTON_VOLVER = 20
    ANCHO_BOTON_VOLVER = 150
    ALTO_BOTON_VOLVER = 35

    estacion_actual = "MOSTRADOR"
    ingredientes_sushi_actual = []
    bebida_actual = "Ninguna"

    ancho_btn_estacion = 140
    alto_btn_estacion = 30
    y_btn_estacion = 540

    btn_mostrador_rect = pygame.Rect(15, y_btn_estacion, ancho_btn_estacion, alto_btn_estacion)
    btn_recepcion_rect = pygame.Rect(170, y_btn_estacion, ancho_btn_estacion, alto_btn_estacion)
    btn_arroz_rect     = pygame.Rect(325, y_btn_estacion, ancho_btn_estacion, alto_btn_estacion)
    btn_relleno_rect   = pygame.Rect(480, y_btn_estacion, ancho_btn_estacion, alto_btn_estacion)
    btn_corte_rect     = pygame.Rect(635, y_btn_estacion, ancho_btn_estacion, alto_btn_estacion)

    jugando = True
    while jugando:
        pantalla.fill(style.BACKGROUND_WARM)
        pos_raton = pygame.mouse.get_pos()

        # Siempre dibujar la linea de pedidos arriba
        estacion_order.dibujar_linea_pedidos(pantalla, tickets, fuente_juego)

        # MOSTRADOR: dibujar clientes + ticket pendiente
        if estacion_actual == "MOSTRADOR":
            estacion_order.mostrar_order(pantalla, fuente_juego, cola_clientes)

            # Dibujar ticket pendiente (grande a la derecha)
            for ticket in tickets:
                if ticket.estado == "pendiente":
                    ticket.dibujar(pantalla, fuente_dinamica)

            # Dibujar indicador de zona de colgado
            if ticket_arrastrando:
                pygame.draw.rect(pantalla, (50, 200, 50, 60),
                                 (0, 0, 800, Ticket.ZONA_LINEA_Y), 3)

        # Otras estaciones: dibujar area de lectura si hay ticket vistiendo
        elif estacion_actual in ["RECEPCION", "ARROZ", "RELLENO", "CORTE"]:
            if estacion_actual == "RECEPCION":
                dibujar_texto("PEDIDOS EN COLA", fuente_juego, (80, 80, 80), 30, 155)
            elif estacion_actual == "ARROZ":
                estacion_cook.mostrar_cook(pantalla, fuente_juego)
            elif estacion_actual == "RELLENO":
                estacion_build.mostrar_build(pantalla, fuente_juego)
            elif estacion_actual == "CORTE":
                tiene_sushi = len(ingredientes_sushi_actual) > 0
                estacion_tea.mostrar_tea(pantalla, fuente_juego, fuente_dinamica, tiene_sushi)

            # Dibujar ticket vistiendo (area de lectura)
            if ticket_vistiendo and ticket_vistiendo.estado == "vistiendo":
                ticket_vistiendo.dibujar(pantalla, fuente_dinamica)

        # Barra de preparacion
        pygame.draw.rect(pantalla, style.PANEL_DARK_BG, (30, 460, 740, 40), border_radius=8)
        pygame.draw.rect(pantalla, style.BUTTON_BLUE_HOVER, (30, 460, 740, 40), 1, border_radius=8)
        texto_preparacion = f"Esterilla: {' + '.join(ingredientes_sushi_actual) if ingredientes_sushi_actual else 'Vacia' }  |  Bebida: {bebida_actual}"
        dibujar_texto(texto_preparacion, fuente_juego, (220, 220, 220), 45, 470)

        # Boton Volver
        pygame.draw.rect(pantalla, (180, 50, 50), (X_BOTON_VOLVER, Y_BOTON_VOLVER, ANCHO_BOTON_VOLVER, ALTO_BOTON_VOLVER), border_radius=17)
        pygame.draw.rect(pantalla, (140, 30, 30), (X_BOTON_VOLVER, Y_BOTON_VOLVER, ANCHO_BOTON_VOLVER, ALTO_BOTON_VOLVER), width=2, border_radius=17)
        dibujar_texto("VOLVER AL MENU", fuente_juego, (255, 255, 255), X_BOTON_VOLVER + 18, Y_BOTON_VOLVER + 7)

        # Botones de estacion
        color_mostrador = style.BUTTON_GREEN if estacion_actual == "MOSTRADOR" else style.BUTTON_BLUE
        color_recepcion = style.BUTTON_GREEN if estacion_actual == "RECEPCION" else style.BUTTON_BLUE
        color_arroz     = style.BUTTON_GREEN if estacion_actual == "ARROZ" else style.BUTTON_BLUE
        color_relleno   = style.BUTTON_GREEN if estacion_actual == "RELLENO" else style.BUTTON_BLUE
        color_corte     = style.BUTTON_GREEN if estacion_actual == "CORTE" else style.BUTTON_BLUE

        style.draw_button(pantalla, "MOSTRADOR", btn_mostrador_rect, color_mostrador, style.BUTTON_BLUE_HOVER, pos_raton)
        style.draw_button(pantalla, "RECEPCION", btn_recepcion_rect, color_recepcion, style.BUTTON_BLUE_HOVER, pos_raton)
        style.draw_button(pantalla, "EST. ARROZ", btn_arroz_rect, color_arroz, style.BUTTON_BLUE_HOVER, pos_raton)
        style.draw_button(pantalla, "EST. RELLENO", btn_relleno_rect, color_relleno, style.BUTTON_BLUE_HOVER, pos_raton)
        style.draw_button(pantalla, "EST. CORTE", btn_corte_rect, color_corte, style.BUTTON_BLUE_HOVER, pos_raton)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if evento.type == pygame.MOUSEBUTTONDOWN:
                if evento.button == 1:
                    # Boton volver
                    rect_boton_volver = pygame.Rect(X_BOTON_VOLVER, Y_BOTON_VOLVER, ANCHO_BOTON_VOLVER, ALTO_BOTON_VOLVER)
                    if rect_boton_volver.collidepoint(pos_raton):
                        jugando = False
                        continue

                    # Botones de estacion
                    if btn_mostrador_rect.collidepoint(pos_raton):
                        # Cerrar lectura al cambiar de estacion
                        if ticket_vistiendo:
                            ticket_vistiendo.cerrar_lectura()
                            ticket_vistiendo = None
                        estacion_actual = "MOSTRADOR"
                    elif btn_recepcion_rect.collidepoint(pos_raton):
                        if ticket_vistiendo:
                            ticket_vistiendo.cerrar_lectura()
                            ticket_vistiendo = None
                        estacion_actual = "RECEPCION"
                    elif btn_arroz_rect.collidepoint(pos_raton):
                        if ticket_vistiendo:
                            ticket_vistiendo.cerrar_lectura()
                            ticket_vistiendo = None
                        estacion_actual = "ARROZ"
                    elif btn_relleno_rect.collidepoint(pos_raton):
                        if ticket_vistiendo:
                            ticket_vistiendo.cerrar_lectura()
                            ticket_vistiendo = None
                        estacion_actual = "RELLENO"
                    elif btn_corte_rect.collidepoint(pos_raton):
                        if ticket_vistiendo:
                            ticket_vistiendo.cerrar_lectura()
                            ticket_vistiendo = None
                        estacion_actual = "CORTE"

                    # === MOSTRADOR: Drag de tickets pendientes ===
                    elif estacion_actual == "MOSTRADOR":
                        for ticket in tickets:
                            if ticket.estado == "pendiente" and ticket.rect_pendiente().collidepoint(pos_raton):
                                ticket_arrastrando = ticket
                                ticket.dragging = True
                                ticket.offset_drag_x = pos_raton[0] - ticket.x
                                ticket.offset_drag_y = pos_raton[1] - ticket.y
                                break

                    # === OTRAS ESTACIONES: Click en ticket colgado para ver ===
                    elif estacion_actual in ["RECEPCION", "ARROZ", "RELLENO", "CORTE"]:
                        # Si ya hay uno vistiendo, verificar si el clic es fuera para cerrar
                        if ticket_vistiendo and ticket_vistiendo.estado == "vistiendo":
                            if not ticket_vistiendo.rect_lectura().collidepoint(pos_raton):
                                ticket_vistiendo.cerrar_lectura()
                                ticket_vistiendo = None
                            continue

                        # Buscar clic en un ticket colgado en la linea
                        for ticket in tickets:
                            if ticket.estado == "colgado" and ticket.rect_colgado().collidepoint(pos_raton):
                                ticket.ver_pedido()
                                ticket_vistiendo = ticket
                                break

                    # Clicks en estaciones especificas
                    if estacion_actual == "ARROZ":
                        estacion_cook.gestionar_clic_cook(pos_raton, ingredientes_sushi_actual)
                    elif estacion_actual == "RELLENO":
                        estacion_build.gestionar_clic_build(pos_raton, ingredientes_sushi_actual)
                    elif estacion_actual == "CORTE":
                        bebida_actual = estacion_tea.gestionar_clic_tea(pos_raton, bebida_actual)

            if evento.type == pygame.MOUSEBUTTONUP:
                if evento.button == 1:
                    # Soltar ticket arrastrando
                    if ticket_arrastrando and ticket_arrastrando.dragging:
                        ticket_arrastrando.dragging = False
                        # Si se suelta en la zona de la linea, colgarlo
                        if ticket_arrastrando.y < Ticket.ZONA_LINEA_Y:
                            ticket_arrastrando.colgar()
                        else:
                            ticket_arrastrando.volver_a_pendiente()
                        ticket_arrastrando = None

            if evento.type == pygame.MOUSEMOTION:
                # Arrastrar ticket pendiente
                if ticket_arrastrando and ticket_arrastrando.dragging:
                    ticket_arrastrando.x = pos_raton[0] - ticket_arrastrando.offset_drag_x
                    ticket_arrastrando.y = pos_raton[1] - ticket_arrastrando.offset_drag_y

            if evento.type == pygame.KEYDOWN:
                # Presiona C para spawnear cliente nuevo
                if evento.key == pygame.K_c:
                    if len(tickets) >= MAX_TICKETS:
                        pass
                    else:
                        nuevo_cliente = Cliente(800, 300)
                        posicion_en_cola = len(cola_clientes)
                        nuevo_cliente.posicion_destino = X_MOSTRADOR + (posicion_en_cola * DISTANCIA_ENTRE_CLIENTES)

                        nuevo_ticket = Ticket(nuevo_cliente, len(tickets))
                        tickets.append(nuevo_ticket)
                        cola_clientes.append(nuevo_cliente)

                # Presiona ESPACIO para entregar comida
                if estacion_actual == "CORTE" and evento.key == pygame.K_SPACE:
                    if len(ingredientes_sushi_actual) > 0:
                        comida_lista = set(ingredientes_sushi_actual)
                        cliente_atendido = None

                        for c in cola_clientes:
                            if c.estado == "esperando" and c.pedido == comida_lista:
                                cliente_atendido = c
                                break

                        if cliente_atendido:
                            cola_clientes.remove(cliente_atendido)
                            for t in tickets:
                                if t.cliente == cliente_atendido:
                                    if ticket_vistiendo == t:
                                        ticket_vistiendo = None
                                    tickets.remove(t)
                                    break
                            for i, t in enumerate(tickets):
                                t.actualizar_posicion_slot(i, len(tickets))
                        else:
                            print("Ningun cliente pidio esta combinacion. Sushi tirado!")

                        for i, c_restante in enumerate(cola_clientes):
                            c_restante.posicion_destino = X_MOSTRADOR + (i * DISTANCIA_ENTRE_CLIENTES)

                        ingredientes_sushi_actual = []
                        bebida_actual = "Ninguna"

        # Remover clientes enojados
        for cliente in cola_clientes[:]:
            if cliente.estado == "enojado":
                cola_clientes.remove(cliente)
                for t in tickets:
                    if t.cliente == cliente:
                        if ticket_vistiendo == t:
                            ticket_vistiendo = None
                        if ticket_arrastrando == t:
                            ticket_arrastrando = None
                        tickets.remove(t)
                        break
                for i, t in enumerate(tickets):
                    t.actualizar_posicion_slot(i, len(tickets))
                for i, c_restante in enumerate(cola_clientes):
                    c_restante.posicion_destino = X_MOSTRADOR + (i * DISTANCIA_ENTRE_CLIENTES)

        pygame.display.update()
        reloj.tick(60)
       
if __name__ == "__main__":
    menu_principal()
