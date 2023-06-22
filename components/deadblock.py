import pygame

class Deadblock():
    """ Represents the game blocks that have died.
    """
    def __init__(self,x,y,color,screen):
        """ Initializing the dead game block class.

        Args:
            x (int): The x coordinate of the game blocks.
            y (int): The y coordinate of the game blocks.
            color (tuple): The rgb tuple that represents the color of the game block.
            screen (pygame.display): The screen the game blocks is displayed on.
        """
        self.x = x
        self.y = y
        self.color = color
        self.screen = screen


    def display_block(self):
        """ Displays the image of the dead block in the screen.
        """
        x = 50*self.x 
        y = 50*self.y
        pygame.draw.rect(self.screen,self.color,[x,y,50,50])


