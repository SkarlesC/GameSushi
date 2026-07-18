
import pygame
from style import styles as style

# Hitboxes de los contenedores de ingredientes
RECT_NORI = pygame.Rect(50, 150, 160, 60)
RECT_SALMON = pygame.Rect(230, 150, 160, 60)
RECT_AGUACATE = pygame.Rect(50, 230, 160, 60)
RECT_ATUN = pygame.Rect(230, 230, 160, 60)

def mostrar_build(pantalla, fuente_juego):
    """Dibuja la mesa de trabajo con los ingredientes para armar el rollo"""
    # style.draw_text(pantalla, "BUILD", style.FONT_TITLE, style.TEXT_DARK, 30, 75)
    style.draw_text(pantalla, "Selecciona los rellenos del pedido:", fuente_juego, style.TEXT_DARK, 30, 120)
    
    ingredientes = [
        {"rect": RECT_NORI, "color": (46, 139, 87), "txt": "Alga Nori"},
        {"rect": RECT_SALMON, "color": (250, 128, 114), "txt": "Salmón"},
        {"rect": RECT_AGUACATE, "color": (154, 205, 50), "txt": "Aguacate"},
        {"rect": RECT_ATUN, "color": (220, 20, 60), "txt": "Atún"},
    ]
    
    for ing in ingredientes:
        pygame.draw.rect(pantalla, ing["color"], ing["rect"], border_radius=6)
        pygame.draw.rect(pantalla, style.BLACK, ing["rect"], width=2, border_radius=6)
        style.draw_text(pantalla, ing["txt"], fuente_juego, style.BLACK, ing["rect"].x + 20, ing["rect"].y + 20)

def gestionar_clic_build(pos_raton, ingredientes_sushi):
    """Maneja los clics de los cajones de comida en la pantalla Build"""
    if RECT_NORI.collidepoint(pos_raton):
        ingredientes_sushi.append("Nori")
    elif RECT_SALMON.collidepoint(pos_raton):
        ingredientes_sushi.append("Salmon")
    elif RECT_AGUACATE.collidepoint(pos_raton):
        ingredientes_sushi.append("Aguacate")
    elif RECT_ATUN.collidepoint(pos_raton):
        ingredientes_sushi.append("Atun")
