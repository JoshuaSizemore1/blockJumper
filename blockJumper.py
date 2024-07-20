#Importing libraries
import pygame
import random
import os
import math
import threading
present_working_directory = os.getcwd()

#initiallising pygame 
pygame.init()



#global game variables 
screen_size = [1000, 500]
width = 1000
height = 500

screen = pygame.display.set_mode((screen_size[0], screen_size[1]))
timer = pygame.time.Clock()
wall_thickness = 5
gravity = 0.5
max_speed = 20
running = True
end_run = True
max_lives = 3
lives = max_lives
fps = 60
score = 0
font = pygame.font.Font(None, 32)
"""score_text = font.render("Score: " + str(score), True, (255, 0, 0), (255, 255, 255))
score_text_rect = score_text.get_rect()
score_text_rect.topleft = (0 + wall_thickness, 0 + wall_thickness)"""
mouse_rect = pygame.Rect(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1], 1, 1)
bot_mode = 0
total_missles = 0
missles_name = "missles"
total_missleLaunchers = 0
missleLaunchers_name = "missleLauncher"
misslesLaunchers_spawn = 0
missleLauncher_can_spawn = True
newid = 0

pygame.display.set_caption("Block Jumper")
blockJumperIcon = pygame.image.load("blockJumperIcon.png")
pygame.display.set_icon(blockJumperIcon)


path = os.path.realpath("sprits")
os.chdir(path)

new_path = os.path.realpath("random")
os.chdir(new_path)
grey_backdrop = pygame.image.load("greyBackdrop.png")
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
missleLauncherSprits = [pygame.image.load("missleLauncherBody.png")]
os.chdir(present_working_directory)

#Defining all classes, and class functions

class Mouse:

    def __init__(self, x_pos, y_pos):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.rect = pygame.Rect(self.x_pos, self.y_pos, 1, 1)
    
    def update_pos(self, new_x, new_y):
        self.rect = pygame.Rect(new_x, new_y, 1, 1)


class Buttons:
    def __init__(self, text_color, background_color, rect_color, x_pos, y_pos, width, height, text, id):
        self.text_color = text_color
        self.rect_color = rect_color
        self.background_color = background_color
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.width = width
        self.height = height 
        self.text = text
        self.text_feild = ""
        self.text_feild_rect = ""
        self.button_rect = ""
        self.id = id

    def draw(self):
        global screen
        self.button_rect = pygame.Rect(self.x_pos, self.y_pos, self.width, self.height)
        pygame.draw.rect(screen, self.rect_color, self.button_rect, 5)
        self.text_feild = font.render(self.text, True, self.text_color, self.background_color)
        self.text_feild_rect = self.text_feild.get_rect()
        self.text_feild_rect.topleft = (self.x_pos + 10, self.y_pos + 35)
        screen.blit(self.text_feild, self.text_feild_rect)


    def check_click(self):
        global running
        global end_run
        if pygame.mouse.get_pressed()[0]:
            if pygame.Rect.colliderect(self.button_rect, mouse.rect):
                if self.id == 1:
                    end_run = False
                    running = False


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


#Points class is for every point that is used for increasing score only one currently but could add more
class Points:
    #Defining all the atributes of the Points class
    def __init__(self, x_pos, y_pos, width, color):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.width = width
        self.color = color
        self.radius = width/2
        self.rect = pygame.Rect(self.x_pos, self.y_pos, self.width, self.width)
        self.point = ""
    
    #Defining the function that draws all the points(circles) under the Circles class, and updates their hitboxes
    def draw(self):
        self.rect = pygame.Rect(self.x_pos - self.radius, self.y_pos - self.radius, self.width, self.width)
        self.point = pygame.draw.circle(screen, self.color, (self.x_pos, self.y_pos), self.radius)
    
    #Defining the function that checks if the players hitboc collides with the points hitboxes, and if so it increases score and moves the point to a random (x,y)
    def check_got(self, score):
        #Iterates through all the players to check if any of them collide with the point
        for item in players:
            if pygame.Rect.colliderect(self.rect, item.rect):
                self.x_pos = random.randint(70, 930)
                self.y_pos = random.randint(70, 430)
                score += 1
        return score


#Lines class is for every line that is used for collisions; including boarders of screen, and platforms
class Lines():
    #Defining all the atributes of the Lines class
    def __init__(self, start_x, start_y, end_x, end_y, color, width, height, wall_thickness, id):
        self.start_x = start_x
        self.start_y = start_y
        self.end_x = end_x
        self.end_y = end_y
        self.color = color
        self.width = width
        self.height = height
        self.wall_thickness = wall_thickness
        self.id = id
        self.rect = pygame.Rect(self.start_x, self.start_y - (self.wall_thickness), self.width, self.height*2)
        self.line = ""
        """
        id 1 = bottom wall(floor) collision
        id 2 = left wall collision
        id 3 = top wall (roof / platform) collision
        id 4 = right wall collision
        """

    
    #Defining the function that draws all the lines under the Lines class
    def draw(self):
        self.rect = pygame.Rect(self.start_x, self.start_y - (self.wall_thickness), self.width, self.height*2)
        #pygame.draw.rect(screen, "red", self.rect)
        self.line = pygame.draw.line(screen, self.color, (self.start_x, self.start_y), (self.end_x, self.end_y), self.wall_thickness)


#PLayer class is for all  the players that are used (currently only 1)
class Player():
    #Defining all the atributes of the Player class
    def __init__(self, x_pos, y_pos, color, width, height, x_speed, y_speed, id):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.color = color
        self.width = width
        self.height = height
        self.x_speed = x_speed
        self.y_speed = y_speed
        self.id = id
        self.object = ""
        self.rect = pygame.Rect(self.x_pos, self.y_pos, self.width, self.height)
        self.speed_cap = 4
        self.jump_count = 0
        self.jump_power = 13
        self.jumped = True
        self.og_height = height
        self.dashed = False
        self.auto_move_timer = 0
        self.auto_move_side = 0
        self.currentSprit = charFaceForward
        """
        id = arbatraty identifier never used in current code but might be later
        jump_count = how many itriations a jump will last when up arrow is pressed
        jumped = if the player has a jump left (will lose jump when jumping(turnes False), and gain a jump when colliding with line.id = 1 (turnes True))
        jump_power = start number for number added to x_pos when jumping
        og_height = original height that will never change
        speed_cap = max numbered added to x_pos when moving right or left
        """

    #Defining the function that will apply the correct gravity to the player depending on if it is colliding with any Lines or if it is jumping
    
    def check_grav(self):
        collided = False 
        #Iterates through every line in the lines list        
        for item in lines:

            #Is true if the players hitbox (self.rect) touches / collides with a line (item.rect)
            if pygame.Rect.colliderect(self.rect, item.rect):

                #If player collides with a bottom wall (floor / platform) it will gain its jump back and reset jump power, and its position is set so it is on top of it.
                if item.id == 1 or item.id == 5:
                    if self.jump_count == 0:
                        self.jump_power = 13
                        self.y_speed = 0
                        self.y_pos = item.start_y  - self.height
                        collided = True
                        self.jumped = False
                        self.dashed = False

                #If player collides with a left wall it will be stopped and its position is set so it is touching it
                if item.id == 2 :
                    self.x_speed = 0
                    self.x_pos = item.start_x

                #If player collides with a top wall (roof) it will be end all jumping and lose all jump power
                if item.id == 3:
                    self.jump_count = 0
                    self.jump_power = 0

                #If player collides with a right wall it will be stopped and its position is set so it is touching it
                if item.id == 4:
                    self.x_speed = 0
                    self.x_pos = item.start_x - self.width

        #If the player is still jumping it will increase its hiegth getting lower each times until it stops 
        if self.jump_count > 0:     
                if self.jump_count == 30:
                    self.y_speed = 0       
                self.y_pos -= self.jump_power
                if (self.jump_power - gravity) > 0:
                    self.jump_power -= gravity
                self.jump_count -= 1

        #The player will always fall down unless it is colliding with line, or unless it has reached the max down speed, and is not in a jump
        if collided == False and self.y_speed != max_speed and self.jump_count == 0:
            self.y_speed += gravity
        

    #Defining the function that updates the players position based on its speed
    def update_pos(self):
        self.x_pos += self.x_speed
        self.y_pos += self.y_speed


    #Defining the function that draws the player, and creates its hitbox 
    def draw(self):
        pygame.draw.rect(screen, "red", self.rect)
        self.rect = pygame.Rect(self.x_pos, self.y_pos, self.width, self.height)
        #self.object = pygame.draw.rect(screen, self.color, self.rect)
        screen.blit(self.currentSprit, (self.x_pos, self.y_pos))


    #Defining the function that checks if the up arrow is pressed and sets up the jumping mode if it is pressed
    def check_key_up(self):
        key=pygame.key.get_pressed()
        if key[pygame.K_UP] or key[pygame.K_SPACE]:
            if not self.jumped:
                self.jump_count = 30
                self.jumped = True


    #Defining the function that checks if the right arrow is pressed and moves the player to the right if pressed
    def check_key_right(self):  
        key=pygame.key.get_pressed()
        if key[pygame.K_RIGHT] or key[pygame.K_d]:
            if self.x_speed < self.speed_cap:
                self.currentSprit = charFaceForward
            else:
                self.currentSprit = charFaceRight
            if abs(self.x_speed) < self.speed_cap:
                self.x_speed += 5


    #Defining the function that checks if the right arrow is pressed and moves the player to the left if pressed
    def check_key_left(self):
        key=pygame.key.get_pressed()
        if key[pygame.K_LEFT] or key[pygame.K_a]:
            if abs(self.x_speed) < self.speed_cap:
                self.currentSprit = charFaceForward
            else:
                self.currentSprit = charFaceLeft
            if abs(self.x_speed) < self.speed_cap:
                self.x_speed -= 5
    

    def random_move(self):
        if self.auto_move_timer == 0:
            num = random.randint(1, 20)
            if(num > 18):
                self.jump_count = 30
                self.jumped = True
                self.auto_move_timer = 0
            elif(num >= 12):
                self.auto_move_side = 1
                self.auto_move_timer = 15
            elif(num >= 5):
                self.auto_move_side = 2
                self.auto_move_timer = 15
            elif(num >= 1):
                self.auto_move_side = 0
                self.auto_move_timer = 20
        else:
            self.auto_move_timer -= 1

        if(self.auto_move_side == 1) and (self.auto_move_timer > 0):
            self.x_speed -= 5
        elif(self.auto_move_side == 2) and (self.auto_move_timer > 0):
            self.x_speed += 5


#Missles class is for all the green balls that chase the player and deal damage
class Missles():
    def __init__(self, x_pos, y_pos, color, width, heigth, x_speed, y_speed, id):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.color = color
        self.width = width
        self.height = heigth
        self.radius = width/2
        self.x_speed = x_speed
        self.y_speed = y_speed
        self.x_speed_cap = 3
        self.y_speed_cap = 30
        self.test_x = 0
        self.x_speed_decay = 0.2
        self.y_speed_decay = 1
        self.id = id
        self.bounced = False
        self.missle = ""
        self.rect = pygame.Rect(self.x_pos, self.y_pos, self.width, self.width)

    
    def draw(self):
        self.rect = pygame.Rect(self.x_pos - self.radius, self.y_pos - self.radius, self.width, self.width)
        self.missle = pygame.draw.circle(screen, self.color, (self.x_pos, self.y_pos), self.radius)

    
    def update_pos(self):
        self.x_pos += self.x_speed
        self.y_pos += self.y_speed
    
    def track_player(self):
        global lives
        global screen_size
        global missles
        global missleLaunchers
        global total_missles
        if pygame.Rect.colliderect(self.rect, player1.rect):
            lives = lives - 1
            total_missles = 0
            missles = []
            self.x_speed = 0
            self.y_speed = 0
            player1.x_pos = screen_size[0]/2
            player1.y_pos = screen_size[1]/2
            for item in missleLaunchers:
                item.ammo = 1
        for i in range(len(missles)-1):
            if(missles[i].id != self.id):
                if pygame.Rect.colliderect(self.rect, missles[i].rect):
                    missles.pop(i)
                    missleLaunchers[i].ammo = 1

        else:
            if self.x_pos > player1.x_pos + 25:
                if self.x_speed > 0:
                    self.x_speed -= self.x_speed_decay
                elif self.x_speed > -self.x_speed_cap:
                    self.x_speed -= .2
            elif self.x_pos < player1.x_pos +25:
                if self.x_speed < 0:
                    self.x_speed += self.x_speed_decay
                if self.x_speed < self.x_speed_cap:
                    self.x_speed += .2


            if int(self.y_pos) > player1.y_pos + 25:
                if self.y_speed > 0:
                    self.y_speed -= self.y_speed_decay
                    self.test_x /= 4
                else:
                    self.y_speed += -0.09*self.test_x
                if self.test_x < 5:
                    self.test_x += 0.05
                """
                elif self.y_speed > -self.y_speed_cap:
                    self.test_x += .03
                    self.y_speed += -0.09*self.test_x """ 

            elif int(self.y_pos) < player1.y_pos + 25:
                if self.y_speed < 0:
                    self.y_speed += self.y_speed_decay
                    self.test_x /= 4
                else:
                    self.y_speed += 0.09*self.test_x
                if self.test_x < 5:
                    self.test_x += 0.05
                """
                elif self.y_speed < self.y_speed_cap:
                    self.test_x += .03
                    self.y_speed += 0.09*self.test_x"""

            

            for item in lines:
                if item.id == 1:
                    if pygame.Rect.colliderect(self.rect, item.rect):
                        self.y_speed = 0
                        self.test_x = 0
                        self.y_pos -= item.height
                elif item.id == 3:
                    if pygame.Rect.colliderect(self.rect, item.rect):
                        self.y_speed = 0
                        self.test_x = 0
                        self.y_pos += item.height

                if item.id == 2:
                    if pygame.Rect.colliderect(self.rect, item.rect):
                        self.x_speed = 0
                        self.test_x = 0
                        self.x_pos += item.width
                elif item.id == 4:
                    if pygame.Rect.colliderect(self.rect, item.rect):
                        self.x_speed = 0
                        self.test_x = 0
                        self.x_pos -= item.width
            
                    
class MissleLauncher():
    def __init__(self, point, y_pos, images, id):
        self.point = point
        self.y_pos = y_pos
        self.images = images
        self.body = self.images[0]
        if(self.point == 1):
            self.x_pos = -5
            self.x_offset = self.x_pos + 75
            self.smoke_direction = -0.1
        else:
            self.x_pos = 925
            self.body = pygame.transform.rotate(self.images[0], 180).convert_alpha()
            self.x_offset = self.x_pos - 20
            self.smoke_direction = 0.1
        self.ammo = 1
        self.is_shooting = False
        self.shooting_cooldown = 100
        self.animation_cooldown = 0
        self.id = id
        self.rect = pygame.Rect(self.x_pos, self.y_pos, 50, 50)

    def draw(self):
        screen.blit(self.body, (self.x_pos, self.y_pos))

    
    
    def shoot_missle(self):
        global newid
        global total_missles
        global missles_name
        global missles
        missles_name = "missle" + str(total_missles + 1)
        if self.ammo > 0:

            if self.shooting_cooldown == 0:
                missles.append(exec("%s = None" % (missles_name)))
                for i in range(len(missles)):
                    if missles[i] == None:
                        missles[i] = Missles(self.x_pos + 75, self.y_pos + 35, "green", 20, 20, 0, 0, newid)
                        newid = newid + 1
                        self.ammo = self.ammo - 1
                self.shooting_cooldown = 100
                total_missles = total_missles + 1

                particleEffects_name = "Missle_" + str(self.id) + "_smoke"
                particleEffects.append(exec("%s = None" % (particleEffects_name)))
                for i in range(len(particleEffects)):
                    if particleEffects[i] == None:
                        particleEffects[i] = ParticleEffect((particleEffects_name + "_"), self.x_offset, (self.y_pos + 15), [[211, 211, 211, 255], [128, 128, 128, 255]], "cicle", 10, 10, 51, False, self.smoke_direction, 20, "fade", "round(random.uniform(-1,0.7),1)", "round(random.uniform(0.5,1),1)", "round(random.uniform(0.5,1.5),1)", 0)
            
            else:
                self.shooting_cooldown = self.shooting_cooldown - 1


class Particle():
    def __init__(self, x_pos, y_pos, color, shape, width, heigth, gravity, x_speed, effect, y_direction, x_speed_cap, y_speed_cap, id):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.color = color
        self.shape = shape
        self.width = width
        self.heigth = heigth
        self.gravity = gravity
        self.x_speed = x_speed
        self.effect = effect
        self.y_speed = eval(y_direction)
        self.x_vol = 0
        self.y_vol = 0
        self.x_speed_cap = eval(x_speed_cap)
        self.y_speed_cap = eval(y_speed_cap)
        self.color_tup = tuple(self.color)
        self.id = id

    def draw(self):
        #particle_surface = pygame.Surface((self.width, self.heigth), pygame.SRCALPHA)
        pygame.draw.circle(screen, self.color_tup, (self.x_pos, self.y_pos), (self.width/2))
    
    def update_pos(self):
        if self.gravity == True:
            pass
        else:
            if abs(self.x_vol) < self.x_speed_cap:
                self.x_vol = self.x_vol + self.x_speed
            if abs(self.y_vol) < self.y_speed_cap:
                self.y_vol = self.y_vol + self.y_speed
            
        self.x_pos = self.x_pos + self.x_vol
        self.y_pos = self.y_pos + self.y_vol
    
    def check_effect(self):
        if self.effect == "fade":
            fade_speed = 5
            if self.color[3] > 0:
                if (self.color[3] - fade_speed) <= 0:
                    self.color[3] = 0
                else:
                    self.color[3] = self.color[3] - fade_speed
                self.color_tup = tuple(self.color)



class ParticleEffect():
    def __init__(self, particle_name, starting_x_pos, starting_y_pos, colors, shape, width, heigth, duration, gravity, speed, amount, effect, y_direction, x_speed_cap, y_speed_cap, id):
        self.particle_name = particle_name
        self.starting_x_pos = starting_x_pos
        self.starting_y_pos = starting_y_pos
        self.colors = colors
        self.shape = shape
        self.width = width
        self.heigth = heigth
        self.duration = duration
        self.gravity = gravity
        self.speed = speed
        self.amount = amount
        self.effect = effect
        self.new_particle_name = ""
        self.particles = []
        self.y_direction = y_direction
        self.x_speed_cap = x_speed_cap
        self.y_speed_cap = y_speed_cap
        self.id = id
        self.particles_made = False
    
    def draw_particles(self):
        for particle in self.particles:
            particle.draw()

    def update_particles(self):
        global particleEffects
        if self.duration > 0:
            for particle in self.particles:
                particle.check_effect()
                particle.update_pos()
            self.duration = self.duration - 1
        else:
            del particleEffects[self.id]

    def create_particles(self):
        if self.particles_made == False:
            for i in range(self.amount):
                self.new_particle_name = self.particle_name + str(i)
                self.particles.append(exec("%s = None" % (self.new_particle_name)))
                for i in range(len(self.particles)):
                    if self.particles[i] == None:
                        self.particles[i] = Particle(self.starting_x_pos, self.starting_y_pos, self.colors[random.randint(0,(len(self.colors)-1))], self.shape, self.width, self.heigth, self.gravity, self.speed, self.effect, self.y_direction, self.x_speed_cap, self.y_speed_cap, i)
            self.particles_made = True

def end_game():
    global running
    tick = 500
    while(running):
        #setting game fps to 60
        timer.tick(fps)
        #setting screen background color to white
        screen.fill("white")
        #Updates score text based on new score
        score_text = font.render("Score: " + str(score), True, (255, 0, 0), (255, 255, 255))
        #Sends text to screen
        #Allows user to exit out of the game
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    quit()
        for item in lines:
            item.draw()
        for item in players:
            item.draw()
        for item in missleLaunchers:
            item.draw()
        mouse.update_pos(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])
        screen.blit(emptyLive, (screen_size[0] - 175, 5))
        screen.blit(emptyLive, (screen_size[0] - 115, 5))
        screen.blit(emptyLive, (screen_size[0] - 55, 5))
        if tick > 0:
            screen.blit(grey_backdrop, (0,tick))
            tick = tick - 12
        else:
            screen.blit(grey_backdrop, (0,0))
        update_buttons()
        update_texts()
        pygame.display.flip()

def reset_game():
    global screen
    global gravity
    global max_speed
    global running
    global lives
    global score
    global mouse_rect
    global bot_mode
    global total_missles
    global missles_name
    global missles
    global missleLaunchers
    screen = pygame.display.set_mode((screen_size[0], screen_size[1]))
    gravity = 0.5
    max_speed = 20
    running = True
    max_lives = 3
    lives = max_lives
    score = 0
    mouse_rect = pygame.Rect(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1], 1, 1)
    bot_mode = 0
    total_missles = 0
    missles_name = "missles"
    missles = []
    missleLaunchers = []


#Defining all global functions 

#Defining the function that updates all players in the Player class using all the class functions
def update_players():
    for item in players:
        item.draw()
        item.check_grav()
        item.x_speed = 0
        item.check_key_left()
        item.check_key_right()
        item.check_key_up()
        if(bot_mode == 1):
            item.random_move()
        item.update_pos()

#Defining the function that updates all lines in the Line class using all the class functions
def update_line():
    for item in lines:
        item.draw()
        if item.id == 1:
            item.start_y = screen_size[1]
            item.end_x = screen_size[0]
            item.end_y = screen_size[1]
            item.width = screen_size[0]
        elif item.id == 3:
            item.end_x = screen_size[0]
            item.width = screen_size[0]
        elif item.id == 4:
            item.start_x = screen_size[0]
            item.end_x = screen_size[0]
            item.end_y = screen_size[1]
            item.height = screen_size[1]
        elif item.id == 3:
            item.end_y = screen_size[1]
            item.height = screen_size[1]

def update_points():
    global score
    for item in points:
        item.draw()
        score = item.check_got(score)
    return score

def update_buttons():
    for item in buttons:
        item.draw()
        item.check_click()

def update_texts():
    global score
    text1.text = "Score: " + str(score)
    for item in texts:
        item.make_text()

def update_missles():
    for item in missles:
        item.draw()
        item.update_pos()
        item.track_player()

def update_missleLaunchers():
    global score
    global missleLaunchers_name
    global total_missleLaunchers
    global misslesLaunchers_spawn
    global missleLauncher_can_spawn
    if(score % 6 == 0 and score > 0 and missleLauncher_can_spawn == True):
        missleLauncher_can_spawn = False
        misslesLaunchers_spawn = 1
    elif(score % 6 != 0):
        missleLauncher_can_spawn = True
    if(misslesLaunchers_spawn == 1):

        missleLaunchers_name = "missleLauncher" + str(total_missleLaunchers)
        missleLaunchers.append(exec("%s = None" % (missleLaunchers_name)))
        for i in range(len(missleLaunchers)):
            if missleLaunchers[i] == None:
                spawn_y_pos = random.randint(100,400)
                #Make it so that it does not spawn a launcher where one already is
                """for i in range(len(missleLaunchers)-1):
                    if not spawn_y_pos <= missleLaunchers[i].y_pos - 40 or spawn_y_pos >= missleLaunchers[i].y_pos + 40:
                        while not spawn_y_pos <= missleLaunchers[i].y_pos - 40 or spawn_y_pos >= missleLaunchers[i].y_pos + 40:
                            spawn_y_pos = random.randint(100,400)"""
                if(random.randint(1,2) == 1):
                    missleLaunchers[i] = MissleLauncher(1, spawn_y_pos, missleLauncherSprits, total_missleLaunchers)
                else:
                    missleLaunchers[i] = MissleLauncher(2, spawn_y_pos, missleLauncherSprits, total_missleLaunchers)
        

        total_missleLaunchers = total_missleLaunchers + 1
        misslesLaunchers_spawn = 0
            
    if(len(missleLaunchers) > 0):
        for item in missleLaunchers:
            item.shoot_missle()
            item.draw()

def update_lives():
    global lives
    global newid
    if lives <= 0:
        screen.blit(emptyLive, (screen_size[0] - 175, 5))
        screen.blit(emptyLive, (screen_size[0] - 115, 5))
        screen.blit(emptyLive, (screen_size[0] - 55, 5))
        newid = 0
        end_game()
    elif lives == 1:
        screen.blit(emptyLive, (screen_size[0] - 175, 5))
        screen.blit(emptyLive, (screen_size[0] - 115, 5))
        screen.blit(fullLive, (screen_size[0] - 55, 5))
    elif lives == 2:
        screen.blit(emptyLive, (screen_size[0] - 175, 5))
        screen.blit(fullLive, (screen_size[0] - 115, 5))
        screen.blit(fullLive, (screen_size[0] - 55, 5))
    else:
        screen.blit(fullLive, (screen_size[0] - 175, 5))
        screen.blit(fullLive, (screen_size[0] - 115, 5))
        screen.blit(fullLive, (screen_size[0] - 55, 5))

def update_enemey_count():
    global total_missleLaunchers
    global total_missles
    total_missles = len(missles)
    total_missleLaunchers = len(missleLaunchers)

def update_particle_effects():
    for item in particleEffects:
        item.create_particles()
        item.update_particles()
        item.draw_particles()

#Creating the player and assigning it the the Player class
player1 = Player(700, 200, "black", 50, 50, 0, 0, 1)



#Adding the player to the players list so that it can easily be updated using the update_player function
players = [player1]

#Creating all the lines and assigning them to the Lines class
bottom_wall = Lines(0, screen_size[1], screen_size[0], screen_size[1], "black", screen_size[0], wall_thickness, wall_thickness, 1)
top_wall = Lines(0, 0, screen_size[0], 0, "black", screen_size[0], wall_thickness, wall_thickness, 3)
right_wall = Lines(screen_size[0], 0, screen_size[0], screen_size[1], "black", wall_thickness, screen_size[1], wall_thickness, 4)
left_wall = Lines(0, 0, 0, screen_size[1], "black", wall_thickness, screen_size[1], wall_thickness, 2)
middle_plat1 = Lines(100, 400, 300, 400, "black", 200, wall_thickness, wall_thickness, 5)
middle_plat2 = Lines(400, 300, 600, 300, "black", 200, wall_thickness, wall_thickness, 5)
middle_plat3 = Lines(700, 400, 900, 400, "black", 200, wall_thickness, wall_thickness, 5)
middle_plat4 = Lines(100, 200, 300, 200, "black", 200, wall_thickness, wall_thickness, 5)
middle_plat5 = Lines(700, 200, 900, 200, "black", 200, wall_thickness, wall_thickness, 5)

#Adding the lines to the lines list so that it can easily be updated using the update_line function
lines = [bottom_wall, top_wall, right_wall, left_wall, middle_plat1, middle_plat2, middle_plat3, middle_plat4, middle_plat5]
 
point1 = Points(500, 250, 30, "red")
points = [point1]

button1 = Buttons((0, 100, 255), None, "black", 415, 350, 160, 100, "Back to Menu", 1)
buttons = [button1]

missleLaunchers = []
missles = []
total_missles = len(missles)
total_missleLaunchers = len(missleLaunchers)



mouse = Mouse(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[0])

text1 = Text("Score: " + str(score), None, (255, 0, 0), (0 + wall_thickness), (0 + wall_thickness), 1)
texts = [text1]

particleEffects = []

#Y-direction for smoke behind,,,, random.randint(-1,1)
#Main while loop that runs that game


def runGame():
    global running
    global fps
    global score
    global bot_mode
    global screen
    global screen_size
    global width
    global height
    while running:
        #setting game fps to 60
        timer.tick(fps)
        #setting screen background color to white
        screen.fill("white")

        #Allows user to exit out of the game
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    quit()

        #updates the lines, and players so each tiem it iteerates through the loop
        key=pygame.key.get_pressed()
        if key[pygame.K_z]:
            if bot_mode == 0: 
                bot_mode = 1
            elif bot_mode == 1:
                bot_mode = 0

        score = update_points()
        update_missleLaunchers()
        update_line()
        update_texts()
        update_players()
        update_missles()
        mouse.update_pos(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])
        update_lives()
        screen_size[0], screen_size[1] = screen.get_size()
        update_enemey_count()
        if len(particleEffects) > 0:
            update_particle_effects()
        #Displays the screen so that the user can see it.
        pygame.display.flip()