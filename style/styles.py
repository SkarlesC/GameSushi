import pygame

# Colores principales
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
SKY_BLUE = (200, 230, 255)
SUSHI_ORANGE = (255, 128, 0)
SUSHI_ORANGE_HOVER = (200, 100, 0)
BUTTON_GREEN = (50, 150, 50)
BUTTON_GREEN_HOVER = (70, 200, 70)
ERROR_RED = (200, 0, 0)
SUCCESS_GREEN = (0, 128, 0)
BACKGROUND_GRAY = (240, 240, 240)
MOSTRADOR_BROWN = (139, 69, 19)
BORDER_BROWN = (60, 50, 5)
PANEL_BG = (255, 255, 240)
TICKET_BG = (255, 255, 255)
TICKET_BORDER = (210, 210, 210)
TICKET_LINE = (180, 180, 180)
CARD_HIGHLIGHT = (100, 149, 237)
TEXT_SECONDARY = (120, 120, 120)
TEXT_DARK = (50, 50, 50)

# Fuentes definidas después de inicializar pygame
FONT_TITLE = None
FONT_BUTTON = None
FONT_INPUT = None
FONT_GAME = None
FONT_DYNAMIC = None


def init_fonts():
    global FONT_TITLE, FONT_BUTTON, FONT_INPUT, FONT_GAME, FONT_DYNAMIC
    FONT_TITLE = pygame.font.SysFont("Arial", 60, bold=True)
    FONT_BUTTON = pygame.font.SysFont("Arial", 30)
    FONT_INPUT = pygame.font.Font(None, 40)
    FONT_GAME = pygame.font.SysFont("Arial", 18)
    FONT_DYNAMIC = pygame.font.SysFont(["Segoe UI", "Helvetica", "Arial"], 18)


def draw_text(screen, text, font, color, x, y):
    surface = font.render(text, True, color)
    screen.blit(surface, (x, y))


def draw_button(screen, text, rect, color_default, color_hover, mouse_pos):
    color = color_hover if rect.collidepoint(mouse_pos) else color_default
    pygame.draw.rect(screen, color, rect, border_radius=12)
    pygame.draw.rect(screen, BLACK, rect, 2, border_radius=12)

    text_surface = FONT_BUTTON.render(text, True, WHITE)
    text_rect = text_surface.get_rect(center=rect.center)
    screen.blit(text_surface, text_rect)
