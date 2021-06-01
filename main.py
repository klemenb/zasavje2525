import pygame, sys, os


clock = pygame.time.Clock()

from pygame.locals import *
from pygame import mixer

pygame.init()  # initiates pygame

pygame.display.set_caption('ZASAVJE 2525')

WINDOW_SIZE = (1400, 800)

screen = pygame.display.set_mode(WINDOW_SIZE, 0, 32)  # initiate the window

display = pygame.Surface((500, 250))  # used as the surface for rendering, which is scaled

moving_right = False
moving_left = False
main_menu = True
vertical_momentum = 0
air_timer = 0
true_scroll = [0, 0]

#GAME OVER text
over_font = pygame.font.Font("freesansbold.ttf", 64)
respawn_font = pygame.font. Font("freesansbold.ttf", 25)

#win text
win_font = pygame.font.Font("freesansbold.ttf", 90)

#virustext
virus_font = pygame.font.Font("freesansbold.ttf", 36)

#za prikazovanje scora
score_value = 0
font = pygame.font.Font("freesansbold.ttf", 36)
font_lose = pygame.font.Font("freesansbold.ttf", 56)
textX = 30
testY = 30


#definicija za prikaz START slike
def start():
    if player_rect.x == 325:
        screen.blit(start_img, (430, 208))

#definicija za game over text
def game_over_text():
    if player_rect.y > 409:
        over_text = over_font.render("GAME OVER", True, (255, 0, 0))
        respawn_text = respawn_font.render("Click BACKSPACE to RESPAWN", True, (0, 0, 0))
        screen.blit(over_text, (300, 250))
        screen.blit(respawn_text, (300, 350))

#text za avoid viruses
def virus_text():
    if player_rect.x >= 11700 and player_rect.x <11850:
        virus_text = virus_font.render("Avoid purple viruses", True, (0, 0, 0))
        screen.blit(virus_text, (530, 80))


#definicija za win text
def win_text():
    if player_rect.x > 17880:
        if score_value > 285:
            win_text = win_font.render("YOU WIN", True, (0, 0, 0))
            screen.blit(win_text, (350, 250))
        else:
            lose_text = font_lose.render("Not enough score!", True, (0, 0, 0))
            screen.blit(lose_text, (320, 250))

#definicija za score
def show_score(x, y):
    score = font.render("Score: " + str(score_value),True, (0, 0, 0))
    screen.blit(score, (x, y))


#definicija za branje mape iz datoteke
def load_map(path):
    f = open(path + '.txt', 'r')
    data = f.read()
    f.close()
    data = data.split('\n')
    game_map = []
    for row in data:
        game_map.append(list(row))
    return game_map

#level 1 text
def level1text():
    if player_rect.x >= 550 and player_rect.x <650:
        screen.blit(level1_img, (580, 120))

#level 2 text
def level2text():
    if player_rect.x >= 5000 and player_rect.x <5150:
        screen.blit(level2_img, (580, 120))

#level 3 text
def level3text():
    if player_rect.x >= 7050 and player_rect.x <7200:
        screen.blit(level3_img, (580, 120))

#level 4 text
def level4text():
    if player_rect.x >= 11700 and player_rect.x <11850:
        screen.blit(level4_img, (580, 120))

#level 5 text
def level5text():
    if player_rect.x >= 14650 and player_rect.x <14800:
        screen.blit(level5_img, (580, 120))
        screen.blit(level5_img, (580, 120))



global animation_frames
animation_frames = {}

#definicija za animacije
def load_animation(path, frame_durations):
    global animation_frames
    animation_name = path.split('/')[-1]
    animation_frame_data = []
    n = 0
    for frame in frame_durations:
        animation_frame_id = animation_name + '_' + str(n)
        img_loc = path + '/' + animation_frame_id + '.png'
        # player_animations/idle/idle_0.png
        animation_image = pygame.image.load(img_loc)
        animation_frames[animation_frame_id] = animation_image.copy()
        for i in range(frame):
            animation_frame_data.append(animation_frame_id)
        n += 1
    return animation_frame_data


def change_action(action_var, frame, new_value):
    if action_var != new_value:
        action_var = new_value
        frame = 0
    return action_var, frame



animation_database = {}

#vstavljanje SLIK in pa map za animacije
animation_database['run'] = load_animation('player_animations/run', [7, 7])
animation_database['idle'] = load_animation('player_animations/idle', [7, 7])

game_map = load_map('map')

start_img = pygame.image.load('start_btn.png')
grass_img = pygame.image.load('dirt_grass.png')
dirt_img = pygame.image.load('dirt.png')
rock_img = pygame.image.load('rock_Tiled_BG.png')
rockGrass_img = pygame.image.load('Rock_Grass.png')
metalGrass_img = pygame.image.load('Metal_Grass.png')
metal_img = pygame.image.load('Metal_Tiled_BG.png')
spikes_img = pygame.image.load('spikes.png')
rock_deco_big_img = pygame.image.load('Rock_Deco_Big.png')
rock_deco_pair_img = pygame.image.load('Rock_Deco_Pair.png')
rock_deco_small_img = pygame.image.load('Rock_Deco_Small.png')
virus_1_img = pygame.image.load('Grass_Virus.png')
virus_2_img = pygame.image.load('Future_Virus.png')
znakHR = pygame.image.load('znak_HR.png')
znakZC = pygame.image.load('znak_ZC.png')
znakTRB = pygame.image.load('znak_TRB.png')
level1_img = pygame.image.load('level1.png')
level2_img = pygame.image.load('level2.png')
level3_img = pygame.image.load('level3.png')
level4_img = pygame.image.load('level4.png')
level5_img = pygame.image.load('level5.png')

player_action = 'idle'
player_frame = 0
player_flip = False

#LOKACIJA spawna playerja
player_rect = pygame.Rect(325, 350, 30, 32)


#STOLPNICE V OZADJU(barva,[X-os,Y-os,širina,dolžina])
background_objects = [[0.5, [200, 50, 66, 400]], [0.5, [600, 150, 80, 300]], [0.5, [1000, 80, 50, 400]], [0.5, [1050, 150, 200, 250]], [0.5, [1700, 80, 120, 400]], [0.5, [2100, 120, 70, 400]], [0.5, [2700, 200, 150, 500]]]

#tile da v hit list
def collision_test(rect, tiles):
    hit_list = []
    for tile in tiles:
        if rect.colliderect(tile):
            hit_list.append(tile)
    return hit_list

#collsion s tile
def move(rect, movement, tiles):
    collision_types = {'top': False, 'bottom': False, 'right': False, 'left': False}
    rect.x += movement[0]
    hit_list = collision_test(rect, tiles)
    for tile in hit_list:
        if movement[0] > 0:
            rect.right = tile.left
            collision_types['right'] = True
        elif movement[0] < 0:
            rect.left = tile.right
            collision_types['left'] = True
    rect.y += movement[1]
    hit_list = collision_test(rect, tiles)
    for tile in hit_list:
        if movement[1] > 0:
            rect.bottom = tile.top
            collision_types['bottom'] = True
        elif movement[1] < 0:
            rect.top = tile.bottom
            collision_types['top'] = True
    return rect, collision_types


# single rock
rocks_1 = [[1060,288],[1952,352],[2450,288],[4604,320],[4710,256]]

# rock pair
rocks_2 = [[684,288],[2400,288],[3490,192]]

# virus 1 list
viruses1 = [[5350,45],[5760,288],[6652,32],[6716,-20],[7750,250],[8380,260],[9282,288],[10500,-10],[11276,20],[12888,190],[13504,160],[14402,352],[14500,100],[15170,30],[16468,160]]

# virus 2 list
viruses2 = [[12470,380],[12784,230],[14108,140],[15234,192],[16180,220],[16668,224],[15540,192],[15734,192],[17200,190],[17675,224]]

# music
mixer.init()
mixer.music.load('music.wav')
mixer.music.set_volume(0.2)
mixer.music.play(-1)

running = True
while running:  # game loop


    display.fill((146, 244, 255))  # ozadje modro

    #premikanje slike
    true_scroll[0] += (player_rect.x - true_scroll[0] - 100) / 20
    true_scroll[1] += (player_rect.y - true_scroll[1] - 106) / 20
    scroll = true_scroll.copy()
    scroll[0] = int(scroll[0])
    scroll[1] = int(scroll[1])

    #kvadrati ozadja
    for background_object in background_objects:
        obj_rect = pygame.Rect(background_object[1][0] - scroll[0] * background_object[0],
                               background_object[1][1] - scroll[1] * background_object[0], background_object[1][2],
                               background_object[1][3])
        if background_object[0] == 0.5:
            pygame.draw.rect(display, (65, 55, 51), obj_rect) #rjava svetla
        else:
            pygame.draw.rect(display, (152, 251, 152), obj_rect) #svetlo zelena

    tile_rects = []
    y = 0


    # rock 1 pickup
    for rock in rocks_1:
        display.blit(rock_deco_big_img, (rock[0] - scroll[0],rock[1] - scroll[1]))
        rock_rect = pygame.Rect(rock[0], rock[1], 32, 32)
        if player_rect.x >= rock_rect[0] -30 and player_rect.x <= rock_rect[0] +30 and player_rect.y >= rock_rect[1] - 30 and player_rect.y <= rock_rect[1] + 30:
            rocks_1.remove(rock)
            score_value += 10
            pickupSound = pygame.mixer.Sound("pickup.wav")
            pickupSound.play()


    # rock 2 pickup
    for rock in rocks_2:
        display.blit(rock_deco_pair_img, (rock[0] - scroll[0], rock[1] - scroll[1]))
        rock_rect = pygame.Rect(rock[0], rock[1], 32, 32)
        if player_rect.x >= rock_rect[0] - 30 and player_rect.x <= rock_rect[0] + 30 and player_rect.y >= rock_rect[
            1] - 30 and player_rect.y <= rock_rect[1] + 30:
            rocks_2.remove(rock)
            score_value += 10
            pickupSound = pygame.mixer.Sound("pickup.wav")
            pickupSound.play()

    # virus 1 pickup
    for virus in viruses1:
        display.blit(virus_1_img, (virus[0] - scroll[0], virus[1] - scroll[1]))
        virus_rect = pygame.Rect(virus[0], virus[1], 32, 32)
        if player_rect.x >= virus_rect[0] - 30 and player_rect.x <= virus_rect[0] + 30 and player_rect.y >= virus_rect[
            1] - 30 and player_rect.y <= virus_rect[1] + 30:
            viruses1.remove(virus)
            score_value += 15
            pickupSound = pygame.mixer.Sound("pickup.wav")
            pickupSound.play()

    # virus 2 pickup
    for virus in viruses2:
        display.blit(virus_2_img, (virus[0] - scroll[0], virus[1] - scroll[1]))
        virus_rect = pygame.Rect(virus[0], virus[1], 32, 32)
        if player_rect.x >= virus_rect[0] - 30 and player_rect.x <= virus_rect[0] + 30 and player_rect.y >= virus_rect[
            1] - 30 and player_rect.y <= virus_rect[1] + 30:
            if player_rect.x >= 11700 and player_rect.x < 14650:
                player_rect = pygame.Rect(11700, 260, 30, 32)
            if player_rect.x >= 14650 and player_rect.x < 17884:
                player_rect = pygame.Rect(14650, 190, 30, 32)
            deathSound = pygame.mixer.Sound("death.wav")
            deathSound.play()

    #KOCKE za sestavljanje mape in njihove SPAWN kode
    for layer in game_map:
        x = 0
        for tile in layer:
            if tile == '1':
                display.blit(dirt_img, (x * 32 - scroll[0], y * 32 - scroll[1]))
            if tile == '2':
                display.blit(grass_img, (x * 32 - scroll[0], y * 32 - scroll[1]))
            if tile == '3':
                display.blit(rock_img, (x * 32 - scroll[0], y * 32 - scroll[1]))
            if tile == '4':
                display.blit(rockGrass_img, (x * 32 - scroll[0], y * 32 - scroll[1]))
            if tile == '5':
                display.blit(metalGrass_img, (x * 32 - scroll[0], y * 32 - scroll[1]))
            if tile == '6':
                display.blit(metal_img, (x * 32 - scroll[0], y * 32 - scroll[1]))
            if tile == '7':
                display.blit(spikes_img, (x * 32 - scroll[0], y * 32 - scroll[1]))
            if tile == '8':
                display.blit(znakTRB, (x * 32 - scroll[0], y * 32 - scroll[1]))
            if tile == '9':
                display.blit(znakZC, (x * 32 - scroll[0], y * 32 - scroll[1]))
            if tile == 'A':
                display.blit(znakHR, (x * 32 - scroll[0], y * 32 - scroll[1]))
            if tile != '0' and tile != 'A' and tile != '9' and tile != '8':
                tile_rects.append(pygame.Rect(x * 32, y * 32, 32, 32))
            x += 1
        y += 1

    #premikanje playerja
    player_movement = [0, 0]
    if moving_right == True:
        player_movement[0] += 2
    if moving_left == True:
        player_movement[0] -= 2
    player_movement[1] += vertical_momentum
    vertical_momentum += 0.2
    if vertical_momentum > 3:
        vertical_momentum = 3

    if player_movement[0] == 0:
        player_action, player_frame = change_action(player_action, player_frame, 'idle')
    if player_movement[0] > 0:
        player_flip = False
        player_action, player_frame = change_action(player_action, player_frame, 'run')
    if player_movement[0] < 0:
        player_flip = True
        player_action, player_frame = change_action(player_action, player_frame, 'run')

    player_rect, collisions = move(player_rect, player_movement, tile_rects)

    #da ne pade dol
    if collisions['bottom'] == True:
        air_timer = 0
        vertical_momentum = 0
    else:
        air_timer += 1

    #loading animacije
    player_frame += 1
    if player_frame >= len(animation_database[player_action]):
        player_frame = 0
    player_img_id = animation_database[player_action][player_frame]
    player_img = animation_frames[player_img_id]
    display.blit(pygame.transform.flip(player_img, player_flip, False),
                 (player_rect.x - scroll[0], player_rect.y - scroll[1]))

    #bloka playerja na lokacijo
    if player_rect.x < 325:
        player_rect.x = 326
    if player_rect.y > 410:
        player_rect.y = 410
    if player_rect.x > 17884:
        player_rect.x = 17884

#TIPKE s katerimi se prekimako
    for event in pygame.event.get():  # event loop
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
           if not game_over_text():
                button_press_time = pygame.time.get_ticks()
                if event.key == K_SPACE:
                    player_rect.x += 1
                if player_rect.x > 325:
                    if event.key == K_RIGHT:
                        moving_right = True
                    if event.key == K_LEFT:
                        moving_left = True
                    if event.key == K_UP:
                        if air_timer < 6:
                            jumpSound = pygame.mixer.Sound("jump.wav")
                            jumpSound.play()
                            vertical_momentum = -5
                            # pygame.mixer.Sound.play(jump_sound)
        if event.type == KEYUP:
            if event.key == K_RIGHT:
                moving_right = False
            if event.key == K_LEFT:
                moving_left = False

    # game over
    if player_rect.y > 409:
        if event.key == K_BACKSPACE:
            deathSound = pygame.mixer.Sound("death.wav")
            deathSound.play()
            if player_rect.x >=325 and player_rect.x <5000 :
                player_rect = pygame.Rect(325, 260, 30, 32)
            if player_rect.x >=5000 and player_rect.x <7050 :
                player_rect = pygame.Rect(5050, 260, 30, 32)
            if player_rect.x >=7050 and player_rect.x <11700 :
                player_rect = pygame.Rect(7050, 260, 30, 32)
            if player_rect.x >=11700 and player_rect.x <14650 :
                player_rect = pygame.Rect(11750, 260, 30, 32)
            if player_rect.x >=14650 and player_rect.x <17884 :
                player_rect = pygame.Rect(14650, 190, 30, 32)
        moving_right = False
        moving_left = False
        vertical_momentum = 5

    screen.blit(pygame.transform.scale(display, WINDOW_SIZE), (0, 0))
    level1text()
    level2text()
    level3text()
    level4text()
    level5text()
    virus_text()
    game_over_text()
    start()
    win_text()
    show_score(textX, testY)
    pygame.display.update()
    clock.tick(60)
