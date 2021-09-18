import curses 
import datetime
import random


class Tetris:

    figures=[[[0,0,0],
              [2,2,2],
              [0,2,0]],
             [[0,0,0],
              [3,3,3],
              [3,0,0]],
             [[0,0,0],
              [4,4,4],
              [0,0,4]],
             [[5,5],
              [5,5]],
             [[0,0,0,0],
              [0,0,0,0],
              [6,6,6,6],
              [0,0,0,0]],
             [[0,0,0],
              [0,7,7],
              [7,7,0]],
             [[0,0,0],
              [8,8,0],
              [0,8,8]] 
              ]
    x = 0 # up, down
    y = 0 # left, right

    figure=0
    current_figure=figures[figure]
    

    screen = None
    

    # create glass
    def __init__(self):
        self.glass = [[0 for x in range(12)] for x in range(20)]

        screen = None

        # create borders
        for i in range(len(self.glass)):

            if i<=18:

                for j in range(len(self.glass[i])):
                    if j==0 or j==11:
                        self.glass[i][j]=1

            else:
                for j in range(len(self.glass[i])):
                    self.glass[i][j]=1

        self.timer = datetime.datetime.now()
        
        # self.glass[10][5] = 1

    ### screen
    def has_screen_changed(self):

        current_dimensions = self.screen.getmaxyx()

        curses.init_pair(50, 15, 9)

        while self.screen.getmaxyx()[0]<30 or self.screen.getmaxyx()[1]<55:
            current_dimensions = self.screen.getmaxyx()
            
            key=self.screen.getch()
            if key==ord('q'):
                self.screen.clear()
                exit(0)

            if self.screen_dimensions != current_dimensions:
                self.screen_dimensions = current_dimensions
                self.screen.clear()

            if self.screen.getmaxyx()[0]<30 or self.screen.getmaxyx()[1]<55:
                self.screen.move(self.screen.getmaxyx()[0]//2, self.screen.getmaxyx()[1]//2-9)
                self.screen.addstr('Terminal too small', curses.color_pair(50))
            elif self.screen.getmaxyx()[0]<3 or self.screen.getmaxyx()[1]<20:
                self.screen.move(self.screen.getmaxyx()[0]//2, self.screen.getmaxyx()[1]//2-3)
                self.screen.addstr('Error', curses.color_pair(50))
            else:
                self.screen.addstr(0, 0, ' ')

            

        if current_dimensions != self.screen_dimensions:
            self.screen_dimensions = current_dimensions
            self.screen.clear()

    # draw scene
    def draw(self):
        self.has_screen_changed()

        left_corner = (self.screen.getmaxyx()[1])//2 - 36 # ширина
        top_corner = (self.screen.getmaxyx()[0])//2 - 14 # высота

        # drawing the glass
        for i in range(len(self.glass)):
            for j in range(len(self.glass[i])):
                self.screen.move(top_corner+5+i, left_corner+10+j*2)
                if self.glass[i][j]==1:
                    self.screen.addstr('  ', curses.color_pair(1))
                elif self.glass[i][j]==2:
                    self.screen.addstr('  ', curses.color_pair(2))
                elif self.glass[i][j]==3:
                    self.screen.addstr('  ', curses.color_pair(3))
                elif self.glass[i][j]==4:
                    self.screen.addstr('  ', curses.color_pair(4))
                elif self.glass[i][j]==5:
                    self.screen.addstr('  ', curses.color_pair(5))
                elif self.glass[i][j]==6:
                    self.screen.addstr('  ', curses.color_pair(6))
                elif self.glass[i][j]==7:
                    self.screen.addstr('  ', curses.color_pair(14))
                elif self.glass[i][j]==8:
                    self.screen.addstr('  ', curses.color_pair(15))
                else:
                    self.screen.addstr('  ', curses.color_pair(10))

        # drawing current figure
        for i in range(len(self.current_figure)):
            for j in range(len(self.current_figure[i])):
                self.screen.move(top_corner+5+self.x+i, left_corner+self.y*2+10+j*2)
                if self.current_figure[i][j]==1:
                    self.screen.addstr('  ', curses.color_pair(1))
                elif self.current_figure[i][j]==2:
                    self.screen.addstr('  ', curses.color_pair(2))
                elif self.current_figure[i][j]==3:
                    self.screen.addstr('  ', curses.color_pair(3))
                elif self.current_figure[i][j]==4:
                    self.screen.addstr('  ', curses.color_pair(4))
                elif self.current_figure[i][j]==5:
                    self.screen.addstr('  ', curses.color_pair(5))
                elif self.current_figure[i][j]==6:
                    self.screen.addstr('  ', curses.color_pair(6))
                elif self.current_figure[i][j]==7:
                    self.screen.addstr('  ', curses.color_pair(14))
                elif self.current_figure[i][j]==8:
                    self.screen.addstr('  ', curses.color_pair(15))


        self.screen.refresh()


    ### remove lines
    def remove_lines(self):

        pass
    # global count_lines
    # global speed

    # for i in range(len(m)-1):
    #     gaps_in_line=False

    #     for j in m[i]:
    #         if j==0:
    #             gaps_in_line=True

    #     if gaps_in_line==False:
    #         for e in range(i, 0, -1):
    #             m[e][1:-1]=m[e-1][1:-1]
    #         count_lines+=1
    #         speed = 500000**(1-0.0005*count_lines) 
    # return m

    ### save figure to glass
    def save_figure(self):
        for i in range(len(self.current_figure)):
            for j in range(len(self.current_figure[i])):
                if self.current_figure[i][j]!=0:
                    self.glass[self.x+i][self.y+j]=self.current_figure[i][j]
        self.figure=random.randint(0, 6)
        self.current_figure=self.figures[self.figure]
        self.x, self.y = 0, 5
        self.timer=datetime.datetime.now()

    ### can move
    def __can_move(self, new_x, new_y, figure):
        # if figure can move
        for i in range(len(figure)):
                for j in range(len(figure[i])):
                    if figure[i][j]!=0:
                        if self.glass[new_x+i][new_y+j]!=0:
                            return False
        return True

    ### drop
    def drop(self):
        new_x=self.x
        while self.__can_move(new_x+1, self.y, self.current_figure)==True:
            new_x+=1
        return new_x

    ### timer
    def tick(self):
        # this moves the figure down if the timer is expired

        if (datetime.datetime.now()-self.timer).microseconds>=500000:
            self.timer=datetime.datetime.now()
            self.move_figure('tick')

        return

    ### moving current figure
    def move_figure(self, command):
        # Commands:
        #  'left' - move left
        #  'right' - move right
        #  'drop' - drop - full drop
        #  'tick' - move the figure down on a timer tick
        #  'rotate' - rotate

        new_x, new_y, new_figure=self.x, self.y, self.current_figure

        if command=='left':
            if self.__can_move(new_x, new_y-1, new_figure) == True:
                self.y-=1

        elif command=='right':
            if self.__can_move(new_x, new_y+1, new_figure) == True:
                self.y+=1

        elif command=='drop':
            self.x=self.drop()

        elif command=='tick':
            if self.__can_move(new_x+1, new_y, new_figure) == True:
                self.x+=1
            else:
                self.save_figure()


        elif command=='rotate':
            new_figure=[[0 for _ in range(len(self.current_figure[0]))] for _ in range(len(self.current_figure))]
            for i in range(len(self.current_figure)):
                for j in range(len(self.current_figure[i])):
                    new_figure[j][len(self.current_figure[i])-i-1]=self.current_figure[i][j]

            if self.__can_move(new_x, new_y, new_figure) == True:
                self.current_figure=new_figure











def run_game(screen):

    # colors
    curses.curs_set(0)
    curses.start_color()
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_WHITE)
    curses.init_pair(2, curses.COLOR_BLUE, curses.COLOR_BLUE)
    curses.init_pair(3, curses.COLOR_CYAN, curses.COLOR_CYAN)
    curses.init_pair(4, 11, 11)
    curses.init_pair(5, curses.COLOR_RED, curses.COLOR_RED)
    curses.init_pair(6, curses.COLOR_GREEN, curses.COLOR_GREEN)
    curses.init_pair(14, 126, 126)
    curses.init_pair(15, 154, 154)



    tetris.screen = screen

    tetris.x = 0 # up, down
    tetris.y = 5 # left, right
    tetris.figure = 2

    screen.nodelay(True)

    tetris.screen_dimensions=tetris.screen.getmaxyx()

    while True:
        key=screen.getch()

        if key==curses.KEY_LEFT:
            tetris.move_figure('left')
        elif key==curses.KEY_RIGHT:
            tetris.move_figure('right')
        elif key==curses.KEY_DOWN:
            tetris.move_figure('drop')
        elif key==curses.KEY_UP:
            tetris.move_figure('rotate')

        # command = readKey()

        # if command != '':
        #     tetris.move_figure(command)


        tetris.draw()
        tetris.tick()

        # for i in range(4):
        #     
        #     screen.getch()
        #     tetris.move_figure('drop')







########################################################


tetris = Tetris()



curses.wrapper(run_game)



























