import pygame
import random
import os
import datetime

pygame.mixer.init()

pygame.init()

#colors
white = (255, 255, 255) # R G B values
red = (255, 0, 0)
black = (0, 0, 0)

#creating Window
screen_width = 900
screen_height = 500
gamewindow = pygame.display.set_mode((screen_width, screen_height))

#backgroug image
bgimage = pygame.image.load("assets/gameBackground.jpg")
bgimage = pygame.transform.scale(bgimage, (screen_width, screen_height)).convert_alpha()

#background game over image
bg_gameover_image = pygame.image.load("assets/gameOver.jpg")
bg_gameover_image = pygame.transform.scale(bg_gameover_image, (screen_width, screen_height)).convert_alpha()

#home backgroug image
home_bgimage = pygame.image.load("assets/home.jpg")
home_bgimage = pygame.transform.scale(home_bgimage, (screen_width, screen_height)).convert_alpha()

pygame.display.set_caption("Snake")
pygame.display.update()

clock = pygame.time.Clock()

font = pygame.font.SysFont(None, 55)
font1 = pygame.font.SysFont(None, 30)

def text_screen(text, color, x, y):
    screen_text = font.render(text, True, color)
    gamewindow.blit(screen_text, (x,y))

def text_screen1(text, color, x, y):
    screen_text1 = font1.render(text, True, color)
    gamewindow.blit(screen_text1, (x,y))

def plot_snake(gamewindow, color, snk_list, snake_size):
    for x,y in snk_list:
        pygame.draw.rect(gamewindow, color, [x, y, snake_size, snake_size])

def welcome():
    exit_game = False
    while not exit_game:
        gamewindow.fill(white) #try random colors
        gamewindow.blit(home_bgimage,(0,0))
        text_screen("WLCOME TO SNAKE GAME", white, 176, 150)
        text_screen1("-> Press SPACE BAR to continue.", white, 176, 300)
        text_screen1("-> Press Q to exit from the game.", white, 176, 350)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game = True
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    pygame.mixer.music.load('assets/Sneaky-Snitch-background.mp3')
                    pygame.mixer.music.play()
                    gameloop()
                if event.key == pygame.K_q:
                    exit()
                

        pygame.display.update()
        clock.tick(60)



#game loop
def gameloop():
    #game specific variables
    exit_game = False
    game_over = False
    snake_x = 45
    snake_y = 55
    velocity_x = 0
    velocity_y = 0

    #food for snake
    food_x = random.randint(20, screen_width/2) 
    food_y = random.randint(20, screen_height/2)
    score = 0
    init_velocity = 5

    snake_size = 20   # snake size can be changed
    fps = 60

    snk_list = []
    snk_length = 1

    # Check if high score file exists
    if(not os.path.exists("highscore.txt")):
        with open("highscore.txt", "w") as f:
            f.write("0")


    with open("highscore.txt", "r") as f:
        highscore = f.read()


    while not exit_game:

        if game_over:
            with open("highscore.txt", "w") as f:
                f.write(str(highscore))
            gamewindow.fill(white)
            gamewindow.blit(bg_gameover_image,(0,0))
            text_screen1("Game Over, Choose the following:", red, 250, 200) #try random numbers
            text_screen1("-> Press enter to return main menu", white, 270, 250)
            text_screen1("-> Press Q to exit from the game!", red, 270, 300)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True


                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        #gameloop()
                        welcome()
                    if event.key == pygame.K_q:
                        exit()
        else:
            for event in pygame.event.get():
                #print(event)

                if event.type == pygame.QUIT:
                    exit_game = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        velocity_x = init_velocity
                        velocity_y = 0

                    if event.key == pygame.K_LEFT:
                        velocity_x = - init_velocity
                        velocity_y = 0

                    if event.key == pygame.K_UP:
                        velocity_y = - init_velocity
                        velocity_x = 0
                    
                    if event.key == pygame.K_DOWN:
                        velocity_y = init_velocity
                        velocity_x = 0


            snake_x = snake_x + velocity_x
            snake_y = snake_y + velocity_y

            if abs(snake_x - food_x)<8 and abs(snake_y - food_y)<8:
                score += 10
                
                food_x = random.randint(20, screen_width/2) 
                food_y = random.randint(20, screen_height/2)
                snk_length += 5
                #init_velocity += 0.5
                if score>int(highscore):
                    highscore = score

            gamewindow.fill(white)
            gamewindow.blit(bgimage, (0,0))
            text_screen1("Score: "+ str(score) + "    Hight Score: "+str(highscore), (255,255,255), 5, 5)
            #text_screen("Timr")
            pygame.draw.rect(gamewindow, red, [food_x, food_y, snake_size, snake_size])

            head = []
            head.append(snake_x)
            head.append(snake_y)
            snk_list.append(head)

            if len(snk_list)>snk_length:
                del snk_list[0]


            if head in snk_list[:-1]:
                game_over = True
                pygame.mixer.music.load('assets/snake_gameover.mp3')
                pygame.mixer.music.play()

                
            if snake_x<0 or snake_x>screen_width or snake_y<0 or snake_y>screen_height:
                game_over = True
                #print("Game Over:")
                pygame.mixer.music.load('assets/snake_gameover.mp3')
                pygame.mixer.music.play()

            plot_snake(gamewindow, black, snk_list, snake_size)
        pygame.display.update()
        clock.tick(fps)

    pygame.quit()
    quit()

welcome()