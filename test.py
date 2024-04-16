import pygame, random
from pygame._sdl2 import Window

pygame.init()

# This will get the screen resolution, must be done before the 
# pygame.display.set_mode
display_info = pygame.display.Info()
window_size = (display_info.current_w, display_info.current_h)

surface = pygame.display.set_mode( (100, 200) )

window = Window.from_display_module()
window.position = (0,100) # Will place the window around the screen


inProgram = True
while inProgram:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            inProgram = False

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_SPACE:
                # Move the window to a random screen position
                window.position = (random.randint(0, window_size[0]), 
                random.randint(30, window_size[1]))

    surface.fill((0, 100, 100))

    pygame.display.flip()