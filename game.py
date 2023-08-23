import pygame
import os


WIDTH, HIEGHT = 900, 500
WINDOW = pygame.display.set_mode((WIDTH, HIEGHT))
pygame.display.set_caption("My Game")

# colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)


# Frame and Movment
FBS = 60
VELOCITY = 5
BULLETS_VELOCITY = 9
MAX_BULLETS = 3


YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2

# Width and Hieght of Spaceships
SPACESHIP_WIDTH, SPACESHIP_HIEGHT = 55, 40

# Border
BORDER = pygame.Rect(WIDTH // 2 - 5, 0, 10, HIEGHT)

# Add image or (surfaces)
# os.path.join("Assets", "spaceship_yellow.png") it is not require
YELLOW_SPACESHIP_IMAGE = pygame.image.load("Assets/spaceship_red.png")

# Scale and Rotate
YELLOW_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(
    YELLOW_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HIEGHT)), 90)


RED_SPACESHIP_IMAGE = pygame.image.load(
    os.path.join("Assets", "spaceship_red.png"))

RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(
    RED_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HIEGHT)), 270)


SPACE = pygame.transform.scale(pygame.image.load(
    os.path.join("Assets", "space.png")), (WIDTH, HIEGHT))


def draw_window(yellow, red, yellow_bullets, red_bullets):
    WINDOW.blit(SPACE, (0, 0))
    pygame.draw.rect(WINDOW, BLACK, BORDER)
    WINDOW.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y))
    WINDOW.blit(RED_SPACESHIP, (red.x, red.y))

    for bullet in yellow_bullets:
        pygame.draw.rect(WINDOW, YELLOW, bullet)

    for bullet in red_bullets:
        pygame.draw.rect(WINDOW, RED, bullet)

    pygame.display.update()


def yellow_handle_movement(keys_pressed, yellow):
    if keys_pressed[pygame.K_a] and yellow.x - VELOCITY > 0:  # LEFT
        yellow.x -= VELOCITY
    # DOWN
    if keys_pressed[pygame.K_s] and (yellow.y + yellow.width) + VELOCITY < HIEGHT:
        yellow.y += VELOCITY
    # RIGHT
    if keys_pressed[pygame.K_d] and (yellow.x + yellow.width) + VELOCITY - 25 < BORDER.x:
        yellow.x += VELOCITY
    if keys_pressed[pygame.K_w] and yellow.y - VELOCITY > 0:  # UP
        yellow.y -= VELOCITY


def red_handle_movement(keys_pressed, red):
    # LEFT
    if keys_pressed[pygame.K_LEFT] and red.x - VELOCITY > BORDER.x:
        red.x -= VELOCITY
    # DOWN
    if keys_pressed[pygame.K_DOWN] and (red.y + red.width) + VELOCITY < HIEGHT:
        red.y += VELOCITY
    # RIGHT
    if keys_pressed[pygame.K_RIGHT] and (red.x + red.width) + VELOCITY - 20 < WIDTH:
        red.x += VELOCITY
    if keys_pressed[pygame.K_UP] and red.y - VELOCITY > 0:  # UP
        red.y -= VELOCITY


def handle_bullets(yellow_bullets, red_bullets, yellow, red):
    for bullet in yellow_bullets:
        bullet.x += BULLETS_VELOCITY
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullets.remove(bullet)
        elif bullet.x > WIDTH:
            yellow_bullets.remove(bullet)

    for bullet in red_bullets:
        bullet.x -= BULLETS_VELOCITY
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)
        elif bullet.x < 0:
            red_bullets.remove(bullet)


def main():

    yellow = pygame.Rect(300, 100, SPACESHIP_WIDTH, SPACESHIP_HIEGHT)
    red = pygame.Rect(700, 100, SPACESHIP_WIDTH, SPACESHIP_HIEGHT)
    yellow_bullets = []
    red_bullets = []
    clock = pygame.time.Clock()

    run = True
    while run:
        clock.tick(FBS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(yellow_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(
                        yellow.x + yellow.width, yellow.y + yellow.height // 2 + 5, 10, 5)
                    yellow_bullets.append(bullet)
                if event.key == pygame.K_RCTRL and len(red_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(
                        red.x - 20, red.y + red.height // 2 + 5, 10, 5)
                    red_bullets.append(bullet)

        keys_pressed = pygame.key.get_pressed()
        yellow_handle_movement(keys_pressed, yellow)
        red_handle_movement(keys_pressed, red)
        draw_window(yellow, red, yellow_bullets, red_bullets)
        handle_bullets(yellow_bullets, red_bullets, yellow, red)

    pygame.quit()


if __name__ == "__main__":
    main()
