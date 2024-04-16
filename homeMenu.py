import pygame 
import os
import math
import blockJumper
present_working_directory = os.getcwd()


pygame.init()

width = 1000
height = 500
#screen_Size = pygame.display.get_desktop_sizes()
#screen = pygame.display.set_mode((screen_Size[0][0], screen_Size[0][1] - 100), pygame.FULLSCREEN)
screen = pygame.display.set_mode((width, height))
#screen = pygame.display.set_mode((screen_Size[0][0], screen_Size[0][1]))
timer = pygame.time.Clock()
fps = 60
pygame.display.set_caption("Block Jumper")
blockJumperIcon = pygame.image.load("blockJumperIcon.png")
pygame.display.set_icon(blockJumperIcon)
dot_num = 0
rule_menu = False


font = pygame.font.Font(None, 32)
mouse_rect = pygame.Rect(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1], 1, 1)


path = os.path.realpath("sprits")
os.chdir(path)

new_path = os.path.realpath("homeBackground")
os.chdir(new_path)
background_image = pygame.image.load("background.png")
dot_image = pygame.image.load("dots.png")
os.chdir(path)

new_path = os.path.realpath("buttons")
os.chdir(new_path)
play_button = pygame.image.load("playButton.png")
rules_button = pygame.image.load("rulesButton.png")
back_menu_button = pygame.image.load("backToMenuButton.png")
button_images = [play_button, rules_button, back_menu_button]
os.chdir(present_working_directory)



running = True


#Defining classes
class Mouse:

    def __init__(self, x_pos, y_pos):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.rect = pygame.Rect(self.x_pos, self.y_pos, 1, 1)
    
    def update_pos(self, new_x, new_y):
        self.rect = pygame.Rect(new_x, new_y, 1, 1)


class Buttons:
    def __init__(self, x_pos, y_pos, image, id):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.image = image
        self.id = id
        self.rect = ""


    def draw(self):
        global screen
        self.rect = self.image.get_rect()
        self.rect.left = self.x_pos
        self.rect.top = self.y_pos
        screen.blit(self.image, (self.x_pos, self.y_pos))


    def check_click(self):
        global rule_menu
        if pygame.mouse.get_pressed()[0]:
            if pygame.Rect.colliderect(self.rect, mouse.rect):
                if self.id == 1:
                    blockJumper.reset_game()
                    blockJumper.runGame()
                elif self.id == 2:
                    rule_menu = True
                elif self.id == 3:
                    rule_menu = False
                    

class Text:
    def __init__(self, text, background, color, x_pos, y_pos, id):
        self.text = text
        self.background = background
        self.color = color
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.id = id 
        self.text_feild_rect = None
        self.text_feild = None

    def make_text(self):
        self.text_feild = font.render(self.text, True, self.color, self.background)
        self.text_feild_rect = self.text_feild.get_rect()
        self.text_feild_rect.topleft = (self.x_pos, self.y_pos)
        screen.blit(self.text_feild, self.text_feild_rect)


class Dot:
    def __init__(self, x_pos, y_pos, move_speed, id):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.move_speed = move_speed
        self.id = id
        self.restarted = False

    def draw(self):
        screen.blit(dot_image, (self.x_pos, self.y_pos))
    
    def update_pos(self):
        self.x_pos = self.x_pos + self.move_speed
        #self.y_pos = self.y_pos + .25*(math.sin(.08*self.x_pos))
    
    def restart_animation(self):
        global dot_num
        if(self.x_pos > 0 and self.restarted == False):
            dot_name = "dot" + str(dot_num)
            dots.append(exec("%s = None" % (dot_name)))
            for i in range(len(dots)):
                if dots[i] == None:
                    dots[i] = Dot(self.x_pos - 1000, self.y_pos, self.move_speed, dot_num)
                    dot_num = dot_num + 1
                    self.restarted = True
        elif(self.x_pos >= 1000):
            for i in range(len(dots)-1):
                if self.id == dots[i].id:
                    dots.pop(i)


class Background:
    def __init__(self, x_pos, y_pos, image):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.image = image
        self.x_velocity = 0
        self.increasing = 0
    
    def draw(self):
        screen.blit(self.image, (self.x_pos, self.y_pos))

    def update_pos(self):
        global rule_menu
        if rule_menu == True and self.x_pos > -1000:

            self.x_velocity = (-1/500*((self.increasing -500)**2) + 500)
            self.increasing += 0.5
            if self.x_pos - self.x_velocity < -1000:
                self.x_pos = -1000
            else:
                self.x_pos -= self.x_velocity

        elif rule_menu == False and self.x_pos < 0:

            self.x_velocity = (-1/500*((self.increasing -500)**2) + 500)
            self.increasing += 0.5
            if self.x_pos + self.x_velocity > 0:
                self.x_pos = 0
            else:
                self.x_pos += self.x_velocity
        else:
            self.increasing = 0
            self.x_velocity = 0



#Creating overall functions
def update_buttons():
    if rule_menu == False and background.x_pos == 0:
        for item in buttons[0]:
            item.draw()
            item.check_click()
    elif rule_menu == True and background.x_pos == -1000:
        for item in buttons[1]:
            item.draw()
            item.check_click()

def update_texts():
    for item in texts:
        item.make_text()

def update_dots():
    for item in dots:
        item.restart_animation()
        item.update_pos()
        item.draw()

def update_background():
    background.update_pos()
    background.draw()


#Creating objects and putting in class lists
background = Background(0, 0, background_image)    

button1 = Buttons(235, 350, button_images[0], 1)
button2 = Buttons(515, 350, button_images[1], 2)
button3 = Buttons(235, 350, button_images[2], 3)
buttons = [[button1, button2], [button3]]

mouse = Mouse(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[0])

#text1 = Text("Block Jumper", None, "black", 400, 100, 1)
texts = []

dot1 = Dot(0,0, .5, 1)
dots = [dot1]

while running:
    timer.tick(fps)
    screen.fill("white")

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            quit()

    mouse.update_pos(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])
    if pygame.mouse.get_pressed()[0]:
            clicked = True
    update_background()
    update_dots()
    update_buttons()
    #update_texts() 
    pygame.display.flip()
pygame.quit()
