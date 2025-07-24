import pygame
import math
import sys

# Inicialização do pygame
pygame.init()

# Configuração da tela
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sistema Pêndulo Invertido (Física Real)")

# Cores
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GRAY = (200, 200, 200)

# Parâmetros físicos (em "unidades de jogo", não SI exato)
g = 9.81              # gravidade
L = 1.0               # comprimento do pêndulo (metros "fictícios")
PIXELS_PER_METER = 150  # escala: 1 m = 150 pixels
pole_length_px = L * PIXELS_PER_METER

# Posições e dimensões do carrinho
car_width = 100
car_height = 40
wheel_radius = 15
ground_y = HEIGHT - 100
car_x = WIDTH // 2
car_speed = 0.0
car_accel = 8.0         # aceleração mais forte (para resposta rápida)
car_damping = 0.98      # atrito para o carrinho não ficar acelerando infinito

# Estado do pêndulo
theta = math.radians(5)   # ângulo inicial
theta_dot = 0.0
damping = 0.01            # atrito angular (para o pêndulo perder energia)

# Física do pêndulo com base móvel
def update_pendulum(dt, force):
    global theta, theta_dot, car_x, car_speed

    # Atualiza velocidade e posição do carrinho
    car_speed += force * dt
    car_speed *= car_damping  # atrito horizontal
    car_x += car_speed

    # Equação aproximada para o pêndulo (base móvel)
    theta_ddot = (g/L) * math.sin(theta) - (force/L) * math.cos(theta)
    theta_dot += theta_ddot * dt
    theta_dot *= (1 - damping)  # atrito angular
    theta += theta_dot * dt

    # Limita carrinho dentro da tela
    if car_x < 50:
        car_x = 50
        car_speed = 0
    if car_x > WIDTH - 50:
        car_x = WIDTH - 50
        car_speed = 0

# Desenha grid
def draw_grid():
    spacing = 50
    for x in range(0, WIDTH, spacing):
        pygame.draw.line(screen, GRAY, (x, 0), (x, HEIGHT), 1)
    for y in range(0, HEIGHT, spacing):
        pygame.draw.line(screen, GRAY, (0, y), (WIDTH, y), 1)

# Relógio para FPS
clock = pygame.time.Clock()

running = True
while running:
    dt = clock.tick(60) / 1000  # 60 FPS → segundos por frame
    screen.fill(WHITE)

    # Eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Controles manuais (setas)
    keys = pygame.key.get_pressed()
    force = 0.0
    if keys[pygame.K_LEFT]:
        force = -car_accel
    elif keys[pygame.K_RIGHT]:
        force = car_accel

    # Atualiza física
    update_pendulum(dt, force)

    # Calcula ponta do pêndulo em pixels
    pole_x = car_x + pole_length_px * math.sin(theta)
    pole_y = ground_y - car_height - wheel_radius - pole_length_px * math.cos(theta)

    # Desenha grade, chão e carrinho
    draw_grid()
    pygame.draw.line(screen, BLACK, (0, ground_y), (WIDTH, ground_y), 4)
    pygame.draw.rect(screen, BLUE, (car_x - car_width//2, ground_y - car_height - wheel_radius, car_width, car_height))

    # Rodas (acima do chão)
    roda_y = ground_y - wheel_radius
    pygame.draw.circle(screen, BLACK, (int(car_x - car_width//3), int(roda_y)), wheel_radius)
    pygame.draw.circle(screen, BLACK, (int(car_x + car_width//3), int(roda_y)), wheel_radius)

    # Pêndulo
    pygame.draw.line(screen, BLACK, (car_x, ground_y - car_height - wheel_radius), (pole_x, pole_y), 4)
    pygame.draw.circle(screen, RED, (int(pole_x), int(pole_y)), 10)

    pygame.display.flip()

pygame.quit()
sys.exit()
