import pygame

# Inicializar pygame
pygame.init()

# Configuración de la pantalla
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("CarlOz VS RAM")

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Configuración de las paletas y la pelota
PADDLE_WIDTH, PADDLE_HEIGHT = 10, 100
BALL_SIZE = 10
PADDLE_SPEED = 5
BALL_SPEED_INCREMENT = 0.5  # Aumento de velocidad tras cada rebote

# Cargar sonidos
hit_sound = pygame.mixer.Sound("sounds/hit.wav")
score_sound = pygame.mixer.Sound("sounds/score.wav")
wall_sound = pygame.mixer.Sound("sounds/hit.wav")

# Fuente para texto
font = pygame.font.Font(None, 36)

# Variables globales
ball_moving = False
winning_score = 5
score1 = 0
score2 = 0
ball = pygame.Rect(WIDTH//2 - BALL_SIZE//2, HEIGHT//2 - BALL_SIZE//2, BALL_SIZE, BALL_SIZE)
ball_speed_x = 4
ball_speed_y = 4
paddle1 = pygame.Rect(30, HEIGHT//2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT)
paddle2 = pygame.Rect(WIDTH - 40, HEIGHT//2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT)

def show_menu():
    global winning_score, score1, score2
    menu_running = True
    while menu_running:
        screen.fill(BLACK)
        title_text = font.render("Selecciona puntos para ganar: 5, 10 o 15", True, WHITE)
        screen.blit(title_text, (WIDTH//2 - 200, HEIGHT//3))
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_5:
                    winning_score = 5
                    menu_running = False
                elif event.key == pygame.K_0:
                    winning_score = 10
                    menu_running = False
                elif event.key == pygame.K_1:
                    winning_score = 15
                    menu_running = False
    
    # Reiniciar puntuaciones
    score1 = 0
    score2 = 0

def reset_game():
    global ball, ball_speed_x, ball_speed_y, ball_moving, paddle1, paddle2
    ball.x = WIDTH//2 - BALL_SIZE//2
    ball.y = HEIGHT//2 - BALL_SIZE//2
    ball_speed_x = 4
    ball_speed_y = 4
    ball_moving = False
    paddle1.y = HEIGHT//2 - PADDLE_HEIGHT//2
    paddle2.y = HEIGHT//2 - PADDLE_HEIGHT//2

# Mostrar menú antes de comenzar el juego
show_menu()

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
    
    # Movimiento de las paletas
    if keys[pygame.K_w] and paddle1.top > 0:
        paddle1.y -= PADDLE_SPEED
    if keys[pygame.K_s] and paddle1.bottom < HEIGHT:
        paddle1.y += PADDLE_SPEED
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
    
    # Rebote en las paletas con cálculo de ángulo
    if ball.colliderect(paddle1) or ball.colliderect(paddle2):
        hit_sound.play()
        ball_speed_x *= -1  # Cambia la dirección horizontal
        ball_speed_x += BALL_SPEED_INCREMENT if ball_speed_x > 0 else -BALL_SPEED_INCREMENT  # Aumenta velocidad
        offset = (ball.centery - paddle1.centery) / (PADDLE_HEIGHT / 2) if ball.colliderect(paddle1) else (ball.centery - paddle2.centery) / (PADDLE_HEIGHT / 2)
        ball_speed_y = offset * 5  # Ajuste del ángulo de salida
    
    # Verificar si la pelota sale por los lados
    if ball.left <= 0:
        score2 += 1  # Punto para el jugador 2
        score_sound.play()
        reset_game()
    if ball.right >= WIDTH:
        score1 += 1  # Punto para el jugador 1
        score_sound.play()
        reset_game()
    
    # Verificar si alguien ha ganado
    if score1 >= winning_score or score2 >= winning_score:
        show_menu()  # Reiniciar el juego si alguien gana
    
    # Dibujar paletas, pelota y puntuaciones
    pygame.draw.rect(screen, WHITE, paddle1)
    pygame.draw.rect(screen, WHITE, paddle2)
    pygame.draw.ellipse(screen, WHITE, ball)
    for i in range(0, HEIGHT, 20):
        pygame.draw.rect(screen, WHITE, (WIDTH//2 - 1, i, 2, 10))
    
    score_text = font.render(f"{score1} - {score2}", True, WHITE)
    screen.blit(score_text, (WIDTH // 2 - 20, 20))
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
