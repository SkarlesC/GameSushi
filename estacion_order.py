
import pygame
from style import styles as style


def dibujar_linea_pedidos(pantalla, tickets, fuente):
    """Dibuja la linea horizontal y solo los tickets en estado colgado"""
    # Fondo de la zona de la linea
    pygame.draw.rect(pantalla, (235, 230, 220), (0, 0, 800, 135))

    # Linea principal (cuerda/cable)
    pygame.draw.line(pantalla, style.LINE_CABLE, (30, 30), (770, 30), 3)

    # Soportes en los extremos (clavos grandes)
    pygame.draw.circle(pantalla, style.LINE_SUPPORT, (30, 30), 7)
    pygame.draw.circle(pantalla, (60, 45, 25), (30, 30), 4)
    pygame.draw.circle(pantalla, style.LINE_SUPPORT, (770, 30), 7)
    pygame.draw.circle(pantalla, (60, 45, 25), (770, 30), 4)

    # Etiqueta
    style.draw_text(pantalla, "LINEA DE PEDIDOS", fuente, (150, 130, 110), 320, 115)

    # Dibujar solo tickets colgados
    for ticket in tickets:
        if ticket.estado == "colgado":
            ticket.dibujar(pantalla, fuente)


def mostrar_order(pantalla, fuente_juego, cola_clientes):
    """Renderiza la vista del mostrador con los clientes"""
    # Linea del mostrador de madera
    pygame.draw.rect(pantalla, style.MOSTRADOR_BROWN, (0, 380, 420, 25))
    pygame.draw.rect(pantalla, style.COUNTER_DARK, (0, 380, 420, 25), 2)

    # Texto del mostrador
    style.draw_text(pantalla, "MOSTRADOR DE PEDIDOS", fuente_juego,
                    (255, 255, 255), 20, 415)

    # Actualizar y dibujar a cada cliente en la fila
    for cliente in cola_clientes:
        cliente.actualizar()
        cliente.dibujar(pantalla, fuente_juego)
