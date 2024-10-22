import pygame
import sys
import random

# Inicialización de Pygame
pygame.init()

# Dimensiones de la pantalla
WIDTH, HEIGHT = 820, 620
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Carga de imágenes
logotipo = pygame.image.load('mono.png')
fondo = pygame.image.load('fondo.png')
banana = pygame.image.load('banana.png')
bomba = pygame.image.load('bomba.png')

logo_x, logo_y = 70, 70
velocidad = 0.2

bananas_comidas = 0
vidas_restantes = 5
niveles = 1
bomba_visible = False

def check_overlap(x1, y1, x2, y2, width, height):
    return (x1 < x2 + width and x1 + width > x2 and y1 < y2 + height and y1 + height > y2)

def posicion_aleatoria_valida():
    x = random.randint(0, WIDTH - banana.get_width())
    y = random.randint(0, HEIGHT - banana.get_height())
    return x, y

def siguiente_nivel():
    global niveles, velocidad
    niveles += 1
    velocidad += 0.2
    colocar_elementos()

def colocar_elementos():
    global banana_x, banana_y, bomba_x, bomba_y
    banana_x, banana_y = posicion_aleatoria_valida()
    bomba_x, bomba_y = posicion_aleatoria_valida()

colocar_elementos()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    new_logo_x, new_logo_y = logo_x, logo_y

    if keys[pygame.K_UP]:
        new_logo_y -= velocidad
    if keys[pygame.K_DOWN]:
        new_logo_y += velocidad
    if keys[pygame.K_LEFT]:
        new_logo_x -= velocidad
    if keys[pygame.K_RIGHT]:
        new_logo_x += velocidad

    # Límite de movimiento
    new_logo_x = max(0, min(WIDTH - logotipo.get_width(), new_logo_x))
    new_logo_y = max(0, min(HEIGHT - logotipo.get_height(), new_logo_y))

    logo_x, logo_y = new_logo_x, new_logo_y

    # Colisión con banana
    if check_overlap(logo_x, logo_y, banana_x, banana_y, logotipo.get_width(), logotipo.get_height()):
        bananas_comidas += 1
        colocar_elementos()
        if bananas_comidas % 5 == 0:
            velocidad += 0.2
        if bananas_comidas % 10 == 0:
            siguiente_nivel()

    if bananas_comidas >= 5:
        bomba_visible = True
        if check_overlap(logo_x, logo_y, bomba_x, bomba_y, logotipo.get_width(), logotipo.get_height()):
            vidas_restantes -= 1
            colocar_elementos()
            if vidas_restantes == 0:
                pygame.quit()
                sys.exit()

    screen.blit(fondo, (0, 0))
    screen.blit(banana, (banana_x, banana_y))
    screen.blit(logotipo, (logo_x, logo_y))

    if bomba_visible:
        screen.blit(bomba, (bomba_x, bomba_y))

    pygame.display.set_caption(f"Bananas comidas: {bananas_comidas} Vidas Restantes: {vidas_restantes} Nivel: {niveles}")
    pygame.display.flip()

pygame.quit()
sys.exit()
