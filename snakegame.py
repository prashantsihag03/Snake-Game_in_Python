import pygame
import time
import random

x = pygame.init()
#print(x) ----- To check whether initialization is successfull or not.

#variables----------------
White = (255,255,255)
Black = (0,0,0)
Red = (255,0,0)
Green = (0,155,0)

display_width = 800
display_height = 600
FPS = 30
block_size = 20
appleThickness = 30
pixel_move = 10
clock = pygame.time.Clock()
smallFont = pygame.font.SysFont("comicsansms", 25)
medFont = pygame.font.SysFont("comicsansms", 35)
largeFont = pygame.font.SysFont("comicsansms", 50)

direction = "right"
img = pygame.image.load("snake.gif")
appleimg = pygame.image.load("apple.png")

#variables-----------------

#functions-------------------
def score(score):
    text = smallFont.render("Score: "+str(score), True, Black)
    gameDisplay.blit(text, [0,0])
    
def pause():
    
    paused = True
    message_to_screen("Paused", Black, size="medium", y_displace = -50)
    message_to_screen("Press c to continue or q to quit", Black, size="small")
    pygame.display.update()
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    paused = False
                    
                elif event.key == pygame.K_q:
                    pygame.quit()
                    quit()

        gameDisplay.fill(White)
        message_to_screen("Paused", Black, size="medium", y_displace = -50)
        message_to_screen("Press c to continue or q to quit", Black, size="small")
        pygame.display.update()
        clock.tick(5)
    
def message_to_screen(msg, color, size="small", y_displace=0, x_displace=0):

    if size == "small":
        text_surf = smallFont.render(msg, True, color)
        
    elif size == "medium":
        text_surf = medFont.render(msg, True, color)
        
    elif size == "large":
        text_surf = largeFont.render(msg, True, color)
        
    #pygame provides no way to directly draw text on an existing Surface: instead you must use Font.render() to create an image (Surface) of the text,
    #then blit this image onto another Surface. The text can only be a single line: newline characters are not rendered.
    text_rect = text_surf.get_rect() #get_rect() is used to get the rectangular area of the Surface.
    text_rect.center = (display_width/2)+x_displace, (display_height/2)+y_displace
    gameDisplay.blit(text_surf, text_rect) #It is a thin wrapper around a Pygame surface that allows you to easily draw images to the screen (“blit” them).

def randapplegen():
    randAppleX = round(random.randrange(0, display_width-appleThickness))#/10.0)*10.0
    randAppleY = round(random.randrange(0, display_height-appleThickness))#/10.0)*10.0
    return randAppleX,randAppleY
def gameIntro():

    intro = True

    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    intro = False
                    
                elif event.key == pygame.K_q:
                    pygame.quit()
                    quit()
                
        gameDisplay.fill(White)
        message_to_screen("Welcome to Snake-Game",
                           Green,
                           size="large",
                           y_displace= -100)
        message_to_screen("Objectives of the game is to eat apples presented in red color.",
                           Black,
                           size="small",
                           y_displace= -30)
        message_to_screen("The more apples you eat, the longer the snake gets.",
                           Black,size="small",
                           y_displace= 10)
        message_to_screen("If you run into yourself or the edges, you die !",
                           Black,
                           size="small",
                           y_displace= 50)
        message_to_screen("Press c to start or q to quit. Press p to pause.",
                           Black,
                           size="small",
                           y_displace= 80)

        pygame.display.update()
        clock.tick(5)

        
def snake(block_size, snakeList):
    if direction == "right":
        head = pygame.transform.rotate(img, 270)

    elif direction == "left":
        head = pygame.transform.rotate(img, 90)

    elif direction == "up":
        head = img

    elif direction == "down":
        head = pygame.transform.rotate(img, 180)
        
    gameDisplay.blit(head, (snakeList[-1][0], snakeList[-1][1]))
    
    for XnY in snakeList[:-1]:
        pygame.draw.rect(gameDisplay, Green, [XnY[0], XnY[1], block_size, block_size])  #One-way of drawing something
        #gameDisplay.fill(Red, rect=[200,100,100,50])                                   #Another-way of drawing something

def gameLoop():
    global direction
    direction = 'right'
    gameExit = False
    gameOver = False
    lead_x = display_width/2
    lead_y = display_height/2
    lead_x_change = 0
    lead_y_change = 0
    snakeList = []
    snakeLength = 1

    randAppleX,randAppleY = randapplegen()
    
    while not gameExit:
        if gameOver == True:
            message_to_screen("Game Over", Red, size="large", y_displace=0, x_displace=0)
            message_to_screen("Press c to play again OR q to quit.", Black, size="small", y_displace = 50, x_displace= 0)
            pygame.display.update()

        while gameOver == True:
            
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        gameExit = True
                        gameOver = False
                    if event.key == pygame.K_c:
                        gameLoop()
                
        for event in pygame.event.get():
            #print(event) ---- To print out all the events happening.
            if event.type == pygame.QUIT:
                gameExit = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    direction = "left"
                    lead_x_change = -pixel_move
                    lead_y_change = 0
                elif event.key == pygame.K_RIGHT:
                    direction = "right"
                    lead_x_change = pixel_move
                    lead_y_change = 0
                elif event.key == pygame.K_UP:
                    direction = "up"
                    lead_y_change = -pixel_move
                    lead_x_change = 0
                elif event.key == pygame.K_DOWN:
                    direction = "down"
                    lead_y_change = pixel_move
                    lead_x_change = 0
                elif event.key == pygame.K_p:
                    pause()
                
            
            #below code to stop the movement when user releases the key. Commented bcoz we dont need that feature in snake-game
            #if event.type == pygame.KEYUP:
                #if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    #lead_x_change = 0

        if lead_x >= display_width or lead_x <= 0 or lead_y >= display_height or lead_y <= 0:
            gameOver = True

        lead_x += lead_x_change
        lead_y += lead_y_change
        gameDisplay.fill(White)
        
        #pygame.draw.rect(gameDisplay, Red, [randAppleX, randAppleY, appleThickness, appleThickness])

        gameDisplay.blit(appleimg, (randAppleX, randAppleY))
        
        snakeHead = []
        snakeHead.append(lead_x)
        snakeHead.append(lead_y)
        snakeList.append(snakeHead)

        if len(snakeList) > snakeLength:
            del snakeList[0]

        for eachSegment in snakeList[:-1]:
            if eachSegment == snakeHead:
                gameOver = True
            
        
        snake(block_size, snakeList)
        score(snakeLength - 1)
        pygame.display.update()

##        if(lead_x == randAppleX and lead_y == randAppleY):
##            randAppleX = round(random.randrange(0, display_width-appleThickness)/10.0)*10.0
##            randAppleY = round(random.randrange(0, display_height-appleThickness)/10.0)*10.0
##            snakeLength += 1

##        if lead_x >= randAppleX and lead_x <= randAppleX + appleThickness:
##            if lead_y >= randAppleY and lead_y <= randAppleY + appleThickness:
##                randAppleX = round(random.randrange(0, display_width-appleThickness))#/10.0)*10.0
##                randAppleY = round(random.randrange(0, display_height-appleThickness))#/10.0)*10.0
##                snakeLength += 1

        if lead_x > randAppleX and lead_x < randAppleX + appleThickness or lead_x + block_size > randAppleX and lead_x + block_size < randAppleX + appleThickness:
            if lead_y > randAppleY and lead_y < randAppleY + appleThickness or lead_y + block_size > randAppleY and lead_y + block_size < randAppleY + appleThickness:
                randAppleX,randAppleY = randapplegen()
                snakeLength += 1
                
                

        clock.tick(FPS)    

    pygame.quit()
    quit()

#functions-------------------
    
gameDisplay = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption("ProjectX")
icon = pygame.image.load("apple.png")
pygame.display.set_icon(icon)
#pygame.display.flip()
#pygame.display.update()
gameIntro()
gameLoop()

