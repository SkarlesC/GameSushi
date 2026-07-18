

import pygame
from style import styles as style

# Dispensadores de bebidas
RECT_TE_VERDE = pygame.Rect(60, 180, 140, 120)
RECT_SAKE = pygame.Rect(230, 180, 140, 120)

def mostrar_tea(pantalla, fuente_juego, fuente_dinamica, tiene_sushi):
    """Dibuja la máquina de bebidas y la tabla de corte final"""
    # style.draw_text(pantalla, "ESTACIÓN DE CORTE Y BEBIDAS (TEA STATION)", style.FONT_TITLE, style.TEXT_DARK, 30, 75)
    
    # Render de la Tabla de picar madera
    pygame.draw.rect(pantalla, (222, 184, 135), (40, 150, 180, 150), border_radius=10)
    pygame.draw.rect(pantalla, (139, 69, 19), (40, 150, 180, 150), width=3, border_radius=10)
    
    if tiene_sushi:
        pygame.draw.rect(pantalla, (46, 139, 87), (60, 200, 140, 50), border_radius=5)
        style.draw_text(pantalla, "Presiona [ESPACIO]", fuente_dinamica, style.BLACK, 55, 160)
        style.draw_text(pantalla, "para cortar el rollo", fuente_dinamica, style.BLACK, 52, 180)
    else:
        style.draw_text(pantalla, "Trae un sushi de Build", fuente_dinamica, (150, 0, 0), 50, 210)

    # Render de las Máquinas de Líquidos
    style.draw_text(pantalla, "Servir Bebida del Cliente:", fuente_juego, style.TEXT_DARK, 250, 150)
    
    # Máquina Té Verde
    pygame.draw.rect(pantalla, (143, 188, 143), RECT_TE_VERDE, border_radius=5)
    pygame.draw.rect(pantalla, style.BLACK, RECT_TE_VERDE, width=2, border_radius=5)
    style.draw_text(pantalla, "Té Verde", fuente_dinamica, style.BLACK, RECT_TE_VERDE.x + 35, RECT_TE_VERDE.y + 50)
    
    # Máquina Sake / Líquido dulce
    pygame.draw.rect(pantalla, (175, 238, 238), RECT_SAKE, border_radius=5)
    pygame.draw.rect(pantalla, style.BLACK, RECT_SAKE, width=2, border_radius=5)
    style.draw_text(pantalla, "Sake Líquido", fuente_dinamica, style.BLACK, RECT_SAKE.x + 25, RECT_SAKE.y + 50)

def gestionar_clic_tea(pos_raton, bebida_actual):
    """Devuelve la bebida seleccionada si se presionan los dispensadores"""
    if RECT_TE_VERDE.collidepoint(pos_raton):
        return "Te Verde"
    elif RECT_SAKE.collidepoint(pos_raton):
        return "Sake Liquido"
    return bebida_actual
