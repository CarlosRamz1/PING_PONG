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

# Configuración de las paletas y la pelota
PADDLE_WIDTH, PADDLE_HEIGHT = 10, 100
BALL_SIZE = 10
PADDLE_SPEED = 5

# Posición inicial de las paletas
paddle1 = pygame.Rect(30, HEIGHT//2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT)
paddle2 = pygame.Rect(WIDTH - 40, HEIGHT//2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT)

# Posición inicial de la pelota
ball = pygame.Rect(WIDTH//2 - BALL_SIZE//2, HEIGHT//2 - BALL_SIZE//2, BALL_SIZE, BALL_SIZE)

# Velocidades de la pelota
ball_speed_x = 4
ball_speed_y = 4
ball_moving = False  # Variable para controlar si la pelota está en movimiento

# Puntuaciones
score1 = 0
score2 = 0
font = pygame.font.Font(None, 36)

# Cargar sonidos
hit_sound = pygame.mixer.Sound("sounds/hit.wav")
score_sound = pygame.mixer.Sound("sounds/score.wav")
wall_sound = pygame.mixer.Sound("sounds/hit.wav")

# Reloj para controlar FPS
clock = pygame.time.Clock()

running = True
while running:
    screen.fill(BLACK)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                ball_moving = True  # Iniciar movimiento cuando se presiona Enter
    
    # Capturar teclas presionadas
    keys = pygame.key.get_pressed()
    
    # Movimiento de la paleta 1 (Jugador 1 - W/S)
    if keys[pygame.K_w] and paddle1.top > 0:
        paddle1.y -= PADDLE_SPEED
    if keys[pygame.K_s] and paddle1.bottom < HEIGHT:
        paddle1.y += PADDLE_SPEED
    
    # Movimiento de la paleta 2 (Jugador 2 - Up/Down)
    if keys[pygame.K_UP] and paddle2.top > 0:
        paddle2.y -= PADDLE_SPEED
    if keys[pygame.K_DOWN] and paddle2.bottom < HEIGHT:
        paddle2.y += PADDLE_SPEED
    
    # Mover la pelota solo si está en movimiento
    if ball_moving:
        ball.x += ball_speed_x
        ball.y += ball_speed_y
    
    # Rebote en la parte superior e inferior
    if ball.top <= 0 or ball.bottom >= HEIGHT:
        ball_speed_y *= -1
        wall_sound.play()
    
    # Rebote en las paletas
    if ball.colliderect(paddle1) or ball.colliderect(paddle2):
        ball_speed_x *= -1
        hit_sound.play()
    
    # Verificar si la pelota sale por los lados
    if ball.left <= 0:
        score2 += 1  # Punto para el jugador 2
        score_sound.play()
        ball.x = WIDTH // 2 - BALL_SIZE // 2
        ball.y = HEIGHT // 2 - BALL_SIZE // 2
        ball_moving = False  # Detener pelota hasta presionar Enter
    if ball.right >= WIDTH:
        score1 += 1  # Punto para el jugador 1
        score_sound.play()
        ball.x = WIDTH // 2 - BALL_SIZE // 2
        ball.y = HEIGHT // 2 - BALL_SIZE // 2
        ball_moving = False  # Detener pelota hasta presionar Enter
    
    # Dibujar paletas, pelota y puntuaciones
    pygame.draw.rect(screen, WHITE, paddle1)
    pygame.draw.rect(screen, WHITE, paddle2)
    pygame.draw.ellipse(screen, WHITE, ball)
    
    score_text = font.render(f"{score1} - {score2}", True, WHITE)
    screen.blit(score_text, (WIDTH // 2 - 20, 20))
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
