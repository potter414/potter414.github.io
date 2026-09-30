import pygame
import asyncio
import random
from constants import WIDTH, HEIGHT, JUMP_POWER, GRAVITY, FLOOR
import objects

# Initialze Pygame
pygame.init()

# Game Parameters
running = True
game_started = False
score = 0
scored = False
game_over = False
on_floor = False
mute = "False"
pygame.display.set_caption("Flappy Bird")

# SFXs
wing_sound = pygame.mixer.Sound("sounds/wing.ogg")
hit_sound = pygame.mixer.Sound("sounds/hit.ogg")
point_sound = pygame.mixer.Sound("sounds/point.ogg")
die_sounds = pygame.mixer.Sound("sounds/die.ogg")
swooshing_sound = pygame.mixer.Sound("sounds/swooshing.ogg")

# Center Window
window = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# Bird Actor
bird = objects.Bird()

# Grass Actor
grass = objects.Grass()

# Create Sprite Group
game_sprites = pygame.sprite.Group()
pipe_sprites = pygame.sprite.Group()
game_sprites.add(bird)
game_sprites.add(grass)

pipe_speed = 0
extra_pipe_speed = 0
h_extra_pipe_speed = 5
jump_extra_pipe_speed = 0

# Text Properties
game_over_text_Y = HEIGHT//2 - 250
game_over_alpha = 0
game_over_score_alpha = 0

score_text_y = HEIGHT - 270
score_alpha = 0

close_text_y = -100
close_alpha = 0

restart_text_y = HEIGHT - 190
restart_alpha = 0

green_pipe_speed = 10
red_pipe_speed = 15

# Spawn in Pipes
def spawn_pipes():
    # Set global variables
    global top_pipe, bot_pipe, pipe_speed, rng

    rng = random.randint(1, 2)
    if rng == 1:
        # Pipe actors
        top_pipe = objects.GreenTopPipe()
        bot_pipe = objects.GreenBotPipe()
        pipe_speed = green_pipe_speed
    else: 
        # Pipe actors
        top_pipe = objects.RedTopPipe()
        bot_pipe = objects.RedBotPipe()
        pipe_speed = red_pipe_speed
    pipe_sprites.add(top_pipe)
    pipe_sprites.add(bot_pipe)

spawn_pipes()
top_pipe.rect.centerx, bot_pipe.rect.centerx = WIDTH-100, WIDTH-100

def draw_screen():
    window.fill("deepskyblue")
    pipe_sprites.draw(window)
    game_sprites.draw(window)

def coming_soon():

    image = pygame.image.load("images/comingsoon.png")
    window.blit(image, (120, 0))

def show_opening_text():
    font1 = pygame.font.Font("fonts/bird.ttf", 70)
    font2 = pygame.font.Font("fonts/bird.ttf", 48)
    font3 = pygame.font.Font("fonts/bird.ttf", 70)
    text1 = font1.render("Added Speed Wheen Jumped = " + str(round(jump_extra_pipe_speed, 1)), True, "white")
    text2 = font2.render("While playing the game press h to manually add speed", True, "white")
    text3 = font3.render("Mute =" + str(mute), True, "white")
    window.blit(text1, (WIDTH//2 - 400, HEIGHT//2 - 250))
    window.blit(text2, (WIDTH//2 - 450, HEIGHT//2 - 180))
    window.blit(text3, (WIDTH//2 - 130, HEIGHT//2 - 320))

def draw_score_speed_and_mute():
    font1 = pygame.font.Font("fonts/bird.ttf", 120)
    font2 = pygame.font.Font("fonts/bird.ttf", 30)
    font3 = pygame.font.Font("fonts/bird.ttf", 30)
    text1 = font1.render(str(score), True, "white")
    text2 = font2.render("EXTRA SPEED = " + str(round(extra_pipe_speed, 1)), True, "white")
    text3 = font3.render("MUTE =" + str(mute), True, "white")
    window.blit(text1, (WIDTH//2, 50))
    window.blit(text2, (30, 10))
    window.blit(text3, (690, 10))

def draw_game_over_text():
    font1 = pygame.font.Font("fonts/bird.ttf", 153)
    font2 = pygame.font.Font("fonts/bird.ttf", 149)
    font3 = pygame.font.Font("fonts/bird.ttf", 99)
    text1 = font1.render("GAME OVER", True, "white")
    text2 = font2.render("GAME OVER", True, "orange")
    text3 = font3.render("SCORE: " + str(score), True, "white")
    text4 = font3.render("PRESS R TO RESTART", True, "white")
    window.blit(text1, (WIDTH//2 - 230, game_over_text_Y))
    window.blit(text2, (WIDTH//2 - 225, game_over_text_Y))
    window.blit(text3, (WIDTH//2 - 100, score_text_y))
    window.blit(text4, (WIDTH//2 - 300, restart_text_y))

def top_bot_move():
    top_pipe.rect.x += 1 + extra_pipe_speed
    bot_pipe.rect.x += 1 + extra_pipe_speed

def initialize_game():
    global game_over, score, game_started, on_floor, extra_pipe_speed, rng, animation_speed, jump_extra_pipe_speed, pipe_speed, green_pipe_speed, red_pipe_speed,game_over_text_Y,game_over_alpha, score_alpha, score_text_y, game_over_score_alpha, close_alpha, close_text_y, restart_alpha, restart_text_y, scored

    jump_extra_pipe_speed = 0
    extra_pipe_speed = 0
    score = 0
    scored = False
    game_over = False
    game_started = False
    on_floor = False

    bird.rect.center = (WIDTH//2, HEIGHT//2 - 50)
    bird.vy = 0
    bird.alive = True
    bird.moving = False

    top_pipe.kill()
    bot_pipe.kill()

    spawn_pipes()

    game_over_text_Y = HEIGHT//2 - 250
    game_over_alpha = 0
    game_over_score_alpha = 0


async def main():
    global running, game_started, mute, game_over, jump_extra_pipe_speed, extra_pipe_speed, scored, score
    while running:  
        # Handle events 
        for event in pygame.event.get():    
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_x): 
                running = False 
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_r and game_over:    
                initialize_game()   
        
            # Extra speed when jumped    
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_UP and not game_started and not jump_extra_pipe_speed >= 30:    
                jump_extra_pipe_speed += 0.1    
                jump_extra_pipe_speed = round(jump_extra_pipe_speed, 1)     
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN and not game_started and not jump_extra_pipe_speed == 0:   
                jump_extra_pipe_speed -= 0.1    
                jump_extra_pipe_speed = round(jump_extra_pipe_speed, 1)     
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT and not game_started and not jump_extra_pipe_speed >= 30: 
                jump_extra_pipe_speed += 1  
                jump_extra_pipe_speed = round(jump_extra_pipe_speed, 1)     
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT and not game_started and not jump_extra_pipe_speed <= 0:   
                jump_extra_pipe_speed -= 1  
                jump_extra_pipe_speed = round(jump_extra_pipe_speed, 1) 
        
            # Manual extra speed    
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_h and game_started and not game_over:   
                extra_pipe_speed +=5    
        
            # Jumping    
            elif not game_started and event.type == pygame.MOUSEBUTTONDOWN: 
                if mute == "False": 
                    wing_sound.play()   
                game_started = True 
                bird.rotation = 45  
                bird.vy = JUMP_POWER    
                bird.moving = True  
                top_pipe.moving = True  
                bot_pipe.moving = True  
            elif not game_started and event.type == pygame.KEYDOWN and (event.key == pygame.K_SPACE or event.key == pygame.K_w):    
                if mute == "False": 
                    wing_sound.play()   
                extra_pipe_speed += jump_extra_pipe_speed   
                game_started = True 
                bird.rotation = 45  
                bird.vy = JUMP_POWER    
                bird.moving = True  
                top_pipe.moving = True  
                bot_pipe.moving = True  
            elif (game_started and not game_over) and event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.KEYDOWN and (event.key == pygame.K_SPACE or event.key == pygame.K_w):    
                if mute == "False": 
                    wing_sound.play()   
                extra_pipe_speed += jump_extra_pipe_speed   
                bird.rotation = 45  
                bird.vy = JUMP_POWER    
        
            # Muting    
            elif (mute == "False") and event.type == pygame.KEYDOWN and event.key == pygame.K_m:    
                mute = "True"   
            elif (mute == "True") and event.type == pygame.KEYDOWN and event.key == pygame.K_m: 
                mute = "False"  
        
        game_sprites.update()   
        
        if not game_started and game_over == False: 
            draw_screen()   
            show_opening_text() 
        
            if jump_extra_pipe_speed >= 30: 
                jump_extra_pipe_speed = 30  
                
            if jump_extra_pipe_speed <= 0:  
                jump_extra_pipe_speed = 0   
        
        if game_started:    
            if not game_over:   
                draw_screen()   
                draw_score_speed_and_mute() 
                pipe_sprites.update(extra_pipe_speed)   
        
                # Check for bird collision  
                hit = pygame.sprite.collide_rect(bird, top_pipe) or pygame.sprite.collide_rect(bird, bot_pipe) or pygame.sprite.collide_rect(bird, grass)   
        
                if hit: 
                    if mute == "False": 
                        hit_sound.play()    
                    game_over = True    
                    bird.alive = False  
                    scored = False  
        
                while game_over and (pygame.sprite.collide_rect(bird, top_pipe) or pygame.sprite.collide_rect(bird, bot_pipe)): 
                    top_bot_move()  
        
                # Check if scored   
                if top_pipe.rect.x < bird.rect.x and bot_pipe.rect.x < bird.rect.x + 50 and scored == False:    
                    if mute == "False": 
                        point_sound.play()  
                    scored = True   
                    score += 1  
        
                # Set Grivity and Jump  
                bird.vy += GRAVITY      
                bird.rect.y += bird.vy  
        
                if top_pipe.rect.x < -35 and bot_pipe.rect.x < -35: 
                    spawn_pipes()   
                    scored = False  
        
            else:   
                draw_screen()   
                draw_game_over_text()   
        
        pygame.display.flip()   
        await asyncio.sleep(0)
        clock.tick(60)  
        
asyncio.run(main())
pygame.quit()