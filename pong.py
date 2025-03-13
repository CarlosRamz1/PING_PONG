import pygame

# Inicializar pygame
pygame.init()

# Configuración de la pantalla
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ping Pong Game")

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Reloj para controlar FPS
clock = pygame.time.Clock()

running = True
while running:
    screen.fill(BLACK)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
