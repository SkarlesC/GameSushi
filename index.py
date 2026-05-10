

import pygame
import sys
import script

# Configuración inicial
pygame.init()
ANCHO, ALTO = 800, 600
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Papa's Sushiria")

# Colores y Fuentes
BLANCO = (255, 255, 255)
NARANJA_PAPA = (255, 128, 0) # Un color vibrante tipo arcade
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
        dibujar_texto("PAPA'S SUSHIRIA", fuente_titulo, (50, 50, 50), 180, 150)
        
        # Botón "PLAY"
        boton_rect = pygame.Rect(300, 350, 200, 60)
        
        # Efecto "hover" (si el mouse está encima, cambia de color)
        color_boton = (200, 100, 0) if boton_rect.collidepoint(mouse_pos) else NARANJA_PAPA
        
        pygame.draw.rect(pantalla, color_boton, boton_rect, border_radius=12)
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
                        nombre = pedir_nombre_en_pantalla("Introduce tu nombre de jugador:")
                        script.nuevo(nombre)
                        mostrar_mensaje(pantalla, f"¡Bienvenido {nombre}! Guardando...", (0, 0, 150))
                        corriendo = False
                        
                    elif boton_cargar_rect.collidepoint(mouse_pos):
                        # Lógica de CARGAR PARTIDA
                        nombre = pedir_nombre_en_pantalla("Usuario a cargar:")
                        result = script.cargar(nombre)
                        if result is None:
                            mostrar_mensaje(pantalla, "Error: Ese usuario no es válido.", (200, 0, 0))
                        else:
                            mostrar_mensaje(pantalla, f"Cargando partida de {nombre}...", (0, 128, 0))
                            corriendo = False

            # --- DETECCIÓN POR TECLADO ---
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_1:
                    nombre = pedir_nombre_en_pantalla("Introduce tu nombre de jugador:")
                    script.nuevo(nombre)
                    mostrar_mensaje(pantalla, f"¡Bienvenido {nombre}! Guardando...", (0, 0, 150))
                    corriendo = False
                elif evento.key == pygame.K_2:
                    nombre = pedir_nombre_en_pantalla("Usuario a cargar:")
                    result = script.cargar(nombre)
                    if result is None:
                        mostrar_mensaje(pantalla, "Error: Ese usuario no es válido.", (200, 0, 0))
                    else:
                        mostrar_mensaje(pantalla, f"Cargando partida de {nombre}...", (0, 128, 0))
                        corriendo = False
        
        pygame.display.update()

def pedir_nombre_en_pantalla(titulo):
    nombre = ""
    escribiendo = True
    fuente = pygame.font.Font(None, 40)
    
    while escribiendo:
        pantalla.fill((255, 255, 255)) # Fondo blanco
        
        # Dibujar las instrucciones y lo que el usuario va escribiendo
        txt_titulo = fuente.render(titulo, True, (0, 0, 0))
        txt_nombre = fuente.render(nombre + "|", True, (0, 0, 255)) # Azul para el nombre
        
        pantalla.blit(txt_titulo, (100, 150))
        pantalla.blit(txt_nombre, (100, 200))
        
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()
            
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN: # Al presionar ENTER
                    escribiendo = False
                elif evento.key == pygame.K_BACKSPACE: # Borrar letra
                    nombre = nombre[:-1]
                else:
                    # Solo agregar si es un caracter imprimible (letras/números)
                    if len(evento.unicode) > 0:
                        nombre += evento.unicode
        
        pygame.display.update()
    
    return nombre if nombre != "" else "Cocinero"

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


if __name__ == "__main__":
    menu_principal()