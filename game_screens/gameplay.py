import pygame
import copy

from components.deadblock import Deadblock
from components.gameblock import Gameblock

class GamePlay():
    """ The Tetris gameplay class.
    """
    def __init__(self,screen,width,height,multiplier):
        """ Initializing GamePlay class.

        Args:
            screen (pygame.display): The screen the game is projected on.
            width (int): The block width of game board matrix.
            height (int): The block height of game board matrix.
            multiplier (int): The size of each block on the game board matrix.
        """

        #Initializing game dependent variables.
        self.WIDTH = width
        self.HEIGHT = height
        self.MULTIPLIER = multiplier
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.running = True
        self.speed = 200
        self.score = 0
        self.font = pygame.font.Font('freesansbold.ttf', 32)
        self.one_save_per_round = False

        #Playing game music
        pygame.mixer.music.load('./assets/tetris_music.mp3')
        pygame.mixer.music.set_volume(0.1)
        pygame.mixer.music.play(-1)   


        #Making the gameboard that will store all of the dead pieces
        self.gameboard =[]
        for i in range(self.HEIGHT):
            temp = []
            for j in range(self.WIDTH):
                temp.append(0)
            self.gameboard.append(temp)

        #Making the game pieces
        self.piece = Gameblock(4,-4,self.screen,self.MULTIPLIER)
        self.needs_to_change = False

        #Dead pieces
        self.dead_pieces = []

        #Saved piece
        self.saved_piece = 0


    def run(self):
        """ The main game loop that runs Tetris.
        """
        while self.running:
            print(self.piece.y)
            
            #Displaying background
            self.screen.fill((0,0,0))
            self.draw_grid()
            pygame.draw.rect(self.screen,(0,0,0),(500,0,200,1000))
            self.game_menu()
            pygame.draw.line(self.screen,(255,255,255),(self.WIDTH*self.MULTIPLIER,0),(self.WIDTH*self.MULTIPLIER,self.HEIGHT* self.MULTIPLIER))
            self.display_deadpieces()
        

            #Checking if user exited window and check for movement
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    if (event.key == pygame.K_d or event.key == pygame.K_RIGHT) and self.side_movement(True):
                        self.piece.x += 1
                    if (event.key == pygame.K_a or event.key == pygame.K_LEFT) and self.side_movement(False):
                        self.piece.x -=1
                    if event.key == pygame.K_w or event.key == pygame.K_UP:
                        self.piece.flip()
                    if (event.key == pygame.K_s or event.key == pygame.K_DOWN) and self.piece.y <= 19:
                        self.piece.y +=1 
                        self.piece.counter = 0
                    if event.key == pygame.K_SPACE and self.piece.y < 19:
                        self.hardfall()
                    if event.key == pygame.K_LSHIFT:
                        self.save_piece()

            #Check for collisions
            self.collision_check(False)
             
            #Checking for full rows
            self.clear_lines()
    
            #Displaying game pieces
            self.piece.display_block()
            self.piece.update()

            #Checking if player lost
            self.lost_game()

            #Updating game screen
            pygame.display.flip()
            self.clock.tick(self.speed)
            

    def draw_grid(self):
        """ Draws the lines that make up the gameboard matrix.
        """
        for i in range(self.WIDTH + 1):
            if i != 0:
                pygame.draw.line(self.screen,(255,255,255),(self.MULTIPLIER*i,0),(self.MULTIPLIER*i,self.HEIGHT*self.MULTIPLIER))

        for i in range(self.HEIGHT):
            pygame.draw.line(self.screen,(255,255,255),(0,self.MULTIPLIER*i),(self.WIDTH *self.MULTIPLIER,self.MULTIPLIER*i))


    def display_deadpieces(self):
        """ Displays the dead game pieces on the screen.
        """
        for x in self.dead_pieces:
            x.display_block()


    def is_below(self):
        """ Checks if a block is below the game piece.

        Returns:
            boolean: Returns True if there is a block below the game piece.
        """
        for y in range(4):
            for x in range(4):
                if self.piece.image[y][x] == 1:
                    vertical = self.piece.y + y
                    horizontal = self.piece.x + x
                    if vertical + 1 <= 19 and horizontal < 10:
                        if self.gameboard[vertical + 1][horizontal] != 0:
                            return True
        
        return False


    def collision_check(self,ishardfall):
        """ Checks if a block or the ground is below game piece.

        Args:
            ishardfall (boolean): Indicates if function is being used for hardfall.

        Returns:
            boolean: Returns true if game block collided.
        """
        if self.is_below() or self.piece.hit_ground():

            #This gives the user time to change their position once they have collided
            if ishardfall == False:
                if self.last_chance() == False:
                    print("False")
                    return False

            for y in range(4):
                for x in range(4):
                    if self.piece.image[y][x] == 1:
                        #Coordinates on board
                        vertical = self.piece.y + y
                        horizontal = self.piece.x + x

                        self.dead_pieces.append(Deadblock((horizontal),(vertical),self.piece.color,self.screen))
                        self.gameboard[vertical][horizontal] = self.piece.color
            
            #Making new game piece
            self.one_save_per_round = False
            self.piece = Gameblock(4,-4,self.screen,self.MULTIPLIER)
            self.piece.x = 4
            self.piece.y = -1
            return True
        else:
            return False
    

    def print_dead_grid(self):
        """ Prints a command prop representation of the gameboard(Used for debugging).
        """
        print("------------------")
        for i in range(self.HEIGHT):
            print(self.gameboard[i])
        print("------------------")


    def hardfall(self):
        """ Drops piece to the bottom of the board.
        """
        while self.collision_check(True) == False:
            self.piece.y += 1
    

    def side_movement(self, right):
        """ Determines if a piece can move sideways

        Args:
            right (boolean): True if player is trying to move to the right.

        Returns:
            boolean: Returns True if the player can move to the side.
        """
        for i in range(4):
            for j in range(4):
                if self.piece.image[i][j] == 1:
                    #Gets the actual x, y coordinates on the board
                    y = i + self.piece.y
                    x = j + self.piece.x

                    if right:
                        if x == 9:
                            return False
                        #Checks if theres a dead block to the right
                        if self.gameboard[y][x+1] != 0:
                            return False
                    else:
                        if x == 0:
                            return False
                        #Checks if theres a dead block to the left
                        if self.gameboard[y][x-1] != 0:
                            return False

        return True


    def clear_lines(self):
        """ Checks for full rows and clears them.
        """

        change = True

        while change:
            change = False
            for y in range(self.HEIGHT):
                counter = 0
                for x in range(self.WIDTH):
                    if self.gameboard[y][x] != 0:
                        counter += 1
                if counter == 10:
                    change = True
                    self.score += 10
                    if self.speed < 500:
                        self.speed += 2
                    for i in range(y):
                        for j in range(self.WIDTH):
                            self.gameboard[y - i][j] = self.gameboard[y - i - 1][j]
                
        self.convert()

   
    def convert(self):
        """ Converts the gameboard matrix into dead blocks.
        """
        newlist = []

        for i in range(self.HEIGHT):
            for j in range(self.WIDTH):
                if self.gameboard[i][j] != 0:
                    newlist.append(Deadblock(j,i,self.gameboard[i][j],self.screen))

        self.dead_pieces = newlist


    def game_menu(self):
        """ Displays the score and saved piece image on right side of game window.
        """
        points = self.font.render("SCORE", True, (255, 255, 255))
        score = self.font.render(f'{self.score}', True, (255, 255, 255))
        self.screen.blit(score,(580,90))
        self.screen.blit(points,(540,30))

        saved_text = self.font.render("Saved", True, (255, 255, 255))
        self.screen.blit(saved_text,(540,150))

        if self.saved_piece != 0:
            t = copy.copy(self.saved_piece)
            t.x = 57
            t.y = 25
            t.multiplier = 10
            t.display_block()
   
  
    def save_piece(self):
        """ Saves a piece in to storage so that it can be used upon user request.
        """

        #Save the piece cause empty
        if self.saved_piece == 0 and self.one_save_per_round == False:
            self.saved_piece = copy.copy(self.piece)
            x = (self.piece.x)
            y = (self.piece.y)
            self.piece = Gameblock(x,y, self.screen,self.MULTIPLIER)
            self.piece.x = x
            self.piece.y = y
        
        #Unload the piece
        elif self.one_save_per_round == False:
            x = (self.piece.x)
            y = (self.piece.y)

            self.piece = self.saved_piece
            self.piece.x = x
            self.piece.y = y
            self.saved_piece = 0

        self.one_save_per_round = True


    def last_chance(self):
        """ Gives the player a second to continue moving block once it has collided.
        """
    
        timer = 0

        #Displaying background again to cover old game block
        self.screen.fill((0,0,0))
        self.draw_grid()
        pygame.draw.rect(self.screen,(0,0,0),(500,0,200,1000))
        self.game_menu()
        pygame.draw.line(self.screen,(255,255,255),(self.WIDTH*self.MULTIPLIER,0),(self.WIDTH*self.MULTIPLIER,self.HEIGHT* self.MULTIPLIER))
        self.display_deadpieces()

        while timer < 40:

            #Displaying background
            self.screen.fill((0,0,0))
            self.draw_grid()
            pygame.draw.rect(self.screen,(0,0,0),(500,0,200,1000))
            self.game_menu()
            pygame.draw.line(self.screen,(255,255,255),(self.WIDTH*self.MULTIPLIER,0),(self.WIDTH*self.MULTIPLIER,self.HEIGHT* self.MULTIPLIER))
            self.display_deadpieces()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    if (event.key == pygame.K_d or event.key == pygame.K_RIGHT) and self.side_movement(True):
                        self.piece.x += 1
                        timer = 0
                    if (event.key == pygame.K_a or event.key == pygame.K_LEFT) and self.side_movement(False):
                        self.piece.x -=1
                        timer = 0
                    if event.key == pygame.K_SPACE and self.piece.y < 19:
                        timer = 60
                    
            #Displaying game pieces
            self.piece.display_block()

            #Updating game screen
            pygame.display.flip()
            self.clock.tick(60)
            timer += 1
    
        self.piece.x = self.piece.x
        self.piece.y = self.piece.y
        self.collision_check(True)
        if self.is_below():
            return True
        else: 
            return False
        
        
    def lost_game(self):
        """Ends the game when player loses
        """
        for block in self.dead_pieces:
            if block.y == 0:
                print("GAME OVER")
                pygame.quit()
                exit()
