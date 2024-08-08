# Example file showing a basic pygame "game loop"
import pygame
from screen.Screen import Screen
from actors.Snake import Snake

# pygame setup
pygame.init()
clock = pygame.time.Clock()
running = True

screen = Screen().get_screen()
snake_body = [Snake().get_snake_pixel()]

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("black")

    # RENDER YOUR GAME HERE

    pygame.draw.rect(screen, "white", Snake().get_snake_pixel())

    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

pygame.quit()
