import pygame
import random
import time

pygame.init()

white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 128, 0)
chrome_white = (232, 231, 226)
masala = (87, 86, 84)
redoxide = (106, 27, 27)

font1 = pygame.font.SysFont(None, 35)
font2 = pygame.font.SysFont(None, 35)

display_width = 1024
display_height = 768

gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('Catch')

fps = 200
clock = pygame.time.Clock()

channels = [75, 175, 275, 375, 475, 575, 675, 775, 875, 975]
channels_beingused = [False, False, False, False, False, False, False, False, False, False]

#collecting these objects will result in positive points
class goodFO:
    change_gfo = 3

    def speedup(self):
        self.change_gfo += 1

    def __init__(self, channelnumber):
        self.x_coord = channels[channelnumber]
        self.y_coord = -10  

    def drawFO(self, x_basket, y_basket):
        if self.x_coord > x_basket - 5 and self.x_coord < x_basket + 75 :
            if self.y_coord > y_basket + 10 :
                positivescore()
                self.x_coord = channels[random.randint(0, 9)]
                self.y_coord = -10

        if self.y_coord <= display_height*0.95 :
            pygame.draw.circle(gameDisplay, green, [self.x_coord, self.y_coord], 15)    
            self.y_coord += self.change_gfo

        else:
            self.x_coord = channels[random.randint(0, 9)]
            self.y_coord = -10    
 
 #collecting these objects will result in negative points
class badFO:
    change_bfo = 4

    def speedup(self):
        self.change_bfo += 1

    def __init__(self, channelnumber):
        self.x_coord = channels[channelnumber]
        self.y_coord = -10  

    def drawFO(self, x_basket, y_basket):
        global gameover
        if self.x_coord > x_basket - 5 and self.x_coord < x_basket + 75 :
            if self.y_coord > y_basket + 10 :
                gameover = True
                self.x_coord = channels[random.randint(0, 9)]
                self.y_coord = -10

        if self.y_coord <= display_height*0.95 :
            pygame.draw.circle(gameDisplay, red, [self.x_coord, self.y_coord], 15)    
            self.y_coord += self.change_bfo

        else:
            self.x_coord = channels[random.randint(0, 9)]
            self.y_coord = -10   

score = None
gameover = None

def initgameover():
    global gameover
    gameover = False

def initscore():
    global score
    score = 0

def positivescore():
    global score
    score += 1
    
def display_score(score):
    screen_text = font1.render(score, True, black)
    gameDisplay.blit(screen_text, [display_width*0.93, display_height*0.07])

def display_message(msg, color, x, y):
    screen_text = font2.render(msg, True, color)
    gameDisplay.blit(screen_text, [x, y])    

#display_message("Press 'S' to start", black)
#pygame.display.update()

def gameLoop():

    global gameover
    goodob = goodFO(random.randint(0, 9))
    badob = badFO(random.randint(0, 9))
    initgameover()
    initscore()
    speed = False
    start = time.time()
    gameExit = False
    lead_x = display_width/50
    lead_y = display_height*0.85
    change_x = 5

    right = False
    left = False
    up = False
    down = False

    while not gameExit:

        if time.time() > start + 15:
            speed = True

        if speed == True:
            change_x += 1
            goodob.speedup()
            badob.speedup()
            speed = False
            start = time.time()

        while gameover == True:
            gameDisplay.fill(chrome_white)
            display_message("Your Score : %d"%score, green, display_width*0.42, display_height*0.45)
            display_message("GAME OVER", red, display_width*0.42, display_height*0.35)
            display_message("Press R to try again, Press Q to quit", black, display_width*0.3, display_height*0.55)
            pygame.display.update()
            
            for event in pygame.event.get():
                print(event)
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        gameLoop()
                    if event.key == pygame.K_q:
                        gameover = False
                        gameExit = True    
                if event.type == pygame.QUIT:
                    gameover = False
                    gameExit = True

        for event in pygame.event.get():
            print(event)
            if event.type == pygame.QUIT:
                gameExit = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    right = True
                if event.key == pygame.K_LEFT:
                    left = True
                #if event.key == pygame.K_DOWN:
                    #down = True
                #if event.key == pygame.K_UP:
                    #up = True 
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT:
                    right = False
                if event.key == pygame.K_LEFT:
                    left = False
                #if event.key == pygame.K_DOWN:
                        #down = False
                #if event.key == pygame.K_UP:
                        #up = False

        if right == True and lead_x <= 948:
            lead_x += change_x
        if left == True and lead_x >= 7:
            lead_x -= change_x
        #if down == True and lead_y <= 722:
        #    lead_y += 1.1
        #if up == True and lead_y >= 7:
        #    lead_y -= 1.1 

        gameDisplay.fill(chrome_white)
            
        goodob.drawFO(lead_x, lead_y)
        badob.drawFO(lead_x, lead_y)

        display_score(str(score))
        pygame.draw.line(gameDisplay, redoxide, (0, 0), (1024, 0), 10)
        pygame.draw.line(gameDisplay, redoxide, (0, 0), (0, 768), 10)
        pygame.draw.line(gameDisplay, redoxide, (0, 768), (1024, 768), 14)
        pygame.draw.line(gameDisplay, redoxide, (1024, 768), (1024, 0), 14)
        pygame.draw.arc(gameDisplay, masala, [lead_x, lead_y, 70, 70], 3, 6.45, 7)
        
        pygame.display.update() 
        clock.tick(fps)   

    pygame.quit()
    quit()

gameLoop()    
  