import pygame
from game_screens.gameplay import GamePlay

#Dimensions of screen
HEIGHT = 20
WIDTH = 10
MULTIPLIER = 50

#Setting up the game window.
pygame.init()
running = True
screen = pygame.display.set_mode((WIDTH*MULTIPLIER + 200,HEIGHT*MULTIPLIER))

#Screens
gp = GamePlay(screen,WIDTH,HEIGHT,MULTIPLIER)

#Loop to run game
while running:

    #Checking if user exited out of window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    #Entry pointy into game
    gp.run()




        
