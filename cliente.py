

import pygame
import random



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
            "arroz": random.choice(tipos_arroz),
            "alga": random.choice(tipos_alga),
            "relleno": random.choice(rellenos)
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