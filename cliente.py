

import pygame
import random


class Ticket:
    """Ticket visual con estados: pendiente, colgado, vistiendo"""

    ANCHO_PENDIENTE = 200
    ALTO_PENDIENTE = 250
    ANCHO_COLGADO = 70
    ALTO_COLGADO = 90
    X_PENDIENTE = 560
    Y_PENDIENTE = 50
    Y_LINEA = 35
    ZONA_LINEA_Y = 100
    MARGEN_IZQ = 50
    LIMITE_DERECHO = 750
    X_LECTURA = 550
    Y_LECTURA = 50

    def __init__(self, cliente, slot_index):
        self.cliente = cliente
        self.slot = slot_index
        self.estado = "pendiente"

        # Posicion pendiente (grande, a la derecha)
        self.x = self.X_PENDIENTE
        self.y = self.Y_PENDIENTE
        self.ancho = self.ANCHO_PENDIENTE
        self.alto = self.ALTO_PENDIENTE

        # Posicion destino en la linea
        espacio_total = self.LIMITE_DERECHO - self.MARGEN_IZQ
        self.target_x = self.MARGEN_IZQ + (slot_index * (espacio_total / 10))
        self.target_y = self.Y_LINEA

        # Drag
        self.dragging = False
        self.offset_drag_x = 0
        self.offset_drag_y = 0

        # Colores
        self.color_base = (255, 253, 230)
        self.color_borde = (180, 160, 100)

    def rect_pendiente(self):
        """Rectangulo del ticket cuando esta pendiente (grande)"""
        return pygame.Rect(self.x, self.y, self.ANCHO_PENDIENTE, self.ALTO_PENDIENTE)

    def rect_colgado(self):
        """Rectangulo del ticket cuando esta colgado (pequeno)"""
        return pygame.Rect(self.target_x, self.Y_LINEA, self.ANCHO_COLGADO, self.ALTO_COLGADO)

    def rect_lectura(self):
        """Rectangulo del ticket en modo lectura (grande)"""
        return pygame.Rect(self.X_LECTURA, self.Y_LECTURA, self.ANCHO_PENDIENTE, self.ALTO_PENDIENTE)

    def colgar(self):
        """Colgar el ticket en la linea"""
        self.estado = "colgado"
        self.x = self.target_x
        self.y = self.Y_LINEA
        self.ancho = self.ANCHO_COLGADO
        self.alto = self.ALTO_COLGADO
        self.dragging = False

    def volver_a_pendiente(self):
        """Volver a la posicion pendiente a la derecha"""
        self.estado = "pendiente"
        self.x = self.X_PENDIENTE
        self.y = self.Y_PENDIENTE
        self.ancho = self.ANCHO_PENDIENTE
        self.alto = self.ALTO_PENDIENTE
        self.dragging = False

    def ver_pedido(self):
        """Mostrar en area de lectura"""
        self.estado = "vistiendo"
        self.x = self.X_LECTURA
        self.y = self.Y_LECTURA
        self.ancho = self.ANCHO_PENDIENTE
        self.alto = self.ALTO_PENDIENTE

    def cerrar_lectura(self):
        """Volver a colgado desde modo lectura"""
        self.estado = "colgado"
        self.x = self.target_x
        self.y = self.Y_LINEA
        self.ancho = self.ANCHO_COLGADO
        self.alto = self.ALTO_COLGADO

    def actualizar_posicion_slot(self, nuevo_slot, total_tickets):
        """Recalcular posicion destino en la linea"""
        self.slot = nuevo_slot
        espacio_total = self.LIMITE_DERECHO - self.MARGEN_IZQ
        self.target_x = self.MARGEN_IZQ + (nuevo_slot * (espacio_total / 10))
        if self.estado == "colgado":
            self.x = self.target_x

    def dibujar(self, pantalla, fuente):
        """Dibuja el ticket segun su estado"""
        if self.estado == "pendiente":
            self._dibujar_grande(pantalla, self.x, self.y)
        elif self.estado == "colgado":
            self._dibujar_colgado(pantalla)
        elif self.estado == "vistiendo":
            self._dibujar_grande(pantalla, self.x, self.y)

    def _dibujar_grande(self, pantalla, x, y):
        """Dibuja el ticket en tamano grande (pendiente o lectura)"""
        ancho = self.ANCHO_PENDIENTE
        alto = self.ALTO_PENDIENTE

        # Sombra
        sombra = pygame.Surface((ancho, alto), pygame.SRCALPHA)
        sombra.fill((0, 0, 0, 40))
        pantalla.blit(sombra, (x + 4, y + 4))

        # Fondo
        pygame.draw.rect(pantalla, self.color_base, (x, y, ancho, alto), border_radius=6)

        # Borde
        color_borde = (100, 149, 237) if self.dragging else self.color_borde
        grosor = 3 if self.dragging else 2
        pygame.draw.rect(pantalla, color_borde, (x, y, ancho, alto), grosor, border_radius=6)

        # Titulo: numero de ticket y nombre
        fuente_titulo = pygame.font.SysFont("Arial", 16, bold=True)
        texto_titulo = f"Ticket #{self.slot + 1} - {self.cliente.nombre.upper()}"
        pantalla.blit(fuente_titulo.render(texto_titulo, True, (40, 40, 40)), (x + 10, y + 10))

        # Linea separadora
        pygame.draw.line(pantalla, self.color_borde, (x + 10, y + 35), (x + ancho - 10, y + 35), 1)

        # Ingredientes
        fuente_ing = pygame.font.SysFont("Arial", 14)
        y_info = y + 45
        for ingrediente in self.cliente.pedido:
            texto_ing = f"  * {ingrediente}"
            pantalla.blit(fuente_ing.render(texto_ing, True, (60, 60, 60)), (x + 10, y_info))
            y_info += 22

        # Barra de paciencia del cliente
        if self.cliente.estado == "esperando":
            largo_barra = int((self.cliente.paciencia / self.cliente.paciencia_maxima) * (ancho - 20))
            color_barra = (200, 50, 50) if self.cliente.paciencia < 40 else (50, 180, 50)
            pygame.draw.rect(pantalla, (200, 200, 200), (x + 10, y + alto - 25, ancho - 20, 10))
            pygame.draw.rect(pantalla, color_barra, (x + 10, y + alto - 25, largo_barra, 10))

    def _dibujar_colgado(self, pantalla):
        """Dibuja el ticket pequeno colgado de la linea"""
        x = self.target_x
        y = self.Y_LINEA
        ancho = self.ANCHO_COLGADO
        alto = self.ALTO_COLGADO

        # Cable vertical desde la linea
        centro_x = x + ancho // 2
        pygame.draw.line(pantalla, (100, 100, 100), (centro_x, 28), (centro_x, y), 2)

        # Clavo
        pygame.draw.circle(pantalla, (80, 60, 40), (centro_x, 28), 4)

        # Sombra
        sombra = pygame.Surface((ancho, alto), pygame.SRCALPHA)
        sombra.fill((0, 0, 0, 30))
        pantalla.blit(sombra, (x + 2, y + 2))

        # Fondo
        pygame.draw.rect(pantalla, self.color_base, (x, y, ancho, alto), border_radius=3)

        # Borde
        pygame.draw.rect(pantalla, self.color_borde, (x, y, ancho, alto), 1, border_radius=3)

        # Nombre
        fuente_chica = pygame.font.SysFont("Arial", 10)
        texto_nombre = fuente_chica.render(self.cliente.nombre[:6], True, (60, 60, 60))
        pantalla.blit(texto_nombre, (x + 4, y + 4))

        # Linea separadora
        pygame.draw.line(pantalla, self.color_borde, (x + 3, y + 18), (x + ancho - 3, y + 18), 1)

        # Ingredientes
        y_info = y + 22
        fuente_ing = pygame.font.SysFont("Arial", 8)
        for ingrediente in list(self.cliente.pedido)[:3]:
            texto_ing = fuente_ing.render(ingrediente[:8], True, (90, 90, 90))
            pantalla.blit(texto_ing, (x + 3, y_info))
            y_info += 11


class Cliente:
      def __init__(self, x, y):
        # --- Atributos de Identidad ---
        self.nombres_posibles = ["Paco", "Maria", "Luis", "Ana", "Carlos", "Elena"]
        self.nombre = random.choice(self.nombres_posibles)
        
        # --- Atributos de Posición y Movimiento ---
        self.x = x
        self.y = y
        self.velocidad = 2
        self.posicion_destino = x  # Hacia dónde camina en la cola
        
        # --- Atributos de Estado del Juego ---
        self.estado = "caminando"  # Estados: "caminando", "esperando", "atendido", "enojado"
        self.paciencia_maxima = 100  # Barra de paciencia (100% llena)
        self.paciencia = self.paciencia_maxima
        self.pedido = self.generar_pedido_aleatorio()
        
        # --- Configuración Visual Temporal (Un cuadrado de color) ---
        self.ancho, self.alto = 50, 80
        self.color = (random.randint(50, 200), random.randint(50, 200), random.randint(50, 200))

      def generar_pedido_aleatorio(self):
        """Genera una combinación de ingredientes para el sushi de forma aleatoria"""
        tipos_arroz = ["Arroz Blanco", "Arroz Integral"]
        tipos_alga = ["Nori", "Paper"]
        rellenos = ["Salmon", "Atun", "Langostino", "Aguacate"]
        
        return {
             random.choice(tipos_arroz),
             random.choice(tipos_alga),
             random.choice(rellenos)
        }
 
      def actualizar(self):
        """Maneja la lógica del cliente en cada fotograma (FPS)"""
        # 1. Movimiento hacia su lugar en la cola
        if self.x < self.posicion_destino:
            self.x += self.velocidad
            if self.x >= self.posicion_destino:
                self.x = self.posicion_destino
                if self.estado == "caminando":
                    self.estado = "esperando"
                    
        # 2. Reducción de paciencia si está esperando en la cola
        if self.estado == "esperando":
            self.paciencia -= 0.05  # Controla qué tan rápido se impacienta
            if self.paciencia <= 0:
                self.paciencia = 0
                self.estado = "enojado"

      def dibujar(self, pantalla, fuente):

        """Dibuja al cliente y su información en la pantalla"""
        # Dibujar el cuerpo del cliente
        rect_cliente = pygame.Rect(self.x, self.y, self.ancho, self.alto)
        pygame.draw.rect(pantalla, self.color, rect_cliente, border_radius=5)
        
        # Dibujar el nombre arriba del cliente
        txt_nombre = fuente.render(self.nombre, True, (0, 0, 0))
        pantalla.blit(txt_nombre, (self.x, self.y - 45))
        
        # Dibujar la barra de paciencia (Verde que se acorta)
        if self.estado == "esperando":
            largo_barra = int((self.paciencia / self.paciencia_maxima) * self.ancho)
            # Color dinámico: cambia de verde a rojo según la paciencia
            color_barra = (200, 50, 50) if self.paciencia < 40 else (50, 200, 50)
            
            pygame.draw.rect(pantalla, (200, 200, 200), (self.x, self.y - 15, self.ancho, 8)) # Fondo gris
            pygame.draw.rect(pantalla, color_barra, (self.x, self.y - 15, largo_barra, 8)) # Barra activa









            