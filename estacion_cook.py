
import pygame
from style import styles as style

# Hitboxes fijas para los clics en esta ventana
RECT_ARROZ_BLANCO = pygame.Rect(50, 180, 160, 100)
RECT_ARROZ_INTEGRAL = pygame.Rect(240, 180, 160, 100)

def mostrar_cook(pantalla, fuente_juego):
    """Muestra la cocina y las opciones de preparación del arroz"""
    # style.draw_text(pantalla, "COOK STATION", style.FONT_TITLE, style.TEXT_DARK, 30, 70)
    style.draw_text(pantalla, "Haz clic en una olla para cocinar el arroz:", fuente_juego, style.TEXT_DARK, 30, 135)
    
    # Olla de Arroz Blanco
    pygame.draw.rect(pantalla, (235, 235, 235), RECT_ARROZ_BLANCO, border_radius=8)
    pygame.draw.rect(pantalla, (60, 50, 30), RECT_ARROZ_BLANCO, width=2, border_radius=8)
    style.draw_text(pantalla, "Arroz Blanco", fuente_juego, style.BLACK, 75, 220)
    
    # Olla de Arroz Integral
    pygame.draw.rect(pantalla, (222, 184, 135), RECT_ARROZ_INTEGRAL, border_radius=8)
    pygame.draw.rect(pantalla, (60, 50, 30), RECT_ARROZ_INTEGRAL, width=2, border_radius=8)
    style.draw_text(pantalla, "Arroz Integral", fuente_juego, style.BLACK, 255, 220)

def gestionar_clic_cook(pos_raton, ingredientes_sushi):
    """Maneja las interacciones del ratón exclusivas de la pantalla Cook"""
    if RECT_ARROZ_BLANCO.collidepoint(pos_raton):
        ingredientes_sushi.append("Arroz Blanco")
    elif RECT_ARROZ_INTEGRAL.collidepoint(pos_raton):
        ingredientes_sushi.append("Arroz Integral")