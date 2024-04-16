import pygame
import random
import os
import math

present_working_directory = os.getcwd()

#initiallising pygame 
pygame.init()
pygame.display.set_caption("Block Jumper")
blockJumperIcon = pygame.image.load("blockJumperIcon.png")
pygame.display.set_icon(blockJumperIcon)

screen_size = [1000, 500]
width = 1000
height = 500

screen = pygame.display.set_mode((screen_size[0], screen_size[1]))
timer = pygame.time.Clock()
wall_thickness = 5
gravity = 0.5
max_speed = 20
running = True
lives = 3
fps = 60
score = 0
font = pygame.font.Font(None, 32)
score_text = font.render("Score: " + str(score), True, (255, 0, 0), (255, 255, 255))
score_text_rect = score_text.get_rect()
score_text_rect.topleft = (0 + wall_thickness, 0 + wall_thickness)
mouse_rect = pygame.Rect(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1], 1, 1)
bot_mode = 0
total_missles = 0
angle = 190
missles_name = "missles"


path = os.path.realpath("sprits")
os.chdir(path)
new_path = os.path.realpath("charSprits")
os.chdir(new_path)
charFaceLeft = pygame.image.load("facingLeft.png")
charFaceRight = pygame.image.load("facingRight.png")
charFaceForward = pygame.image.load("facingForward.png")
os.chdir(path)

new_path = os.path.realpath("heartSprits")
os.chdir(new_path)
emptyLive = pygame.image.load("emptyHeart.png")
fullLive = pygame.image.load("fullHeart.png")
os.chdir(path)

new_path = os.path.realpath("missleLauncherSprits")
os.chdir(new_path)
missleLauncherSprits = [pygame.image.load("missleLauncherBody.png"), pygame.image.load("missleLauncherBarrel1.png"),pygame.image.load("missleLauncherBarrel2.png"),pygame.image.load("missleLauncherBarrel3.png"),pygame.image.load("missleLauncherBarrel4.png"),pygame.image.load("missleLauncherBarrel5.png")]
os.chdir(present_working_directory)

while running:
    #setting game fps to 60
    timer.tick(fps)
    #setting screen background color to white
    screen.fill("white")

    #Allows user to exit out of the game
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    image = missleLauncherSprits[1]
    key=pygame.key.get_pressed()
    if key[pygame.K_SPACE]:
        angle = angle + 1
        image = pygame.transform.rotate(image, angle)
    new_rect = image.get_rect()
    pygame.draw.rect(screen, "red", new_rect)
    screen.blit(image, (200, 200))
    pygame.display.flip()

pygame.quit()