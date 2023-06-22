import random #To generate a random number for the pipes
import sys #To use sys.exit() function
import pygame
from pygame.locals import *

#Global varibales for the game
FPS = 40
SCREENWIDTH = 285
SCREENHEIGHT = 500
SCREEN = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT)) #Creates a display surface #tuple of two integers
#set_mode(size=(0, 0), flags=0, depth=0, display=0, vsync=0) -> Surface
#The size argument is a pair of numbers representing the width and height. 
GROUNDY = SCREENHEIGHT * 0.8
#define two dictionaries
GAME_SPRITES = {}
GAME_SOUNDS = {}
PLAYER = 'gallery/sprites/bird.png'
BACKGROUND = 'gallery/sprites/background.png'
PIPE = 'gallery/sprites/pipe.png'
def welcomeScreen():
    #Shows welcome image on the screen

    playerx = int(SCREENWIDTH/5) #Taking only integer values while blitting
    playery = int((SCREENHEIGHT-GAME_SPRITES['player'].get_height())/2)
    messagex = int((SCREENWIDTH-GAME_SPRITES['message'].get_width())/2)
    messagey = int(SCREENHEIGHT*0.15)
    basex = 0
    while True:
        for event in pygame.event.get(): #gets me all the events 
            #if user clicks on the cross button, close the game
            if event.type == QUIT or (event.type==KEYDOWN and event.key==K_ESCAPE): #KEYDOWN->any key has been pressed
                pygame.quit()
                sys.exit()
            #If the user presses space or up key, start the game for them
            elif event.type==KEYDOWN and (event.key==K_SPACE or event.key==K_UP):
                return 
            else:
                SCREEN.blit(GAME_SPRITES['background'], (0, 0))
                SCREEN.blit(GAME_SPRITES['player'], (playerx, playery))
                SCREEN.blit(GAME_SPRITES['message'], (messagex, messagey))
                SCREEN.blit(GAME_SPRITES['base'], (basex, GROUNDY))
                pygame.display.update() # TO CHANGE SCREEN
                FPSCLOCK.tick(FPS) #CONTROL THE FPS OF THE GAME
def mainGame():
    score = 0
    playerx =  int(SCREENWIDTH/5)
    playery =  int(SCREENWIDTH/2)
    basex = 0

    #Create two pipes for blitting on the screen
    newPipe1 = getRandomPipe()
    newPipe2 = getRandomPipe()

    # my List of upper pipes
    upperPipes = [
        {'x': SCREENWIDTH + 220, 'y': newPipe1[0]['y']},
        {'x': SCREENWIDTH + 220 + (SCREENWIDTH / 2), 'y': newPipe2[0]['y']},
    ]
    # my List of lower pipes
    lowerPipes = [
        {'x': SCREENWIDTH + 220, 'y': newPipe1[1]['y']},
        {'x': SCREENWIDTH + 220 + (SCREENWIDTH / 2), 'y': newPipe2[1]['y']},
    ]

    pipeVelx = -4 #Seems like bird is moving forward

    playerVelY = -9
    playerMaxVelY = 10
    playerMinVelY = -8
    playerAccY = 1

    playerFlapAccv = -8 #Velocity while Flapping
    playerFlapped = False #It is true only when the bird is flapping

    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type==KEYDOWN and event.key==K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type ==  KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                if playery > 0:
                    playerVelY = playerFlapAccv
                    playerFlapped = True
                    GAME_SOUNDS['wing'].play()

        crashTest = isCollide(playerx,playery,upperPipes,lowerPipes)#This function will return true if the player is crashed
        if crashTest:
            return
        #check for score
        playerMidPos = playerx + GAME_SPRITES['player'].get_width()/2 #to get to the center of the player
        for pipe in upperPipes:
            pipeMidPos = pipe['x'] + GAME_SPRITES['pipe'][0].get_width()/2 #center of the pipe
            if pipeMidPos <= playerMidPos < pipeMidPos + 4:
                score += 1
                print(f'Your score is {score}')
            GAME_SOUNDS['point'].play()

        if playerVelY < playerMaxVelY and not playerFlapped:
            playerVelY += playerAccY
             
        if playerFlapped:
            playerFlapped = False
        playerHeight = GAME_SPRITES['player'].get_height()
        playery = playery + min(playerVelY, GROUNDY - playery - playerHeight)
        #playery is increased only when the player is not coming down
        
        #move pipes to the left
        for upperpipe, lowerpipe in zip(upperPipes,lowerPipes):
            upperpipe['x'] += pipeVelx
            lowerpipe['x'] += pipeVelx 

        #Add a new pipe when the first pipe is about to cross the leftmost part of the screen
        if 0 < upperPipes[0]['x']<5:
            newpipe = getRandomPipe()
            upperPipes.append(newpipe[0])
            lowerPipes.append(newpipe[1])

        #if the pipe is out of the screen then remove it
        if upperPipes[0]['x'] < -GAME_SPRITES['pipe'][0].get_width():
            upperPipes.pop(0)
            lowerPipes.pop(0)            

        #Blit the sprites now
        SCREEN.blit(GAME_SPRITES['background'],(0,0))
        for upperpipe, lowerpipe in zip(upperPipes,lowerPipes):
            SCREEN.blit(GAME_SPRITES['pipe'][0],(upperpipe['x'],upperpipe['y']))
            SCREEN.blit(GAME_SPRITES['pipe'][1],(lowerpipe['x'],lowerpipe['y']))

        SCREEN.blit(GAME_SPRITES['base'],(basex,GROUNDY))
        SCREEN.blit(GAME_SPRITES['player'],(playerx,playery))
        myDigits = [int(x) for x in list(str(score))] 
        width = 0   
        for digit in myDigits:
            width += GAME_SPRITES['numbers'][digit].get_width()

        Xoffset = (SCREENWIDTH - width)/2

        for digit in myDigits:
            SCREEN.blit(GAME_SPRITES['numbers'][digit], (Xoffset, SCREENHEIGHT*0.12))
            Xoffset += GAME_SPRITES['numbers'][digit].get_width()
        pygame.display.update()
        FPSCLOCK.tick(FPS)
def isCollide(playerx,playery,upperPipes,lowerPipes):
    if (playery > (GROUNDY - 25)) or (playery < 0):
        GAME_SOUNDS['hit'].play()
        return True
    for pipe in upperPipes:
        pipeHeight = GAME_SPRITES['pipe'][0].get_height()
        if (playery < pipeHeight + pipe['y'] and abs(playerx - pipe['x']) < GAME_SPRITES['pipe'][0].get_width()):
            GAME_SOUNDS['hit'].play()
            return True  

    for pipe in lowerPipes:
        
        if (playery + GAME_SPRITES['player'].get_height() > pipe['y']) and abs(playerx - pipe['x']) < GAME_SPRITES['pipe'][0].get_width():
            GAME_SOUNDS['hit'].play()
            return True  

def getRandomPipe():
    """
    Generate positions of two pipes (one bottom straight and one top rotated) for blitting on the screen
    """
    pipeHeight = GAME_SPRITES['pipe'][0].get_height()
    offset = SCREENHEIGHT/3
    y2 = offset + random.randrange(0,int(SCREENHEIGHT-GAME_SPRITES['base'].get_height() - 1.2*offset))
    pipex = SCREENWIDTH+10
    y1 = pipeHeight - y2 + offset
    pipe = [
        {'x':pipex, 'y': -y1}, #Upper pipe
        {'x':pipex, 'y': y2}  #Lower pipe
    ]
    return pipe
    
#if __name__ == '__main__' means->execute following code only if this file is run as a script from the command line and if the file is imported from another file, the code will not be executed.

if __name__ == "__main__":
    #This wii be the main point from where the game will start
    pygame.init() #Initializes all modules of pygame
    FPSCLOCK = pygame.time.Clock() #This clock is used to control the FPS of the game 
    pygame.display.set_caption('Flappy Bird')
    GAME_SPRITES['numbers'] = (
        pygame.image.load('gallery/sprites/0.png').convert_alpha(), #used to render image to the screen; faster blitting
        pygame.image.load('gallery/sprites/1.png').convert_alpha(),
        pygame.image.load('gallery/sprites/2.png').convert_alpha(),
        pygame.image.load('gallery/sprites/3.png').convert_alpha(),
        pygame.image.load('gallery/sprites/4.png').convert_alpha(),
        pygame.image.load('gallery/sprites/5.png').convert_alpha(),
        pygame.image.load('gallery/sprites/6.png').convert_alpha(),
        pygame.image.load('gallery/sprites/7.png').convert_alpha(),
        pygame.image.load('gallery/sprites/8.png').convert_alpha(),
        pygame.image.load('gallery/sprites/9.png').convert_alpha(),
        pygame.image.load('gallery/sprites/0.png').convert_alpha()
    ) #tuple
    GAME_SPRITES['message'] = pygame.image.load('gallery/sprites/message.png').convert_alpha()
    GAME_SPRITES['base'] = pygame.image.load('gallery/sprites/base.png').convert_alpha()
    GAME_SPRITES['pipe'] = (
    pygame.transform.rotate(pygame.image.load(PIPE).convert_alpha(),180),
    pygame.image.load(PIPE).convert_alpha()
    )

    #GAME SOUNDS
    GAME_SOUNDS['die'] = pygame.mixer.Sound('gallery/audio/die.wav')
    GAME_SOUNDS['hit'] = pygame.mixer.Sound('gallery/audio/hit.wav')
    GAME_SOUNDS['point'] = pygame.mixer.Sound('gallery/audio/point.wav')
    GAME_SOUNDS['swoosh'] = pygame.mixer.Sound('gallery/audio/swoosh.wav')
    GAME_SOUNDS['wing'] = pygame.mixer.Sound('gallery/audio/wing.wav')

    GAME_SPRITES['background'] = pygame.image.load(BACKGROUND).convert()
    GAME_SPRITES['player'] = pygame.image.load(PLAYER).convert_alpha()

    while True:
        welcomeScreen() #Shows welcome screen to the user until a button is pressed
        mainGame() #Main game function