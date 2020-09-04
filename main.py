# Flappy Bird game by PhilipWerz

import pygame
import random
from time import sleep
import os

# init
pygame.init()
# comment
dis_width = 370
dis_height = 550

game_speed = 35

ground_level = 490
bird_speed = 4

ground1_x = 0
ground2_x = dis_width

tube_len = 320
tube_width = 52

bird_width = 48
bird_height = 34
 
# load graphics
bg = pygame.image.load(os.path.join("Graphics", "bg.png"))
bg = pygame.transform.scale(bg, (dis_width, ground_level))
ground = pygame.image.load(os.path.join("Graphics", "ground.png"))
ground = pygame.transform.scale(ground, (dis_width, dis_height-ground_level))
bottom_tube = pygame.image.load(os.path.join("Graphics", "tube2.png"))
top_tube = pygame.image.load(os.path.join("Graphics", "tube1.png"))
bird_up = pygame.image.load(os.path.join("Graphics", "bird_up.png"))
bird_up = pygame.transform.scale(bird_up, (bird_width, bird_height))
bird_mid = pygame.image.load(os.path.join("Graphics", "bird_mid.png"))
bird_mid = pygame.transform.scale(bird_mid, (bird_width, bird_height))
bird_down = pygame.image.load(os.path.join("Graphics", "bird_down.png"))
bird_down = pygame.transform.scale(bird_down, (bird_width, bird_height))

# bird_imgs list for bird fly animation
bird_imgs = [bird_mid, bird_up, bird_mid, bird_down]

# set display width/height/title
dis = pygame.display.set_mode((dis_width, dis_height))
pygame.display.set_caption('Flappy Bird')
pygame.display.set_icon(bird_mid)

clock = pygame.time.Clock()

# fonts
font =  pygame.font.Font(os.path.join("Graphics", "FB.ttf"), 50)
font_restart =  pygame.font.Font(os.path.join("Graphics", "FB.ttf"), 23)

class Bird():
    def __init__(self, bird_x, bird_y):
        self.bird_x = bird_x
        self.bird_y = bird_y
        self.gravity = 0

    def jump(self):
        self.gravity = -10 

    def fall(self):
        self.gravity += 0.8
        self.bird_y += self.gravity

    # collision detection bird - tube - ground
    def check_collision(self, tube_list):
        for t in tube_list:
            tx = t[0].tube_x
            tOy = t[0].tube_y
            t1y = t[1].tube_y
            # top tube
            if tOy + tube_len > self.bird_y + 3:
                if tx < self.bird_x + bird_width and tx + tube_width > self.bird_x:
                    return True
            # bottom tube
            if t1y < self.bird_y + bird_height - 3:
                if tx < self.bird_x + bird_width and tx + tube_width > self.bird_x:
                    return True
            # gound
            if self.bird_y + bird_height > ground_level + 9:
                return True
        return False
                

class Tube():
    def __init__(self, tube_x, tube_y):
        self.tube_x = tube_x
        self.tube_y = tube_y
    def move(self):
        self.tube_x -= bird_speed
    def check_bound(self):
        if self.tube_x + tube_width < 0:
            return True
        return False

def get_random_tube():
    rand_height = int(random.randrange(ground_level*0.1, int(ground_level*0.65))) # original 0.6
    tube_top_y = rand_height - tube_len
    tube_bottom_y = rand_height + ground_level*0.25 # orginal 0.3
    return (tube_top_y, tube_bottom_y)

def mooving_bg():
    global ground1_x, ground2_x
    if ground1_x + dis_width < 0:
        ground1_x = dis_width
    else:
        ground1_x -= bird_speed
    if ground2_x + dis_width < 0:
        ground2_x = dis_width
    else:
        ground2_x -= bird_speed
    dis.blit(ground, (ground1_x, ground_level))
    dis.blit(ground, (ground2_x, ground_level))

def score_message(score):
    mesg = font.render(str(score), True, [255, 255, 255])
    dis.blit(mesg, (dis_width*0.4, dis_height*0.2))

def restart_message():
    mesg = font_restart.render("Press Q-Quit or P-Play Again", True, [255, 255, 255])
    mesg_size = mesg.get_rect()
    dis.blit(mesg, (dis_width/2 - mesg_size.width/2, dis_height*0.8))

def game_over_screen(bird, bird_change):
    dis.blit(bg, (0,0))
    mesg = font.render("GAME OVER", True, [255, 255, 255])
    mesg_size = mesg.get_rect()
    dis.blit(mesg, (dis_width/2 - mesg_size.width/2, dis_height*0.25))
    restart_message()
    dis.blit(bird_imgs[bird_change], (dis_width*0.35, ground_level/2))
    mooving_bg()
    pygame.display.update()

def draw_screen(bird, tube_list, bird_change, score):
    dis.blit(bg, (0,0))
    dis.blit(bird_imgs[bird_change], (bird.bird_x, bird.bird_y))
    for t in tube_list:
        dis.blit(top_tube, (t[0].tube_x, t[0].tube_y))
        dis.blit(bottom_tube, (t[1].tube_x, t[1].tube_y))
    score_message(score)
    mooving_bg()
    
    pygame.display.update()

def start_screen():
    start = False
    while not start:
        dis.blit(bg, (0,0))
        mooving_bg()
        mesg = font.render("FLAPPY BIRD", True, [255, 255, 255])
        mesg_size = mesg.get_rect()
        dis.blit(mesg, (dis_width/2 - mesg_size.width/2, dis_height*0.25))
        mesg = font_restart.render("Press SPACE to start", True, [255, 255, 255])
        mesg_size = mesg.get_rect()
        dis.blit(mesg, (dis_width/2 - mesg_size.width/2, dis_height*0.8))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    start = True
        clock.tick(35)
        pygame.display.update()

def gameLoop():
    game_over = False
    game_close = False

    tube_list = []
    rand_heights = get_random_tube()

    tube_list.append([Tube(dis_width, rand_heights[0]), Tube(dis_width, rand_heights[1])])

    bird_x = dis_width*0.35
    bird_y = ground_level/2

    bird = Bird(bird_x, bird_y)

    score = 0
    score_tubes = []
    score_tubes.append(Tube(dis_width, rand_heights[0]))

    NEWTUBE = pygame.USEREVENT+1
    pygame.time.set_timer(NEWTUBE, 1500)
    BIRDCHANGE = pygame.USEREVENT+2
    pygame.time.set_timer(BIRDCHANGE, 120)
    bird_change = 0

    while not game_over:
        draw_screen(bird, tube_list, bird_change, score)
        bird.fall()

        while game_close:
            game_over_screen(bird, bird_change)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_over = True
                    game_close = False
                if event.type == BIRDCHANGE:
                    if bird_change < 3:
                        bird_change += 1
                    else:
                        bird_change = 0
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        gameLoop()
                    if event.key == pygame.K_q:
                        game_close = False
                        game_over = True

            clock.tick(game_speed)

        if bird.check_collision(tube_list):
            sleep(0.25)
            game_close = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == BIRDCHANGE:
                if bird_change < 3:
                    bird_change += 1
                else:
                    bird_change = 0
            if event.type == NEWTUBE:
                rand_heights = get_random_tube()
                tube_list.append([Tube(dis_width, rand_heights[0]), Tube(dis_width, rand_heights[1])])
                score_tubes.append(Tube(dis_width, rand_heights[0]))
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bird.jump()
            if event.type == pygame.MOUSEBUTTONDOWN:
                bird.jump()
        
        for t in score_tubes:
            if bird.bird_x > t.tube_x + tube_width:
                score += 1
                score_tubes.remove(t)
            else:
                t.move()

        for t in tube_list:
            if t[0].check_bound() or t[1].check_bound():
                tube_list.remove(t)
            else:
                t[0].move()
                t[1].move()
        
        clock.tick(game_speed)
    
    pygame.quit()
    quit()

start_screen()
gameLoop()