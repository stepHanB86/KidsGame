import pygame, pygame.mixer, random, sys, os
from os.path import join


# general setup

pygame.init()
WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 720
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption('Oskars Welt')
running = True
clock = pygame.time.Clock()

pygame.mixer.init()
pygame.mixer.set_num_channels(32) 
background_channel = pygame.mixer.Channel(0)
pygame.mouse.set_visible(False)

game_speed = -3.0 
enemy_speed = game_speed
background_speed = game_speed


# variables for player position

player_x, player_y = 50, 300
player_speed = 0.0
score = 0

snowballs = []
snowball_speed = 2.5
last_shot_time = 0 
shoot_delay = 500 


# enemy variables

enemy_x = 1100.0
enemy_y = int(random.randint(200,600))
enemy_speed = -3.0
base_enemy_speed = -3.0 
speed_multiplier = 1.0 
last_score_adjustment = 0 
enemies = []
enemy_count = 0
spawn_delay = 4000
next_spawn_time = pygame.time.get_ticks()


# penguin variables

penguin_x = 1100.0
penguin_y = int(random.randint(200,600))
penguin_speed = game_speed
penguins = []
penguin_count = 0


# stone variables

stone_x = 1100.0
stone_y = int(random.randint(200,600))
stone_speed = game_speed
stones = []
stone_count = 0


# ramp variables

ramp_x = 1100.0
ramp_y = int(random.randint(50,150))
ramps = []
ramp_count = 0


# bird variables

bird_x = 1100.0
bird_y = int(random.randint(20,40))
bird_speed = game_speed
birds = []
bird_count = 0


# explosions variables

explosions = [] 
explosion_lifetime = 20 


# jump variables

is_jumping = False
jump_target_y = 0
jump_target_x = 0
jump_speed = 2.2
jump_returning = False
original_y = player_y 
original_x = player_x


game_over = False

# Background variables

snowbackground_surf = pygame.image.load(join('KidsGame/images', 'spiel_front.png')).convert_alpha()
background_width = snowbackground_surf.get_width()
background_x1 = 0 
background_x2 = background_width
background_speed = enemy_speed 
horizont_surf = pygame.image.load(join('KidsGame/images', 'spiel_background.png')).convert_alpha()
horizont_width = horizont_surf.get_width()
horizont_x1 = 0
horizont_x2 = background_width
horizont_speed = background_speed +2


# importing images

player_surf = pygame.image.load(join('KidsGame/images', 'player_default.png')).convert_alpha()
schlitten_surf = pygame.image.load(join('KidsGame/images', 'schlitten.png')).convert_alpha()
enemy_surf = pygame.image.load(join('KidsGame/images', 'snowman.png')).convert_alpha()
enemy_rect = enemy_surf.get_rect(topleft=(int(enemy_x), int(enemy_y)))
snowball_surf = pygame.image.load(join('KidsGame/images', 'snowball.png')).convert_alpha()
explosion_surf = pygame.image.load(join('KidsGame/images', 'explosion.png')).convert_alpha()
horizont_surf = pygame.image.load(join('KidsGame/images', 'spiel_background.png')).convert_alpha()
mountains_surf = pygame.image.load(join('KidsGame/images', 'mountains.png')).convert_alpha()
stone_surf = pygame.image.load(join('KidsGame/images', 'rock.png')).convert_alpha()
snowbackground_surf = pygame.image.load(join('KidsGame/images', 'spiel_front.png')).convert_alpha()
house_surf = pygame.image.load(join('KidsGame/images', 'house.png')).convert_alpha()
score_surf = pygame.image.load(join('KidsGame/images', 'score.png')).convert_alpha()
penguin_surf = pygame.image.load(join('KidsGame/images', 'penguin.png')).convert_alpha()
penguin_width = penguin_surf.get_width()
ramp_surf = pygame.image.load(join('KidsGame/images', 'ramp.png')).convert_alpha()
ramp_width = ramp_surf.get_width()
playerGameOver_surf = pygame.image.load(join('KidsGame/images', 'player_GameOver.png')).convert_alpha()
schlittenGameOver_surf = pygame.image.load(join('KidsGame/images', 'schlitten_GameOver.png')).convert_alpha()
bird_surf = pygame.image.load(join('KidsGame/images', 'bird.png')).convert_alpha()
bird_width = bird_surf.get_width()
bird_height = bird_surf.get_height()


# importing audio

hit_sound = pygame.mixer.Sound(join('KidsGame/sounds', 'hit_sound.wav'))
hit_sound.set_volume(0.5) 
swing_sound = pygame.mixer.Sound(join('KidsGame/sounds', 'swing_sound.wav'))
swing_sound.set_volume(0.7)
background_sound = pygame.mixer.Sound(join('KidsGame/sounds', 'spiel2.mp3'))
background_sound.set_volume(0.2)
riser_sound = pygame.mixer.Sound(join('KidsGame/sounds', 'riser.wav'))
riser_sound.set_volume(0.1) 
menu_sound = pygame.mixer.Sound(join('KidsGame/sounds', 'spiel2_menu.wav'))
menu_sound.set_volume(0.1)
autsch_sound = pygame.mixer.Sound(join('KidsGame/sounds', 'autsch.wav'))
autsch_sound.set_volume(0.4)
yeah_sound = pygame.mixer.Sound(join('KidsGame/sounds', 'yeah.wav'))
yeah_sound.set_volume(0.2)
lachen_sound = pygame.mixer.Sound(join('KidsGame/sounds', 'lachen.wav'))
lachen_sound.set_volume(0.1)

background_channel.play(background_sound, loops=-1)  # endless loop
channel = pygame.mixer.find_channel()

background_channel.play(background_sound, loops=-1)
channel = pygame.mixer.find_channel()



paused = False



# get base path

def get_base_path():
    if getattr(sys, 'frozen', False):
        return sys._MEIPASS
    return os.path.dirname(os.path.abspath(__file__))


# set path to image files

base_path = get_base_path()
image_path = os.path.join(base_path, "images", "spiel_front.png")


# spawn functions

def spawn_enemy():
    return{
    "x": WINDOW_WIDTH,
    "y": random.randint(150, 550),
    "speed": game_speed
    }

for i in range (enemy_count):
    enemies.append(spawn_enemy())

def spawn_penguin():
    return {
        "x": WINDOW_WIDTH,
        "y": random.randint(150, 550),
        "speed": game_speed
    }
for i in range (penguin_count):
    penguins.append(spawn_penguin())

def spawn_ramp():
    return{
    "x": WINDOW_WIDTH,
    "y": random.randint(20, 150),
    "speed": game_speed
    }

for i in range (ramp_count):
    ramps.append(spawn_ramp())

def spawn_stone():
    return {
        "x": WINDOW_WIDTH,
        "y": random.randint(150, 550),
        "speed": game_speed
    }
for i in range (stone_count):
    stones.append(spawn_stone())

def spawn_bird():
    return {
        "x": WINDOW_WIDTH,
        "y": random.randint(20, 40),
        "speed": game_speed
    }
for i in range (bird_count):
    birds.append(spawn_bird())


# function for pause-menu

def show_pause_menu():
    font = pygame.font.SysFont('ComicSans', 50)
    text = font.render("PAUSE", True, (0, 0, 0))
    display_surface.blit(text, (WINDOW_WIDTH // 2 - text.get_width() // 2, WINDOW_HEIGHT // 3))

    font = pygame.font.SysFont('ComicSans', 30)
    resume_text = font.render("Drücke ESC, um fortzusetzen", True, (0, 0, 0))
    display_surface.blit(resume_text, (WINDOW_WIDTH // 2 - resume_text.get_width() // 2, WINDOW_HEIGHT // 2))

    quit_text = font.render("Drücke Q, um das Spiel zu beenden", True, (0, 0, 0))
    display_surface.blit(quit_text, (WINDOW_WIDTH // 2 - quit_text.get_width() // 2, WINDOW_HEIGHT // 1.5))
    pygame.display.update()


# function for resetting the game

def reset_game():
    global player_x, player_y, score, enemies, penguins, ramps, explosions, game_over, enemy_count, spawn_delay, speed_multiplier
    player_x, player_y = 50, 300
    score = 0  
    enemies.clear()  
    penguins.clear() 
    ramps.clear() 
    explosions.clear()
    enemy_count = 0 
    spawn_delay = 4000
    speed_multiplier = 1.0 
    game_over = False 
    background_channel.play(background_sound, loops=-1)



# Game loop

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if game_over:
        # game over-screen
        font = pygame.font.SysFont('ComicSans', 80)
        game_over_text = font.render("GAME OVER", True, (255, 0, 0))
        score_text = font.render(f"Du hast {score} Punkte erreicht!", True, (0, 0, 0))
        display_surface.blit(game_over_text, (WINDOW_WIDTH // 2 - game_over_text.get_width() // 2, WINDOW_HEIGHT // 3))
        display_surface.blit(score_text, (WINDOW_WIDTH // 2 - score_text.get_width() // 2, WINDOW_HEIGHT // 2))
        font = pygame.font.SysFont('ComicSans', 30)
        restart_text = font.render("Drücke ENTER für einen Neustart oder Q um das Spiel zu verlassen", True, (0, 0, 0))
        display_surface.blit(restart_text, (WINDOW_WIDTH // 2 - restart_text.get_width() // 2, WINDOW_HEIGHT // 1.5))
        pygame.display.update()
        
        # check keys
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN]: 
            reset_game()
        elif keys[pygame.K_q]:
            running = False
        pygame.time.delay(100)
        continue
    
    
    if not paused:
        keys = pygame.key.get_pressed()
        

        if keys[pygame.K_ESCAPE]:
            paused = True
            background_channel.pause() 
         # Move background
        background_x1 += background_speed
        background_x2 += background_speed

        horizont_x1 += horizont_speed
        horizont_x2 += horizont_speed

        # Reset background positions when they move out of the screen
        
        if background_x1 <= -background_width:
            background_x1 = background_x2 + background_width
        if background_x2 <= -background_width:
            background_x2 = background_x1 + background_width

        if horizont_x1 <= -horizont_width:
            horizont_x1 = horizont_x2 + horizont_width
        if horizont_x2 <= -horizont_width:
            horizont_x2 = horizont_x1 + horizont_width

    
        # spawn enemies 
        
        current_time = pygame.time.get_ticks()
        if current_time >= next_spawn_time and len(enemies) < enemy_count:
            enemies.append(spawn_enemy())
            next_spawn_time = current_time + spawn_delay 

        
        # update game state
        
        for enemy in enemies[:]: 
            enemy["x"] += enemy_speed 
            if enemy["x"] < -enemy_surf.get_width(): 
                enemies.remove(enemy) 
                score -= 0 

        for penguin in penguins[:]:
            penguin["x"] += penguin["speed"]                                  # moves left
            if penguin["x"] < -penguin_surf.get_width():                      # when moves out of the screen
                penguins.remove(penguin)                                   
                score -= 0

        for bird in birds[:]:
            bird["x"] += bird_speed 
            if bird["x"] < -bird_surf.get_width(): 
                birds.remove(bird) 
                score -= 0 

               
        # allow jump only if no jump is active
        
        if not is_jumping:
            if keys[pygame.K_UP] and player_y > 140:
                player_y -= 3.0
            if keys[pygame.K_DOWN] and player_y < 520:
                player_y += 3.0

        # moving ramps and check collision
        
        for ramp in ramps[:]:
            ramp["x"] += background_speed
            if ramp["x"] < -ramp_surf.get_width():
                ramps.remove(ramp)

         # collision player with ramp
            
            if player_x  < ramp["x"] + ramp_width and player_x + player_surf.get_width()  - 300 > ramp["x"] and \
                player_y < ramp["y"] + ramp_surf.get_height() -350 and player_y  + player_surf.get_height() - 250 > ramp["y"]:
                if not is_jumping:  
                    is_jumping = True
                    birds.append(spawn_bird())
                    jump_target_y = player_y - 350  # jump height
                    jump_target_x = 250
                    jump_returning = False  
                    if channel:
                        riser_sound.play()
                        yeah_sound.play()
        
        # jump logic
        
        if is_jumping:
            if not jump_returning:
                player_y -= jump_speed
                player_x += jump_speed
                if player_y <= jump_target_y and player_x >= jump_target_x:  # jump height reached
                    jump_returning = True  
            else:
                # player returns
                player_y += jump_speed
                player_x -= jump_speed 
                if player_y >= original_y and player_x <= original_x:  # back to original height
                    
                    player_x = original_x
                    is_jumping = False 


        # dynamic adjustment of spawn delay and speed based on score
        
        if score > 0 and score % 10 == 0 and score != last_score_adjustment:
            spawn_delay = max(600, spawn_delay - 300) 
            speed_multiplier += 0.5  
            last_score_adjustment = score 
            

        if score > 0 and score % 4 == 0 and score != last_score_adjustment:
            penguins.append(spawn_penguin())
            last_score_adjustment = score

        if score > 0 and score % 6 == 0 and score != last_score_adjustment:
            ramps.append(spawn_ramp()) 
            last_score_adjustment = score 

        if score > 0 and score % 3 == 0 and score != last_score_adjustment:
            stones.append(spawn_stone()) 
            birds.append(spawn_bird())
            last_score_adjustment = score 

            
        # controll enemy spawn
        
        if current_time >= next_spawn_time:
            enemies.append(spawn_enemy())
            next_spawn_time = current_time + spawn_delay

        
    
        current_time = pygame.time.get_ticks() 
        if keys[pygame.K_SPACE] and current_time - last_shot_time >= shoot_delay:
            snowballs.append({"x": player_x + 10, "y": player_y + 75})
            last_shot_time = current_time  # update time of last shot
            if channel:
                swing_sound.play()
    


        # update
        
        for snowball in snowballs[:]:
            snowball["x"] += snowball_speed  # move snowball to the right
            if snowball["x"] > WINDOW_WIDTH:  # remove snowball if it leaves screen
                snowballs.remove(snowball)
        
        for stone in stones[:]:
            stone["x"] += stone_speed
            if stone["x"] < -stone_surf.get_width():
                stones.remove(stone)





        # collision snowball and enemy
        
        for snowball in snowballs[:]:
            for enemy in enemies[:]:  # check every snowball against every enemy
                if enemy["x"] < snowball["x"] < enemy["x"] + enemy_surf.get_width() and \
                    enemy["y"] - 30 < snowball["y"] < enemy["y"] + enemy_surf.get_height():
                 # add explosion
                    explosions.append({"x": enemy["x"], "y": enemy["y"], "lifetime": explosion_lifetime})
                    if channel:
                        hit_sound.play()
                    snowballs.remove(snowball)  # remove snowball
                    score += 1
                    enemies.remove(enemy)  # remove enemy after collision
                    break
 
        # collision snowball and bird
        
        for snowball in snowballs[:]:
            for bird in birds[:]:  
                if bird["x"] < snowball["x"] < bird["x"] + bird_surf.get_width() and \
                    bird["y"] < snowball["y"] < bird["y"] + bird_surf.get_height():
                 
                    explosions.append({"x": bird["x"], "y": bird["y"], "lifetime": explosion_lifetime})
                    if channel:
                        hit_sound.play()
                        lachen_sound.play()
                    snowballs.remove(snowball)  
                    score += 5
                    birds.remove(bird)  
                    break

        # collision snowball and stone
        
        for snowball in snowballs[:]:
            for stone in stones[:]:  
                if stone["x"] < snowball["x"] < stone["x"] + stone_surf.get_width() and \
                    stone["y"] < snowball["y"] < stone["y"] + stone_surf.get_height():
                    if channel:
                        hit_sound.play()
                    snowballs.remove(snowball)  
                    break

        # collision snowball and penguin
        
        for snowball in snowballs[:]:
            for penguin in penguins[:]: 
                if penguin["x"] < snowball["x"] < penguin["x"] + penguin_surf.get_width() and \
                    penguin["y"] - 30 < snowball["y"] < penguin["y"] + penguin_surf.get_height():
                    explosions.append({"x": penguin["x"], "y": penguin["y"], "lifetime": explosion_lifetime})
                    if channel:
                        hit_sound.play()
                        lachen_sound.play()
                    snowballs.remove(snowball) 
                    score += 1
                    penguins.remove(penguin) 
                    break


        for enemy in enemies:
            if player_x < enemy["x"] + enemy_surf.get_width() and \
               player_x + player_surf.get_width() > enemy["x"] and \
               player_y < enemy["y"] + enemy_surf.get_height() and \
               player_y + player_surf.get_height() > enemy["y"]:
                game_over = True
                if channel:
                    autsch_sound.play()
                background_channel.stop()
                break

        for penguin in penguins:
            if player_x < penguin["x"] + penguin_surf.get_width() and \
               player_x + player_surf.get_width() > penguin["x"] and \
               player_y < penguin["y"] + penguin_surf.get_height() and \
               player_y + player_surf.get_height() > penguin["y"]:
                game_over = True
                if channel:
                    autsch_sound.play()
                background_channel.stop()
                break
        
        for bird in birds:
            if player_x < bird["x"] + bird_surf.get_width() and \
               player_x + player_surf.get_width() > bird["x"] and \
               player_y < bird["y"] + bird_surf.get_height() and \
               player_y + player_surf.get_height() > bird["y"]:
                game_over = True
                if channel:
                    autsch_sound.play()
                background_channel.stop()
                break

        for stone in stones:
            if player_x < stone["x"] + stone_surf.get_width() and \
               player_x + player_surf.get_width() > stone["x"] and \
               player_y + 80 < stone["y"] + stone_surf.get_height() and \
               player_y + player_surf.get_height() > stone["y"]:
                game_over = True
                background_channel.stop()
                break
        
        
            

        # update explosions
        
        for explosion in explosions[:]:
            explosion["lifetime"] -= 1 
            if explosion["lifetime"] <= 0:
                explosions.remove(explosion) 
    
       
        
        # draw the game
        
        display_surface.fill('deepskyblue3')
        display_surface.blit(horizont_surf, (horizont_x1, -150))
        display_surface.blit(horizont_surf, (horizont_x2, -150))
        display_surface.blit(snowbackground_surf, (background_x1, 210)) # First background
        display_surface.blit(snowbackground_surf, (background_x2, 210)) # Second background
    
        
        for ramp in ramps:
            display_surface.blit(ramp_surf, (int(ramp["x"]), int(ramp["y"])))

        for stone in stones:
            display_surface.blit(stone_surf, (int(stone["x"]), int(stone["y"])))

        for enemy in enemies:
            display_surface.blit(enemy_surf, (int(enemy["x"]), int(enemy["y"])))

        for penguin in penguins:
            display_surface.blit(penguin_surf, (int(penguin["x"]), int(penguin["y"])))

        for bird in birds:
            display_surface.blit(bird_surf, (int(bird["x"]), int(bird["y"])))


        display_surface.blit(schlitten_surf, (int(player_x - 40), int(player_y + 80)))
        display_surface.blit(player_surf, (int(player_x), int(player_y)))

        for explosion in explosions:
            display_surface.blit(explosion_surf, (int(explosion["x"]), int(explosion["y"])))
    
        for snowball in snowballs:
            display_surface.blit(snowball_surf, (int(snowball["x"]), int(snowball["y"])))
    
        display_surface.blit(house_surf, (900, 450))

        display_surface.blit(score_surf, (960, 20))

        font = pygame.font.SysFont('ComicSans', 65)
        score_text = font.render(f"{score}", True, (0, 0, 0))
        display_surface.blit(score_text, (1090, 40))
     
        
    else:
        show_pause_menu() 

        keys = pygame.key.get_pressed()

        if keys[pygame.K_ESCAPE]: 
            paused = False
            background_channel.unpause() 
        elif keys[pygame.K_q]:
            running = False

        



    pygame.display.update()
    clock.tick(120)  
    
pygame.quit()

