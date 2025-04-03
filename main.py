import pygame
import button
from os import path
from pygame.locals import *
import pickle
import math
import re
#add more levels
pygame.init()

#declare basic variables and constants. CAPS are constants
clock = pygame.time.Clock()
FPS = 60
start_time = 0
pause_start_time = 0
high_score = True
SCREEN_WIDTH = 840
SCREEN_HEIGHT = 660
score = []
SIDE_MARGIN = 300

#import images, declare screen
screen = pygame.display.set_mode((SCREEN_WIDTH + SIDE_MARGIN, SCREEN_HEIGHT))
pygame.display.set_caption('Pixel Stuck')
icon_img = pygame.image.load('img/tile/9.png')
swap_img = pygame.image.load('img/tile/4.png').convert_alpha()
swap_img = pygame.transform.scale(swap_img, (60, 60)) 
hook_img = pygame.image.load('img/tile/3.png').convert_alpha()
hook_img = pygame.transform.scale(hook_img, (60, 60)) 
tut_img = pygame.image.load('img/ui/tutorial.png')
back_img = pygame.image.load('img/ui/back.png')
broke_img = pygame.image.load('img/ui/Broken.png').convert_alpha()
broke_img = pygame.transform.scale(broke_img, (57, 57)) 
key_img = pygame.image.load('img/ui/key.jpg')
pygame.display.set_icon(icon_img)

#grid
MAX_COLS = 14
ROWS = 11
TILE_SIZE = SCREEN_HEIGHT // ROWS

#in game variables
tutorial = False
swap_range = False
level = 0
hook_list = [0, 3, 2, 2, 1, 1]
swap_list = [1, 0, 1, 2, 0, 1]
hidden_hook_list = [5, 0]
hidden_swap_list = [0, 1]
swap_count = 1
hook_count = 0
game_over = 0
current_tile = -1
max_levels = 5
max_hidden = 101
facing = 1 #right
player_movement = True
main_menu = True
allow_hook = False
allow_swap = False
get_hooked_r = False
get_hooked_l = False
get_hooked_u = False
swap_1_x = []
swap_1_y = []
swap_1 = []
swap_2 = []
swap_2_x = []
swap_2_y = []
won_tile = []
yet_1 = False
yet_2 = False
count = 0
hidden = False
topstand = False

#colours
GREEN = (144, 201, 120)
WHITE = (255, 255, 255)
RED = (255,69,0)
BLUE = (0, 0, 255)
VIOLET = (138,43,226)

#font
font_level = pygame.font.SysFont('sitkasmallsitkatextbolditalicsitkasubheadingbolditalicsitkaheadingbolditalicsitkadisplaybolditalicsitkabannerbolditalic', 45)
font_sub = pygame.font.SysFont('verdana', 30)
font_score = pygame.font.SysFont('bahnschrift', 40)

#load images
background1_img = pygame.image.load('img/background/1.png')
win_back_img = pygame.image.load('img/background/win.png')
border_img = pygame.image.load('img/background/border.png').convert_alpha()
border_img = pygame.transform.scale(border_img, (250, 300)) 
level_border_img = pygame.image.load('img/background/level_border.png').convert_alpha()
level_border_img = pygame.transform.scale(level_border_img, (250, 75)) 
restart_img = pygame.image.load('img/buttons/restart_btn.png')
start_img = pygame.image.load('img/buttons/start_btn.png')
exit_img = pygame.image.load('img/buttons/exit_btn.png')
exit_active_img = pygame.image.load('img/buttons/exit_btn.png').convert_alpha()
exit_active_img = pygame.transform.scale(exit_active_img, (120, 42)) 
tutorial_img = pygame.image.load('img/ui/tutorial_text.png')
trophy_img = pygame.image.load('img/ui/trophy.png').convert_alpha()
trophy_img = pygame.transform.scale(trophy_img, (60, 60))

#load image rects
hook_rect = hook_img.get_rect()
hook_rect.x = SCREEN_WIDTH + 70
hook_rect.y = 500

swap_rect = swap_img.get_rect()
swap_rect.x = SCREEN_WIDTH + 200
swap_rect.y = 500

broke_rect = broke_img.get_rect()
broke_rect.x = 370
broke_rect.y = 115



#scale rect size for exit and restart img
exit_rect = exit_img.get_rect()
exit_rect = exit_rect.inflate(exit_rect.w, exit_rect.h)
exit_rect.x = SCREEN_WIDTH + 300 - exit_rect.w
exit_rect.y = SCREEN_HEIGHT - exit_rect.h
won_tile.append(exit_rect)

#declare img and rects for end screen
trophy_rect = trophy_img.get_rect()
trophy_rect.x, trophy_rect.y = 700, 150
trophy_rect_2 = trophy_rect.copy()
trophy_rect_2.x, trophy_rect_2.y = 790, 500
trophy_rect_3 = trophy_rect.copy()
trophy_rect_3.x, trophy_rect_3.y = 300, 240
trophy_rect_5 = trophy_rect.copy()
trophy_rect_5.x, trophy_rect_5.y = 550, 600
trophy_rect_6 = trophy_rect.copy()
trophy_rect_6.x, trophy_rect_6.y = 1000, 40
trophy_rect_7 = trophy_rect.copy()
trophy_rect_7.x, trophy_rect_7.y = 50, 100

won_tile.append(trophy_rect)
won_tile.append(trophy_rect_2)
won_tile.append(trophy_rect_3)
won_tile.append(trophy_rect_5)
won_tile.append(trophy_rect_6)
won_tile.append(trophy_rect_7)
    
restart_rect = restart_img.get_rect()
restart_rect = restart_rect.inflate(restart_rect.w, restart_rect.h)
restart_rect.x = SCREEN_WIDTH + 300 - restart_rect.w
restart_rect.y = SCREEN_HEIGHT - restart_rect.h - exit_rect.h
won_tile.append(restart_rect)

highscore_rect = pygame.Rect((0, SCREEN_HEIGHT - 450), (370, 450))
won_tile.append(highscore_rect)

#load sounds
swap_sound = pygame.mixer.Sound('sounds/swap.wav')
hook_sound = pygame.mixer.Sound('sounds/grab.wav')
click_sound = pygame.mixer.Sound('sounds/click.wav')
jump_sound = pygame.mixer.Sound('sounds/jump.wav')
pick_sound = pygame.mixer.Sound('sounds/pickup.wav')
select_sound = pygame.mixer.Sound('sounds/select.wav')

#music = pygame.mixer.music.load('sounds/bgmusic.mp3')
#pygame.mixer.music.play(-1)
#pygame.mixer.music.set_volume(0.2)

#draw grid
def draw_grid():
    THICK_COUNT = 2
    #vertical lines, 3x3 in red and small squares in white
    for c in range (MAX_COLS + 1):
        if THICK_COUNT == 3:
            pygame.draw.line(screen, RED, (c * TILE_SIZE, 0), (c * TILE_SIZE, SCREEN_HEIGHT), 3)
            THICK_COUNT = 1
        else: 
            pygame.draw.line(screen, WHITE, (c * TILE_SIZE, 0), (c * TILE_SIZE, SCREEN_HEIGHT))
            THICK_COUNT += 1
    #horizontal lines
    THICK_COUNT = 2
    for c in range (ROWS + 1):
        if THICK_COUNT == 3:
            pygame.draw.line(screen, RED, (0, c * TILE_SIZE), (SCREEN_WIDTH, c * TILE_SIZE), 3)  
            THICK_COUNT = 1
        else: 
            pygame.draw.line(screen, WHITE, (0, c * TILE_SIZE), (SCREEN_WIDTH, c * TILE_SIZE)) 
            THICK_COUNT += 1

#find the big square the player is in and the mouse
def player_square(x, y):
    sprite_rb_square = -1
    sprite_lb_square = -1
    #find mouse pos
    if y < 4:
        if x < 4:
            mouse_square = 1
        elif x < 7:
            mouse_square = 2
        elif x < 10:
            mouse_square = 3
        else:
            mouse_square = 4
    elif y < 7:
        if x < 4:
            mouse_square = 5
        elif x < 7:
            mouse_square = 6
        elif x < 10:
            mouse_square = 7
        elif x < 14:
            mouse_square = 8
    elif y < 10:
        if x < 4:
            mouse_square = 9
        elif x < 7:
            mouse_square = 10
        elif x < 10:
            mouse_square = 11
        elif x < 14:
            mouse_square = 12 
    
    #sprite pos left hitbox
    if sprite_y < 4:
        if sprite_x_l < 4:
            sprite_l_square = 1
        elif sprite_x_l < 7:
            sprite_l_square = 2
        elif sprite_x_l < 10:
            sprite_l_square = 3
        else:
            sprite_l_square = 4
        if topstand:
            sprite_lb_square = sprite_l_square+4
    elif sprite_y < 7:
        if sprite_x_l < 4:
            sprite_l_square = 5
        elif sprite_x_l < 7:
            sprite_l_square = 6
        elif sprite_x_l < 10:
            sprite_l_square = 7
        elif sprite_x_l < 14:
            sprite_l_square = 8
        if topstand:
            sprite_lb_square = sprite_l_square+4
            
    elif sprite_y < 10:
        if sprite_x_l < 4:
            sprite_l_square = 9
        elif sprite_x_l < 7:
            sprite_l_square = 10
        elif sprite_x_l < 10:
            sprite_l_square = 11
        elif sprite_x_l < 14:
            sprite_l_square = 12 
        
    #sprite pos right hitbox
    if sprite_y < 4:
        if sprite_x_r < 4:
            sprite_r_square = 1
        elif sprite_x_r < 7:
            sprite_r_square = 2
        elif sprite_x_r < 10:
            sprite_r_square = 3
        else:
            sprite_r_square = 4
        if topstand:
            sprite_rb_square = sprite_r_square+4
    elif sprite_y < 7:
        if sprite_x_r < 4:
            sprite_r_square = 5
        elif sprite_x_r < 7:
            sprite_r_square = 6
        elif sprite_x_r < 10:
            sprite_r_square = 7
        elif sprite_x_r < 14:
            sprite_r_square = 8
        if topstand:
            sprite_rb_square = sprite_r_square+4
    elif sprite_y < 10:
        if sprite_x_r < 4:
            sprite_r_square = 9
        elif sprite_x_r < 7:
            sprite_r_square = 10
        elif sprite_x_r < 10:
            sprite_r_square = 11
        elif sprite_x_r < 14:
            sprite_r_square = 12 
        
    
    
    #check for flag
    for flag_y, row in enumerate(world_data):
        for flag_x, tile in enumerate(row):
            if tile ==2:
                if flag_y < 4:
                    if flag_x < 4:
                        flag_square = 1
                    elif flag_x < 7:
                        flag_square = 2
                    elif flag_x < 10:
                        flag_square = 3
                    else:
                        flag_square = 4
                elif flag_y < 7:
                    if flag_x < 4:
                        flag_square = 5
                    elif flag_x < 7:
                        flag_square = 6
                    elif flag_x < 10:
                        flag_square = 7
                    elif flag_x < 14:
                        flag_square = 8
                elif flag_y < 10:
                    if flag_x < 4:
                        flag_square = 9
                    elif flag_x < 7:
                        flag_square = 10
                    elif flag_x < 10:
                        flag_square = 11
                    elif flag_x < 14:
                        flag_square = 12   
                
    #check if overlap between mouse, sprite square and flag square
    if mouse_square == sprite_l_square or mouse_square == sprite_r_square or mouse_square == flag_square or mouse_square == sprite_rb_square or mouse_square == sprite_lb_square:
        return False
    else:
        return True
  


def swap_collide(x, y):
    if y < 4:
        if x < 4:
            mouse_square = 1
        elif x < 7:
            mouse_square = 2
        elif x < 10:
            mouse_square = 3
        else:
            mouse_square = 4
    elif y < 7:
        if x < 4:
            mouse_square = 5
        elif x < 7:
            mouse_square = 6
        elif x < 10:
            mouse_square = 7
        elif x < 14:
            mouse_square = 8
    elif y < 10:
        if x < 4:
            mouse_square = 9
        elif x < 7:
            mouse_square = 10
        elif x < 10:
            mouse_square = 11
        elif x < 14:
            mouse_square = 12 
     
     
    #used square       
    if used_y < 4:
        if used_x < 4:
            used_square = 1
        elif used_x < 7:
            used_square = 2
        elif used_x < 10:
            used_square = 3
        else:
            used_square = 4
    elif used_y < 7:
        if used_x < 4:
            used_square = 5
        elif used_x < 7:
            used_square = 6
        elif used_x < 10:
            used_square = 7
        elif used_x < 14:
            used_square = 8
    elif used_y < 10:
        if used_x < 4:
            used_square = 9
        elif used_x < 7:
            used_square = 10
        elif used_x < 10:
            used_square = 11
        elif used_x < 14:
            used_square = 12
            
    if mouse_square == used_square:
        return False
    else:
        return True
    
#draw text
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))
        
        
        
def reset_level(level):
    global world_data
    player.reset(60, SCREEN_HEIGHT - 65)
    swamp_group.empty()
    flag_group.empty()
    swap_group.empty()
    hook_group.empty()
    
    

    #load in level data and create world
    if path.exists(f'level{level}_data'):
        pickle_in = open(f'level{level}_data', 'rb')
        world_data = pickle.load(pickle_in)
    world = World(world_data)

    return world


   
class World():
    def __init__(self, data):
        self.tile_list = []
        
        
        gold_img = pygame.image.load('img/tile/0.png')
        block1_img = pygame.image.load('img/tile/5.png')
        block2_img = pygame.image.load('img/tile/6.png')
        block3_img = pygame.image.load('img/tile/7.png')
        block4_img = pygame.image.load('img/tile/8.png')
        lock_img = pygame.image.load('img/tile/9.png')
        row_count = 0
        for row in data:
            col_count = 0
            for tile in row:
                if tile == 0 :
                    img = pygame.transform.scale(gold_img, (TILE_SIZE, TILE_SIZE))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * TILE_SIZE
                    img_rect.y = row_count * TILE_SIZE
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == 5 :
                    img = pygame.transform.scale(block1_img, (TILE_SIZE, TILE_SIZE))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * TILE_SIZE
                    img_rect.y = row_count * TILE_SIZE
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == 6 :
                    img = pygame.transform.scale(block2_img, (TILE_SIZE, TILE_SIZE))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * TILE_SIZE
                    img_rect.y = row_count * TILE_SIZE
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == 7 :
                    img = pygame.transform.scale(block3_img, (TILE_SIZE, TILE_SIZE))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * TILE_SIZE
                    img_rect.y = row_count * TILE_SIZE
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == 8 :
                    img = pygame.transform.scale(block4_img, (TILE_SIZE, TILE_SIZE))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * TILE_SIZE
                    img_rect.y = row_count * TILE_SIZE
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == 9 :
                    img = pygame.transform.scale(lock_img, (TILE_SIZE, TILE_SIZE))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * TILE_SIZE
                    img_rect.y = row_count * TILE_SIZE
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == 1:
                    swamp = Swamp(col_count * TILE_SIZE, row_count * TILE_SIZE)
                    swamp_group.add(swamp)
                if tile == 2:
                    flag = Flag(col_count * TILE_SIZE, row_count * TILE_SIZE)
                    flag_group.add(flag)
                if tile == 3:
                    hook = Hook(col_count * TILE_SIZE + (TILE_SIZE // 2), row_count * TILE_SIZE +  (TILE_SIZE // 2))
                    hook_group.add(hook)  
                if tile == 4:
                    swap = Swap(col_count * TILE_SIZE + (TILE_SIZE // 2), row_count * TILE_SIZE +  (TILE_SIZE // 2))
                    swap_group.add(swap)                    
                
                
                
                col_count += 1
            row_count +=1
            
            
    def draw(self):
        for tile in self.tile_list:
            screen.blit(tile[0], tile[1])

#player
class Player():
    def __init__(self, x, y):
        self.reset(x, y)

    def update(self, game_over):
        global facing, sprite_x_r, sprite_x_l, sprite_y, sprite_x_c, hidden, topstand
        dx = 0
        dy = 0
        walk_cooldown = 5

        #get keypresses
        if game_over == 0:
            key = pygame.key.get_pressed()
            if key[pygame.K_SPACE]and self.jumped == False and self.in_air == False and player_movement == True: 
                self.vel_y = -10
                self.jumped = True
                jump_sound.play()
            if key[pygame.K_UP]and self.jumped == False and self.in_air == False and player_movement == True: 
                self.vel_y = -10
                self.jumped = True
                jump_sound.play()
            if key[pygame.K_SPACE] == False:
                self.jumped = False
            if key[pygame.K_UP] == False:
                self.jumped = False
            if key[pygame.K_LEFT] and player_movement == True or key[pygame.K_a]and player_movement == True:
                dx -= 3
                self.counter += 1
                self.direction = -1
                facing = -1
            if key[pygame.K_RIGHT] and player_movement == True or key[pygame.K_d]and player_movement == True:
                dx += 3
                self.counter += 1
                self.direction = 1
                facing = 1
            if key[pygame.K_LEFT] == False and key[pygame.K_RIGHT] == False and key[pygame.K_d] == False and key[pygame.K_a] == False:
                self.counter = 0
                self.index = 0
                if self.direction == 1:
                    self.image = self.images_right[self.index]
                if self.direction == -1:
                    self.image = self.images_left[self.index]
                
    
    
            #handle animation
            if self.counter > walk_cooldown:
                self.counter = 0	
                self.index += 1
                if self.index >= len(self.images_right):
                    self.index = 0
                if self.direction == 1:
                    self.image = self.images_right[self.index]
                if self.direction == -1:
                    self.image = self.images_left[self.index]
    
    
            #add gravity
            self.vel_y += 0.7
            if self.vel_y > 10:
                self.vel_y = 10
            dy += self.vel_y
    
            #check for collision
            self.in_air = True
            for tile in world.tile_list:
                #check for collision in x direction
                if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height) and not tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                    dx = 0
                #check for collision in y direction
                if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height) :
                    #check if below the ground i.e. jumping
                    if self.vel_y < 0:
                        for tile in world.tile_list: #fixed
                            if self.direction == 1:
                                if tile[1].colliderect(self.rect.x, self.rect.y, self.width + 15, self.height):  #check if facing side blocked
                                    if self.rect.y  - tile[1].y <20 and self.rect.y  - tile[1].y > -20:
                                        self.vel_y = 0
                            elif self.direction == -1:
                                if tile[1].colliderect(self.rect.x - 15, self.rect.y, self.width, self.height): 
                                    if self.rect.y  - tile[1].y <20 and self.rect.y  - tile[1].y > -20:
                                        self.vel_y = 0
                        #dy = tile[1].bottom - self.rect.top
                        #self.vel_y = 0
                        pass
                    #check if above the ground i.e. falling
                    elif self.vel_y >= 0 and tile[1].top - self.rect.bottom > -46:
                        dy = tile[1].top - self.rect.bottom
                        self.vel_y = 0
                        self.in_air = False
                        
            #check collision with enemy
            if pygame.sprite.spritecollide(self, swamp_group, False):
                game_over = -1
                    
            #check for collision with exit
            if pygame.sprite.spritecollide(self, flag_group, False):
                game_over = 1


        elif game_over == -1:
            self.image = self.dead_image
            if self.rect.y > 200:
                self.rect.y -= 5
                
        elif game_over == 1:
            key = pygame.key.get_pressed()
            if key[pygame.K_SPACE]: 
                self.vel_y = -10
                jump_sound.play()
            if key[pygame.K_UP]: 
                self.vel_y = -10
                jump_sound.play()
            if key[pygame.K_LEFT] and player_movement == True or key[pygame.K_a]:
                dx -= 3
                self.counter += 1
                self.direction = -1
                facing = -1
            if key[pygame.K_RIGHT] and player_movement == True or key[pygame.K_d]:
                dx += 3
                self.counter += 1
                self.direction = 1
                facing = 1
            if key[pygame.K_LEFT] == False and key[pygame.K_RIGHT] == False and key[pygame.K_d] == False and key[pygame.K_a] == False:
                self.counter = 0
                self.index = 0
                if self.direction == 1:
                    self.image = self.images_right[self.index]
                if self.direction == -1:
                    self.image = self.images_left[self.index]
                    
            
            
            #change for collision win
            for tile in won_tile:
                #check for collision in x direction
                if tile.colliderect(self.rect.x + dx, self.rect.y, self.width, self.height) and not tile.colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                    dx = 0
                #check for collision in y direction
                if tile.colliderect(self.rect.x, self.rect.y + dy, self.width, self.height) :
                    #below
                    if self.vel_y < 0:
                        dy = tile.bottom - self.rect.top
                        self.vel_y = 0
                        pass                    
                    #check if above the ground i.e. falling
                    if self.vel_y >= 0 and tile.top - self.rect.bottom > -46:
                        dy = tile.top - self.rect.bottom
                        self.vel_y = 0
                        self.in_air = False  
            if level <101:
                if self.rect.x > 960:
                    self.rect.x = 0
                if self.rect.x < 0:
                    self.rect.x = 960
                if self.rect.y > SCREEN_HEIGHT:
                    self.rect.y = 0
                if self.rect.y < 0:
                    self.rect.y = SCREEN_HEIGHT
            if broke_rect.colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                if not hidden and level < 101:  
                    hidden = True
                
        
        
        
            #handle animation
            if self.counter > walk_cooldown:
                self.counter = 0	
                self.index += 1
                if self.index >= len(self.images_right):
                    self.index = 0
                if self.direction == 1:
                    self.image = self.images_right[self.index]
                if self.direction == -1:
                    self.image = self.images_left[self.index]
        
        
            #add gravity
            self.vel_y += 0.8
            if self.vel_y > 10:
                self.vel_y = 10
            dy += self.vel_y            
            
            
        #update player coordinates
        self.rect.x += dx
        self.rect.y += dy
        #player coords to check collision of hook
        sprite_x_r = (self.rect.x + TILE_SIZE-16)  // TILE_SIZE
        sprite_x_l = self.rect.x  // TILE_SIZE
        sprite_x_c = (((self.rect.x + TILE_SIZE-16) + self.rect.x) // 2) // TILE_SIZE
        sprite_y = self.rect.y // TILE_SIZE
        if self.rect.y == 370 or self.rect.y == 190:
            topstand = True
        else:
            topstand = False
        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
            dy = 0

        #draw player onto screen
        screen.blit(self.image, self.rect)
        
        # Draw hitbox visualization
        pygame.draw.rect(screen, (255, 0, 0), self.rect, 1)  # Red rectangle for player hitbox
        
        return game_over
    
    def reset(self, x, y):
        self.images_right = []
        self.images_left = []
        self.dead_image = pygame.image.load('img/characters/ghost.png')
        self.index = 0
        self.counter = 0
        for num in range(1, 3):
            img_right = pygame.image.load(f'img/characters/guy{num}.png')
            img_right = pygame.transform.scale(img_right, ( TILE_SIZE-15 , TILE_SIZE - 10))
            img_left = pygame.transform.flip(img_right, True, False)
            self.images_right.append(img_right)
            self.images_left.append(img_left)
        self.image = self.images_right[self.index]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.vel_y = 0
        self.jumped = False
        self.direction = 1
        





class Swamp(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load('img/tile/1.png')
        self.image = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
        self.rect = self.image.get_rect()
        self.rect.x = x + 1  # Move right by 1 pixel
        self.rect.y = y + 1  # Move down by 1 pixel
        self.rect.width = TILE_SIZE - 2  # Reduce width by 2 pixels
        self.rect.height = TILE_SIZE - 2  # Reduce height by 2 pixels
            
class Flag(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load('img/tile/2_1.png')
        self.image = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
class Hook(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load('img/tile/3.png')
        self.image = pygame.transform.scale(img, (TILE_SIZE // 2, TILE_SIZE // 2))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        
class Swap(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load('img/tile/4.png')
        self.image = pygame.transform.scale(img, (TILE_SIZE // 2, TILE_SIZE // 2))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)   
      
      
player = Player(60, SCREEN_HEIGHT - 65)


swamp_group = pygame.sprite.Group()
flag_group = pygame.sprite.Group()
hook_group = pygame.sprite.Group()
swap_group = pygame.sprite.Group()

            
if path.exists(f'level{level}_data'):
    pickle_in = open(f'level{level}_data', 'rb')
    world_data = pickle.load(pickle_in)
world = World(world_data)
        
#buttons
restart_button = button.Button(SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2 + 100, restart_img, 1)
restart_button_active = button.Button(SCREEN_WIDTH + 20, 100, restart_img, 1)
tutorial_button = button.Button(SCREEN_WIDTH // 2, SCREEN_HEIGHT //2 - 50, tutorial_img, 1)
start_button = button.Button(SCREEN_WIDTH // 2 + 15, SCREEN_HEIGHT //2 - 250, start_img, 2)
exit_button = button.Button(SCREEN_WIDTH // 2 + 35, SCREEN_HEIGHT //2 + 100, exit_img, 2)
hook_button = button.Button(SCREEN_WIDTH + 70, 510, hook_img, 1)
swap_button = button.Button(SCREEN_WIDTH + 200, 500, swap_img, 1)
back_button = button.Button(20, 540, back_img, 1)
exit_button_active = button.Button(SCREEN_WIDTH + 170, 100, exit_active_img, 1)
exit_button_end = button.Button(SCREEN_WIDTH + 300 - exit_rect.w, SCREEN_HEIGHT - exit_rect.h, exit_img, 2)
restart_button_end = button.Button(SCREEN_WIDTH + 300 - restart_rect.w, SCREEN_HEIGHT - restart_rect.h - exit_rect.h, restart_img, 2)

run = True
while run:
    
    clock.tick(FPS)
    screen.blit(background1_img, (0,0))
    
    for event in pygame.event.get():
        
        if event.type == pygame.QUIT:
            run = False    
        
        if event.type == pygame.KEYDOWN:
            # Cheat code: Numpad period key gives +5 swaps and +5 hooks
            if event.key == pygame.K_KP_PERIOD:
                swap_count += 5
                hook_count += 5
                pick_sound.play()  # Play pickup sound for feedback
                
            if (event.key == pygame.K_RIGHT or event.key == pygame.K_d) and allow_hook == True and hook_count > 0 and world_data[sprite_y][sprite_x_r + 1] == -1:
                get_hooked_r = True
            if (event.key == pygame.K_LEFT or event.key == pygame.K_a) and allow_hook == True and hook_count > 0 and world_data[sprite_y][sprite_x_l - 1] == -1:
                get_hooked_l = True
            if (event.key == pygame.K_UP or event.key == pygame.K_w)and allow_hook == True and hook_count > 0 and world_data[sprite_y - 1][sprite_x_r] == -1 and world_data[sprite_y - 1][sprite_x_l] == -1:
                get_hooked_u = True
                
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and swap_range == True and allow_swap == True:
            swap_sound.play()
            if yet_1 == False:
                used_x = x
                used_y = y
                if y < 4:
                    if x < 4:
                        for i in range (1, 4):
                            swap_1_y.append(i)
                            swap_1_x.append(i)
                    elif x < 7:
                        for i in range (1, 4):
                            swap_1_y.append(i)
                        for i in range (4, 7):
                            swap_1_x.append(i)
                    elif x < 10:
                        for i in range (1, 4):
                            swap_1_y.append(i)
                        for i in range (7, 10):
                            swap_1_x.append(i)    
                    else:
                        for i in range (1, 4):
                            swap_1_y.append(i)
                        for i in range (10, 13):
                            swap_1_x.append(i)
                elif y < 7:
                    if x < 4:
                        for i in range (4, 7):
                            swap_1_y.append(i)
                        for i in range (1, 4):
                            swap_1_x.append(i)
                    elif x < 7:
                        for i in range (4, 7):
                            swap_1_y.append(i)
                            swap_1_x.append(i)
                    elif x < 10:
                        for i in range (4, 7):
                            swap_1_y.append(i)
                        for i in range (7, 10):
                            swap_1_x.append(i)
                    elif x < 14:
                        for i in range (4, 7):
                            swap_1_y.append(i)
                        for i in range (10, 13):
                            swap_1_x.append(i)
                elif y < 10:
                    if x < 4:
                        for i in range (7, 10):
                            swap_1_y.append(i)
                        for i in range (1, 4):
                            swap_1_x.append(i)                    
                    elif x < 7:
                        for i in range (7, 10):
                            swap_1_y.append(i)   
                        for i in range (4, 7):
                            swap_1_x.append(i)
                    elif x < 10:
                        for i in range (7, 10):
                            swap_1_y.append(i)   
                        for i in range (7,10):
                            swap_1_x.append(i)
                    elif x < 14:
                        for i in range (7, 10):
                            swap_1_y.append(i)   
                        for i in range (10,13):
                            swap_1_x.append(i)  
            
                yet_1 = True
            elif yet_2 == False and swap_range == True and swap_collide(x, y) == True:
                if y < 4:
                    if x < 4:
                        for i in range (1, 4):
                            swap_2_y.append(i)
                            swap_2_x.append(i)
                    elif x < 7:
                        for i in range (1, 4):
                            swap_2_y.append(i)
                        for i in range (4, 7):
                            swap_2_x.append(i)
                    elif x < 10:
                        for i in range (1, 4):
                            swap_2_y.append(i)
                        for i in range (7, 10):
                            swap_2_x.append(i) 
                    else:
                        for i in range (1, 4):
                            swap_2_y.append(i)
                        for i in range (10, 13):
                            swap_2_x.append(i)                         
                elif y < 7:
                    if x < 4:
                        for i in range (4, 7):
                            swap_2_y.append(i)
                        for i in range (1, 4):
                            swap_2_x.append(i)
                    elif x < 7:
                        for i in range (4, 7):
                            swap_2_y.append(i)
                            swap_2_x.append(i)
                    elif x < 10:
                        for i in range (4, 7):
                            swap_2_y.append(i)
                        for i in range (7, 10):
                            swap_2_x.append(i)
                    elif x < 14:
                        for i in range (4, 7):
                            swap_2_y.append(i)
                        for i in range (10, 13):
                            swap_2_x.append(i)
                elif y < 10:
                    if x < 4:
                        for i in range (7, 10):
                            swap_2_y.append(i)
                        for i in range (1, 4):
                            swap_2_x.append(i)                         
                    elif x < 7:
                        for i in range (7, 10):
                            swap_2_y.append(i)   
                        for i in range (4, 7):
                            swap_2_x.append(i)
                    elif x < 10:
                        for i in range (7, 10):
                            swap_2_y.append(i)   
                        for i in range (7,10):
                            swap_2_x.append(i)
                    elif x < 14:
                        for i in range (7, 10):
                            swap_2_y.append(i)   
                        for i in range (10,13):
                            swap_2_x.append(i)                         
                yet_2 = True
            
    if main_menu == True:
        if exit_button.draw(screen):
            click_sound.play()
            run = False
        if start_button.draw(screen):
            click_sound.play()
            main_menu = False
        if tutorial_button.draw(screen):
            main_menu = False
            click_sound.play()
            tutorial = True
    elif tutorial == True:
        screen.blit(tut_img, (0, 0))
        if back_button.draw(screen):
            click_sound.play()
            main_menu = True
            tutorial = False
    else:   
        pause_end_time = pygame.time.get_ticks()
        draw_grid()
        world.draw()
        #UI
        screen.blit(level_border_img, (SCREEN_WIDTH + 30 , 10))
        draw_text('Gadgets', font_sub, WHITE, SCREEN_WIDTH + 90, 150)
        screen.blit(border_img, (SCREEN_WIDTH + 30 , 200))
        screen.blit(hook_img, (SCREEN_WIDTH + 80,260))
        screen.blit(swap_img, (SCREEN_WIDTH + 80,370))
        
        
        
        
        if game_over == 0:
            #if timer not yet started, start clock
            if start_time == 0:
                start_time = pygame.time.get_ticks()
            #if a pause happened, minus paused time from total time
            if pause_end_time > pause_start_time and pause_start_time > 0:
                start_time += (pause_end_time - pause_start_time)
                pause_start_time = 0
            counting_time = pygame.time.get_ticks() - start_time
            # change milliseconds into seconds #fix pls
            counting_minutes = math.floor(counting_time/60000)
            counting_seconds = str( (counting_time%60000)/1000 ).zfill(3)
            counting_string = "{:.0f}".format(counting_minutes)
            draw_text(counting_string + "m" + counting_seconds + "s", font_score, RED, SCREEN_WIDTH+75, 600)   
            
            
            draw_text(f'Level: {level}', font_level, RED, SCREEN_WIDTH + 60, 25)
            if exit_button_active.draw(screen):
                click_sound.play()
                pause_start_time = pygame.time.get_ticks()
                main_menu = True
                world_data = []
                world = reset_level(level)  
                if hidden:
                    hook_count = hidden_hook_list[level-100]
                    swap_count = hidden_swap_list[level-100]     
                else:
                    hook_count = hook_list[level]
                    swap_count = swap_list[level]                    
            if restart_button_active.draw(screen):
                click_sound.play()
                world_data = []
                world = reset_level(level)
                game_over = 0   
                draw_text(f'Level: {level}', font_level, RED, SCREEN_WIDTH + 60, 25)
                if hidden:
                    hook_count = hidden_hook_list[level-100]
                    swap_count = hidden_swap_list[level-100]     
                else:
                    hook_count = hook_list[level]
                    swap_count = swap_list[level]                
                draw_text('X ' + str(swap_count), font_score, GREEN, SCREEN_WIDTH + 180, 390)
                draw_text('X ' + str(hook_count), font_score, GREEN, SCREEN_WIDTH + 180, 265)                
            #update score
            #check if a hook has been collected
            collide_swap = pygame.sprite.spritecollide(player, swap_group, True)
            if collide_swap:
                for swap in collide_swap:
                    swap_colx = swap.rect.x
                    swap_coly = swap.rect.y
                    world_data[swap_coly // TILE_SIZE][swap_colx // TILE_SIZE] = -1                
                swap_count += 1 
                pick_sound.play()
            draw_text('X ' + str(swap_count), font_score, GREEN, SCREEN_WIDTH + 180, 390) 
            collide_hook = pygame.sprite.spritecollide(player, hook_group, True)
            if collide_hook:          
                for hook in collide_hook:
                    hook_colx = hook.rect.x
                    hook_coly = hook.rect.y
                    world_data[hook_coly // TILE_SIZE][hook_colx // TILE_SIZE] = -1
                hook_count += 1   
                pick_sound.play()
            draw_text('X ' + str(hook_count), font_score, GREEN, SCREEN_WIDTH + 180, 265)
            
            if swap_button.draw(screen) and swap_count > 0:
                select_sound.play()
                allow_swap = not allow_swap
                yet_1 = False
                yet_2 = False 
                swap_1_x = []
                swap_1_y = []
                swap_1 = []
                swap_2 = []
                swap_2_x = []
                swap_2_y = []                 
            
            if allow_swap or allow_hook:
                player_movement = False
            else:
                player_movement = True
            if allow_swap:
                pygame.draw.rect(screen, RED, swap_rect, 3) 
                
            if allow_swap:
                pos = pygame.mouse.get_pos()
                x = (pos[0]) // TILE_SIZE
                y = (pos[1]) // TILE_SIZE
                #check in area
                if pos[0] > TILE_SIZE and pos[0] < SCREEN_WIDTH - TILE_SIZE and pos[1] < SCREEN_HEIGHT - TILE_SIZE and pos[1] > TILE_SIZE and player_square(x, y) == True:
                    swap_range = True
                else:
                    swap_range = False
                        
                if yet_1 == True and yet_2 == True: 
                    for row in swap_1_y:
                        for col in swap_1_x:
                            swap_1.append(world_data[row][col])
                    count = 0
                    for row in swap_2_y:
                        for col in swap_2_x:
                            swap_2.append(world_data[row][col])
                            world_data[row][col] = swap_1[count]
                            count += 1
                    count = 0
                    for row in swap_1_y:
                        for col in swap_1_x:
                            world_data[row][col] = swap_2[count]
                            count += 1                
                    swap_count -= 1               
                    allow_swap = False
                    swamp_group.empty()
                    hook_group.empty()
                    swap_group.empty()                    
                    world = World(world_data) 
            #if using hook
            if hook_button.draw(screen) and hook_count > 0: 
                select_sound.play()
                allow_hook = not allow_hook
                
            if allow_hook and hook_count > 0:
                pygame.draw.rect(screen, RED, hook_rect, 3)
            else:
                allow_hook = False
                
                            
                
            if get_hooked_r == True:
                for tile_check in range (sprite_x_r, 13):
                    if world_data[sprite_y][tile_check] != -1 and world_data[sprite_y][tile_check] != 2 and world_data[sprite_y][tile_check] != 3 and world_data[sprite_y][tile_check] != 4:
                        if world_data[sprite_y][tile_check - 1] == 4 or world_data[sprite_y][tile_check - 1] == 3:
                            break
                        hooked_tile = world_data[sprite_y][tile_check]
                        world_data[sprite_y][tile_check] = -1
                        world_data[sprite_y][tile_check - 1] = hooked_tile
                        hook_count -= 1
                        hook_sound.play()
                        break
                get_hooked_r = False
                swamp_group.empty()
                hook_group.empty()
                swap_group.empty()                  
                world = World(world_data)
                
            elif get_hooked_l == True:
                for tile_check in range (sprite_x_l, 0, -1):
                    if world_data[sprite_y][tile_check] != -1 and world_data[sprite_y][tile_check] != 2 and world_data[sprite_y][tile_check] != 3 and world_data[sprite_y][tile_check] != 4:
                        if world_data[sprite_y][tile_check + 1] == 4 or world_data[sprite_y][tile_check + 1] == 3:
                            break                        
                        hooked_tile = world_data[sprite_y][tile_check]
                        world_data[sprite_y][tile_check] = -1
                        world_data[sprite_y][tile_check + 1] = hooked_tile
                        hook_count -= 1
                        hook_sound.play()
                        break
                get_hooked_l = False
                swamp_group.empty()
                hook_group.empty()
                swap_group.empty()                  
                world = World(world_data)                
                world = World(world_data)  
            
            elif get_hooked_u == True:
                for tile_check in range (sprite_y - 1, 0, -1):
                    if world_data[tile_check][sprite_x_c] != -1 and world_data[tile_check][sprite_x_c] != 2 and world_data[tile_check][sprite_x_c] != 3 and world_data[tile_check][sprite_x_c] != 4:
                        if world_data[tile_check + 1][sprite_x_c] == 4 or world_data[tile_check + 1][sprite_x_c] == 3:
                            break                           
                        hooked_tile = world_data[tile_check][sprite_x_c]
                        world_data[tile_check][sprite_x_c] = -1
                        world_data[tile_check + 1][sprite_x_c] = hooked_tile
                        hook_count -= 1
                        hook_sound.play()
                        break
                get_hooked_u = False
                swamp_group.empty()
                hook_group.empty()
                swap_group.empty()                  
                world = World(world_data)                
                world = World(world_data)             
            
            swap_button.draw(screen)            
        
        swamp_group.draw(screen) 
        flag_group.draw(screen)
        swap_group.draw(screen)
        hook_group.draw(screen)
        
        # Draw hitboxes for all sprites
        for sprite in swamp_group:
            pygame.draw.rect(screen, (0, 255, 0), sprite.rect, 1)  # Green for swamp
        for sprite in flag_group:
            pygame.draw.rect(screen, (0, 0, 255), sprite.rect, 1)  # Blue for flag
        for sprite in swap_group:
            pygame.draw.rect(screen, (255, 255, 0), sprite.rect, 1)  # Yellow for swap
        for sprite in hook_group:
            pygame.draw.rect(screen, (255, 0, 255), sprite.rect, 1)  # Purple for hook
        
        game_over = player.update(game_over)
        if game_over == -1:
            hook_button.draw(screen)
            swap_button.draw(screen)
            draw_text('GAME OVER!', font_level, RED, SCREEN_WIDTH // 2 - 140, SCREEN_HEIGHT // 2)  # Add game over text
            if pause_end_time > pause_start_time and pause_start_time > 0:
                start_time += (pause_end_time - pause_start_time)
                pause_start_time = 0
            counting_time = pygame.time.get_ticks() - start_time
            # change milliseconds into seconds #fix pls
            counting_minutes = math.floor(counting_time/60000)
            counting_seconds = str( (counting_time%60000)/1000 ).zfill(3)
            counting_string = "{:.0f}".format(counting_minutes)            
            if exit_button_active.draw(screen):
                click_sound.play()
                pause_start_time = pygame.time.get_ticks()
                main_menu = True
                world_data = []
                world = reset_level(level)  
                if hidden:
                    hook_count = hidden_hook_list[level-100]
                    swap_count = hidden_swap_list[level-100]     
                else:
                    hook_count = hook_list[level]
                    swap_count = swap_list[level]                       
            if restart_button_active.draw(screen):
                click_sound.play()
                world_data = []
                world = reset_level(level)
                game_over = 0   
                draw_text(f'Level: {level}', font_level, RED, SCREEN_WIDTH + 60, 25)
                if hidden:
                    hook_count = hidden_hook_list[level-100]
                    swap_count = hidden_swap_list[level-100]     
                else:
                    hook_count = hook_list[level]
                    swap_count = swap_list[level]               
                draw_text('X ' + str(swap_count), font_score, GREEN, SCREEN_WIDTH + 180, 390)
                draw_text('X ' + str(hook_count), font_score, GREEN, SCREEN_WIDTH + 180, 265)                  
            draw_text(counting_string + "m" + counting_seconds + "s", font_score, RED, SCREEN_WIDTH+75, 600)   
            draw_text(f'Level: {level}', font_level, RED, SCREEN_WIDTH + 60, 25)
            if hidden:
                    hook_count = hidden_hook_list[level-100]
                    swap_count = hidden_swap_list[level-100]     
            else:
                hook_count = hook_list[level]
                swap_count = swap_list[level]                
            draw_text('X ' + str(swap_count), font_score, GREEN, SCREEN_WIDTH + 180, 390)
            draw_text('X ' + str(hook_count), font_score, GREEN, SCREEN_WIDTH + 180, 265)
            if restart_button.draw(screen):
                click_sound.play()
                world_data = []
                world = reset_level(level)
                game_over = 0
                
        
        if game_over == 1:
        #reset game and go to next level
            if high_score:
                level += 1           
            if level <= max_levels and hidden == False:
                #reset level
                world_data = []
                world = reset_level(level)
                game_over = 0
                hook_count = hook_list[level]
                swap_count = swap_list[level]                 
            elif hidden == False:
                #draws you win background and keeps player updating
                screen.blit(win_back_img, (0, 0))
                screen.blit(trophy_img, (700, 150))
                screen.blit(trophy_img, (790, 500))
                screen.blit(trophy_img, (300, 240))
                screen.blit(trophy_img, (550, 600))
                screen.blit(trophy_img, (1000, 40))
                screen.blit(trophy_img, (50, 100))  
                screen.blit(key_img, (SCREEN_WIDTH/2, SCREEN_HEIGHT/2 - 100))
                pygame.draw.rect(screen, WHITE, highscore_rect, 1)
                game_over = player.update(game_over)
                screen.blit(broke_img, (370,115))
                    
                #if first time, write high score
                if high_score:
                    score_position = ""
                    player.reset(609, SCREEN_HEIGHT - 100)
                    score = []
                    if level >= 100:
                        try:
                            with open('score_unlocked', 'rb') as file:
                                scorelist = (pickle.load(file))
                                for i in scorelist:
                                    score.append(i)
                        except:
                            score = ["0m0.000s", "0m0.000s", "0m0.000s"]
                            
                        currentscore = counting_string + "m" + counting_seconds + "s"
                        low_highscore = re.split('m|s', score[2])
                        mid_highscore = re.split('m|s', score[1])
                        high_highscore = re.split('m|s', score[0])
                        currenttime = 60*float(counting_string) + float(counting_seconds)
                        if (currenttime > (60*(float(low_highscore[0])) + float(low_highscore[1]))) and ((60*(float(low_highscore[0])) + float(low_highscore[1])) != 0):
                            pass
                        elif (currenttime > (60*(float(mid_highscore[0])) + float(mid_highscore[1]))) and ((60*(float(mid_highscore[0])) + float(mid_highscore[1])) != 0):
                            score[2] = currentscore
                            score_position = "3"
                        elif (currenttime > (60*(float(high_highscore[0])) + float(high_highscore[1]))) and ((60*(float(high_highscore[0])) + float(high_highscore[1])) != 0):
                            score[2] = score[1]
                            score[1] = currentscore 
                            score_position = "2"
                        else:
                            score[2] = score[1]
                            score[1] = score[0]
                            score[0] = currentscore
                            score_position = "1"
                        with open('score_unlocked', 'wb') as file:
                            pickle.dump(score, file)
                        high_score = False
                    else:
                        try:
                            with open('score', 'rb') as file:
                                scorelist = (pickle.load(file))
                                for i in scorelist:
                                    score.append(i)
                        except:
                            score = ["0m0.000s", "0m0.000s", "0m0.000s"]
                            
                        currentscore = counting_string + "m" + counting_seconds + "s"
                        low_highscore = re.split('m|s', score[2])
                        mid_highscore = re.split('m|s', score[1])
                        high_highscore = re.split('m|s', score[0])
                        currenttime = 60*float(counting_string) + float(counting_seconds)
                        if (currenttime > (60*(float(low_highscore[0])) + float(low_highscore[1]))) and ((60*(float(low_highscore[0])) + float(low_highscore[1])) != 0):
                            pass
                        elif (currenttime > (60*(float(mid_highscore[0])) + float(mid_highscore[1]))) and ((60*(float(mid_highscore[0])) + float(mid_highscore[1])) != 0):
                            score[2] = currentscore
                            score_position = "3"
                        elif (currenttime > (60*(float(high_highscore[0])) + float(high_highscore[1]))) and ((60*(float(high_highscore[0])) + float(high_highscore[1])) != 0):
                            score[2] = score[1]
                            score[1] = currentscore 
                            score_position = "2"
                        else:
                            score[2] = score[1]
                            score[1] = score[0]
                            score[0] = currentscore
                            score_position = "1"
                        with open('score', 'wb') as file:
                            pickle.dump(score, file)
                        high_score = False
                draw_text("TOP TIMES", font_level, RED, 30, 250)
                draw_text("1.", font_sub, WHITE, 15, 350)
                draw_text(score[0], font_score, VIOLET, 100, 345)
                draw_text("2.", font_sub, WHITE, 15, 425)
                draw_text(score[1], font_score, VIOLET, 100, 420)
                draw_text("3.", font_sub, WHITE, 15, 500)
                draw_text(score[2], font_score, VIOLET, 100, 495)
                pygame.draw.line(screen, WHITE, (0, 550), (370, 550))
                draw_text(score_position, font_sub, RED, 15, 575)
                draw_text(currentscore, font_score, VIOLET, 100, 570)
                if exit_button_end.draw(screen):
                    click_sound.play()
                    level = 0
                    start_time = 0
                    world_data = []
                    world = reset_level(level)
                    game_over = 0
                    hook_count = hook_list[level]
                    swap_count = swap_list[level]                       
                    main_menu = True   
                    high_score = True
                    hidden = False
                if restart_button_end.draw(screen):
                    click_sound.play()
                    level = 0
                    start_time = 0
                    world_data = []
                    world = reset_level(level)
                    game_over = 0
                    high_score = True
                    hidden = False
                    hook_count = hook_list[level]
                    swap_count = swap_list[level]                  
                    
            if hidden == True:
                if level < 100:
                    level = 100
                    high_score = True
                if level <= max_hidden:
                    #reset level
                    world_data = []
                    world = reset_level(level)
                    game_over = 0
                    hook_count = hidden_hook_list[level-100]
                    swap_count = hidden_swap_list[level-100]
                else:
                    hidden = False
                
                
            
            
    

    pygame.display.update()

pygame.quit()
