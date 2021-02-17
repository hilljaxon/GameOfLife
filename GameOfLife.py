from time import sleep
import curses
from random import randint
from copy import deepcopy
from sys import argv


class GameOfLife:
    def __setup(self, screen):
        # Get the dimensions
        self.y, self.x = screen.getmaxyx()
        self.x = self.x//2
        self.y = self.y-5
        self.genNum = int(argv[1]) if len(argv)>1 else 1000
        
    def __init__(self,screen):
        self.__setup(screen)
        # set up the board with a blank slate
        self.board = [[' ' for j in range(self.y)] for i in range(self.x)]
        self.nextBoard = [[' ' for j in range(self.x)] for i in range(self.x)]
        # for i in range(22):
        #     temp = []
        #     for j in range(22):
        #         temp.append(" ")
        #     self.board.append(temp)
        # testing arrangement 
        self.transplant()
        # make 1/3 living cells
        self.populate()

        self.showBoard(screen)


    def populate(self):
        '''randomly make 1/3 of the cells living'''
        for i in range(1, self.x - 1):
            for j in range(1, self.y - 1):
                self.board[i][j] = 'X' if randint(1, 3) == 3 else ' '

    def transplant(self):
        '''testing arrangements'''
        self.board[10][8:11] = ['X', 'X', 'X']  # "should" blink back and forth

    def update(self):  # nextgen
        '''calculates the next generation and updates to that new generation'''
        # newgeneration = [...board...]
        for i in range(1, self.x - 1):
            for j in range(1, self.y - 1):
                # count all the neighbors
                # apply rules of the Game to that cell to determine alive or dead
                # assign next gen to be alive or dead
                self.nextBoard[i][j] = self.isAlive(i, j)  # returns an X or ' '

        self.board = deepcopy(self.nextBoard)
    
    def isAlive(self, x, y):
        # living cells die if under or over populated
        count = self.scan(x,y)
        if self.board[x][y] == 'X':  # aka, alive
            if count < 2:
                return ' '
            elif count > 3:
                return ' '
            else:
                return 'X'
        else:  # dead cells come to life if 3 neighbors
            if count == 3:
                return 'X'
            else:
                return ' '


    def scan(self, x, y): # add neighbors
        '''helper function for update
           Looks at all the neighbors and counts all living cells
           Then, returns the new status of this cell based on that info'''
        count = 0
        for i in range(x - 1, x + 2): # x-1,x,x+1
            for j in range(y - 1, y + 2):  # y-1,y,y+1
                # don't count yourself!!! (when in middle)
                if (not (i == x and j == y)) and self.board[i][j] == 'X':
                    count += 1
        return count

    def showBoard(self, screen):
        '''Black magic and witchcraft
           Provides a function to be used by curses wrapper
           The wrapper give a screen we can write on and handels all the upkeep'''
        curses.curs_set(0)  # get rid of the blinking curser
        for k in range(self.genNum):  # num generations
            for i in range(1, self.x-1):
                for j in range(1, self.y-1):
                    screen.addstr(j, i*2, self.board[i][j])  # write the board cells (with spaces in between, i*2)
            
            screen.addstr(self.y+1, self.x-10, f"Generation: {k + 1}")  # write down the label
            screen.refresh()  # print our work to the console
            self.update()  # load the next generation
            sleep(.3)  # delay


# Main

curses.wrapper(GameOfLife)
