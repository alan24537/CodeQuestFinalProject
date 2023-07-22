"""
2D Dungeon Crawler
"""

from pygame import *
from math import *
from random import *

init()

width, height = 800, 600
screen = display.set_mode((width, height))

# Colors

RED = (255, 0, 0)
GREY = (127, 127, 127)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)

running = True
myClock = time.Clock()


# Player Constants
UP = 0
DOWN = 1
LEFT = 2
RIGHT = 3
PLAYER_SPEED = 5
BULLET_COOLDOWN = 30
BULLET_SPEED = 10

game_state = "menu"

background = Surface((width, height))

# Floor Loading
floor_pictures = []
for i in range(1, 4):
    temp_image = image.load("pictures/floor_" + str(i) + ".png")
    temp_scaled_image = transform.scale(temp_image, (temp_image.get_width() * 2, temp_image.get_height() * 2))
    floor_pictures.append(temp_scaled_image)
for i in range(height // floor_pictures[0].get_height() + 1):
    for j in range(width // floor_pictures[0].get_width() + 1):
        background.blit(choice(floor_pictures), (j * floor_pictures[0].get_width(), i * floor_pictures[0].get_height()))
            
# Font Loading
title_font = font.SysFont("Source Code Pro", 100)
button_font = font.SysFont("Source Code Pro", 40)
score_font = font.SysFont("Source Code Pro", 48)
        
# UI Pictures
empty_heart = transform.scale(image.load("pictures/heart_empty.png"), (32, 32))
full_heart = transform.scale(image.load("pictures/heart_full.png"), (32, 32))

# Player Pictures
player_idle_anims = []
player_run_anims = []
for i in range(4):
    temp_image = image.load("pictures\knight_idle_anim_f" + str(i) + ".png")
    temp_scaled_image = transform.scale(temp_image, (temp_image.get_width() * 3, temp_image.get_height() * 3))
    player_idle_anims.append(temp_scaled_image)
    
    temp_image = image.load("pictures\knight_run_anim_f" + str(i) + ".png")
    temp_scaled_image = transform.scale(temp_image, (temp_image.get_width() * 3, temp_image.get_height() * 3))
    player_run_anims.append(temp_scaled_image)
player_idle_index = 0
player_run_index = 0

arrow_image = image.load("pictures/weapon_arrow.png")
arrow_list = [arrow_image, arrow_image, arrow_image, arrow_image]
arrow_list[DOWN] = transform.rotate(arrow_image, 180)
arrow_list[RIGHT] = transform.rotate(arrow_image, 90)
arrow_list[LEFT] = transform.rotate(arrow_image, 270)


# Player Variables
player_rect = Rect(500, 500, player_idle_anims[0].get_width(), player_idle_anims[0].get_height())
player_dir = UP
player_lives = 3
player_score = 0

player_bullets = []
player_attack_cooldown = 0


# Enemy Pictures
enemy_run_anims = []
for i in range(6):
    temp_image = image.load("pictures\slime_run_anim_f" + str(i) + ".png")
    temp_scaled_image = transform.scale(temp_image, (temp_image.get_width() * 3, temp_image.get_height() * 3))
    enemy_run_anims.append(temp_scaled_image)
enemy_run_index = 0

# Enemy Variables
enemy_rects = []
enemy_spawn_cooldown = 120
enemy_speed = 5


while running:
    for evt in event.get():
        if evt.type == QUIT:
            running = False
                       
    mx, my = mouse.get_pos()
    mb = mouse.get_pressed()
    keys = key.get_pressed()
    
    # Player Movement
    if keys[K_a]:
        player_rect.x = max(player_rect.x - PLAYER_SPEED, 0)
        player_dir = LEFT
    if keys[K_d]:
        player_rect.x = min(player_rect.x + PLAYER_SPEED, width - player_rect.width)
        player_dir = RIGHT
    if keys[K_w]:
        player_rect.y = max(player_rect.y - PLAYER_SPEED, 0)
        player_dir = UP
    if keys[K_s]:
        player_rect.y = min(player_rect.y + PLAYER_SPEED, height - player_rect.height)
        player_dir = DOWN
        
        
    # Player Attacking
    player_attack_cooldown = max(player_attack_cooldown - 1, 0)
    
    if keys[K_SPACE] and player_attack_cooldown == 0:
        player_bullets.append([Rect(player_rect.x + (player_rect.width // 2), player_rect.y + (player_rect.width // 2), arrow_list[player_dir].get_width(), arrow_list[player_dir].get_height()), 
                              player_dir])
        player_attack_cooldown = BULLET_COOLDOWN
    
    for bullet in player_bullets:
        if bullet[1] == UP: 
            bullet[0].y -= BULLET_SPEED
        elif bullet[1] == DOWN:
            bullet[0].y += BULLET_SPEED
        elif bullet[1] == LEFT:
            bullet[0].x -= BULLET_SPEED
        elif bullet[1] == RIGHT:
            bullet[0].x += BULLET_SPEED

        if bullet[0].x < 0 or bullet[0].x > width or bullet[0].y < 0 or bullet[0].y > height:
            player_bullets.remove(bullet)
            
        for enemy in enemy_rects:
            if bullet[0].colliderect(enemy):
                player_bullets.remove(bullet)
                enemy_rects.remove(enemy)
                player_score += 100
    
    # Enemy Movement
    enemy_spawn_cooldown = max(enemy_spawn_cooldown - 1, 0)
    
    if enemy_spawn_cooldown == 0:
        while True:
            randx = randint(0, width - 50)
            randy = randint(0, height - 50)
            
            if dist((player_rect.x, player_rect.y), (randx, randy)) > 500 and not Rect(randx, randy, 50, 50).colliderect(player_rect):
                enemy_rects.append(Rect(randx, randy, 50, 50))
                break
        enemy_spawn_cooldown = 120
        enemy_speed += 0.1
        
    for enemy in enemy_rects:
        if enemy.x < player_rect.x:
            enemy.x += enemy_speed
        elif enemy.x > player_rect.x:
            enemy.x -= enemy_speed
            
        if enemy.y < player_rect.y:
            enemy.y += enemy_speed
        elif enemy.y > player_rect.y:
            enemy.y -= enemy_speed
            
        if enemy.colliderect(player_rect):
            enemy_rects.remove(enemy)
            player_lives -= 1
            if player_lives == 0:
                game_state = "game_over"
    
    # Drawing
    screen.blit(background, (0,0))
    if game_state == "menu":
        title_text = title_font.render("2D Dungeon Crawler", True, WHITE)
        start_text = button_font.render("Click here to start", True, WHITE)
        
        screen.blit(title_text, (width // 2 - title_text.get_width() // 2, height // 2 - title_text.get_height() // 2 - 50))
        screen.blit(start_text, (width // 2 - start_text.get_width() // 2, height // 2 - start_text.get_height() // 2 + 50))
        
        button_rect = start_text.get_rect()
        button_rect.center = (width // 2, height // 2 + 50)
        
        if mb[0] and button_rect.collidepoint(mx, my):
            game_state = "game"
    elif game_state == "game":
        if player_lives == 3:
            screen.blit(full_heart, (10, 10))
            screen.blit(full_heart, (52, 10))
            screen.blit(full_heart, (94, 10))
        elif player_lives == 2:
            screen.blit(empty_heart, (10, 10))
            screen.blit(full_heart, (52, 10))
            screen.blit(full_heart, (94, 10))
        elif player_lives == 1:
            screen.blit(empty_heart, (10, 10))
            screen.blit(empty_heart, (52, 10))
            screen.blit(full_heart, (94, 10))
            
        score_text = score_font.render("Score: " + str(player_score), True, WHITE)
        screen.blit(score_text, (136, 10))
        
        if (keys[K_w] or keys[K_s] or keys[K_a] or keys[K_d]):
            if player_dir != LEFT:
                screen.blit(player_run_anims[int(player_run_index)], (player_rect.x, player_rect.y))
            else:
                screen.blit(transform.flip(player_run_anims[int(player_run_index)], True, False), (player_rect.x, player_rect.y))
            player_run_index = (player_run_index + 0.25) % len(player_run_anims)
        else:
            if player_dir != LEFT:
                screen.blit(player_idle_anims[int(player_idle_index)], (player_rect.x, player_rect.y))
            else:
                screen.blit(transform.flip(player_idle_anims[int(player_idle_index)], True, False), (player_rect.x, player_rect.y))
            player_idle_index = (player_idle_index + 0.25) % len(player_idle_anims)
        
        for enemy in enemy_rects:
            screen.blit(enemy_run_anims[int(enemy_run_index)], (enemy.x, enemy.y))
            enemy_run_index = (enemy_run_index + 0.25) % len(enemy_run_anims)
        for bullet in player_bullets:
            screen.blit(arrow_list[bullet[1]], (bullet[0].x, bullet[0].y))
    elif game_state == "game_over":
        title_text = title_font.render("Game Over", True, WHITE)
        score_text = score_font.render("Score: " + str(player_score), True, WHITE)
        start_text = button_font.render("Click here to try again", True, WHITE)
        
        screen.blit(title_text, (width // 2 - title_text.get_width() // 2, height // 2 - title_text.get_height() // 2 - 50))
        screen.blit(score_text, (width // 2 - score_text.get_width() // 2, height // 2 - score_text.get_height() // 2 + 10))
        screen.blit(start_text, (width // 2 - start_text.get_width() // 2, height // 2 - start_text.get_height() // 2 + 50))
        
        button_rect = start_text.get_rect()
        button_rect.center = (width // 2, height // 2 + 50)
        
        if mb[0] and button_rect.collidepoint(mx, my):
            player_lives = 3
            player_score = 0
            enemy_speed = 5
            game_state = "game"
        
   
    display.flip()
    myClock.tick(60)
            
quit()
