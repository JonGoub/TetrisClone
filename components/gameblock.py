import pygame,random
pygame.init()

class Gameblock():
    """ Generic object that can represents the various game blocks in the Tetris game.
    """

    def __init__(self,x,y,screen,multiplier):
        """ Initializing the game piece class.

        Args:
            x (int): The x coordinate of the game blocks.
            y (int): The y coordinate of the game blocks.
            screen (pygame.display): The screen the game blocks is displayed on.
            multiplier (int): The size of the blocks that make up the game blocks.
        """
        self.x = x
        self.y = y
        self.multiplier = multiplier
        self.screen = screen
        self.flip_sound = pygame.mixer.Sound('./assets/flip_sound.mp3')
        self.color = (random.randrange(50,255),random.randrange(50,255),random.randrange(50,255))
        self.block_type = [
                       #Jblock
                       [[[0,1,0,0],
                         [0,1,1,1],
                         [0,0,0,0],
                         [0,0,0,0]],

                        [[0,0,1,1],
                         [0,0,1,0],
                         [0,0,1,0],
                         [0,0,0,0]],
        
                        [[0,0,0,0],
                         [0,1,1,1],
                         [0,0,0,1],
                         [0,0,0,0]],

                        [[0,0,1,0],
                         [0,0,1,0],
                         [0,1,1,0],
                         [0,0,0,0]]],
                        
                       #Iblock
                       [[[0,0,0,0],
                         [1,1,1,1],
                         [0,0,0,0],
                         [0,0,0,0]],
 
                        [[0,0,1,0],
                         [0,0,1,0],
                         [0,0,1,0],
                         [0,0,1,0]],
        
                        [[0,0,0,0],
                         [0,0,0,0],
                         [1,1,1,1],
                         [0,0,0,0]],

                        [[0,1,0,0],
                         [0,1,0,0],
                         [0,1,0,0],
                         [0,1,0,0]]],


                       #Lblock
                       [[[0,0,0,1],
                         [0,1,1,1],
                         [0,0,0,0],
                         [0,0,0,0]],

                        [[0,0,1,0],
                         [0,0,1,0],
                         [0,0,1,1],
                         [0,0,0,0]],
        
                        [[0,0,0,0],
                         [0,1,1,1],
                         [0,1,0,0],
                         [0,0,0,0]],

                        [[0,1,1,0],
                         [0,0,1,0],
                         [0,0,1,0],
                         [0,0,0,0]]],

                       #Oblock
                       [[[1,1,0,0],
                         [1,1,0,0],
                         [0,0,0,0],
                         [0,0,0,0]],

                        [[1,1,0,0],
                         [1,1,0,0],
                         [0,0,0,0],
                         [0,0,0,0]],

                        [[1,1,0,0],
                         [1,1,0,0],
                         [0,0,0,0],
                         [0,0,0,0]],


                        [[1,1,0,0],
                         [1,1,0,0],
                         [0,0,0,0],
                         [0,0,0,0]]],


                       #Sblock
                       [[[0,0,0,0],
                         [0,1,1,0],
                         [1,1,0,0],
                         [0,0,0,0]],

                       [[0,1,0,0],
                        [0,1,1,0],
                        [0,0,1,0],
                        [0,0,0,0]],
        
                       [[0,0,0,0],
                        [0,1,1,0],
                        [1,1,0,0],
                        [0,0,0,0]],

                       [[0,1,0,0],
                        [0,1,1,0],
                        [0,0,1,0],
                        [0,0,0,0]]],


                      #Tblock
                      [[[0,1,0,0],
                        [1,1,1,0],
                        [0,0,0,0],
                        [0,0,0,0]],

                       [[0,1,0,0],
                        [0,1,1,0],
                        [0,1,0,0],
                        [0,0,0,0]],
                        
                       [[0,0,0,0],
                        [1,1,1,0],
                        [0,1,0,0],
                        [0,0,0,0]],
                    
                       [[0,1,0,0],
                        [1,1,0,0],
                        [0,1,0,0],
                        [0,0,0,0]]],


                      #Zblock
                      [[[0,0,0,0],
                        [0,1,1,0],
                        [0,0,1,1],
                        [0,0,0,0]],

                       [[0,0,0,0],
                        [0,0,1,0],
                        [0,1,1,0],
                        [0,1,0,0]],
        
                       [[0,0,0,0],
                        [0,1,1,0],
                        [0,0,1,1],
                        [0,0,0,0]],

                       [[0,0,0,0],
                        [0,0,1,0],
                        [0,1,1,0],
                        [0,1,0,0]]]
                                    ]
        

        self.images = self.block_type[random.randrange(0,6)]                    
        self.index = 0
        self.image = self.images[self.index]
        self.counter = 0
        self.freeze = False


    def display_block(self):
        """ Displays the image of the block in the screen.
        """
        for i in range(4):
            for j in range(4):
                if self.image[i][j] == 1:
                    x = self.multiplier*self.x + j*self.multiplier
                    y = self.multiplier*self.y + i*self.multiplier
                    pygame.draw.rect(self.screen,self.color,[x,y,self.multiplier,self.multiplier])


    def update(self):
        """ Timer used to make the game block move downwards once every second.
        """
        self.counter +=1 
        if self.counter == 60:
            self.y += 1
            self.counter = 0


    def flip(self):
        """ Rotates the orientation of the game block clockwise.
        """
        self.index += 1
        if self.index >= len(self.image):
            self.index = 0
        self.image = self.images[self.index]
        self.index = self.index

        x_high = 0
        x_low = 10
        
        #Gets the lowest and highest 
        for i in range(4):
            for j in range(4):
                if self.image[i][j] == 1:
                    x = self.x + j
                    if x > x_high:
                        x_high = x
                    if x < x_low:
                        x_low = x
        if x_high > 9:
            self.x -=(x_high - 9)

        if x_low < 0:
            self.x += abs(x_low)

        pygame.mixer.Sound.play(self.flip_sound)


    def hit_ground(self):
        """Calculates if the game block has hit the ground.

        Returns:
            boolean: Whether the game block has hit the ground or not.
        """
        x = 0
        y = 0
        #Gets the lowest value
        for i in range(4):
            for j in range(4):
                if self.image[i][j] == 1:
                    if i > y:
                        y = i
        if (y + self.y) >= 19:
            return True
        else:
            return False