import curses 
import datetime
import random
import sys


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

    current_figure=figures[random.randint(0, 6)]
    next_figure=figures[random.randint(0, 6)]

    screen = None

    scene = ''
    menu_lst=['    TETRIS', 'Start new game', ' Top results  ', '     Exit     ']
    menu_item=1
    records_lst=[' Back ', ' Clear results ']
    records_item=0

    # create glass
    def __init__(self):
        self.glass = [[0 for x in range(12)] for x in range(20)]

        screen = None

        self.scene='menu'

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
        self.count_lines = 0
        self.speed = 500000

    ### screen
    def has_screen_changed(self):

        current_dimensions = self.screen.getmaxyx()

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
                self.screen.addstr('Terminal too small', curses.color_pair(16))
            elif self.screen.getmaxyx()[0]<3 or self.screen.getmaxyx()[1]<20:
                self.screen.move(self.screen.getmaxyx()[0]//2, self.screen.getmaxyx()[1]//2-3)
                self.screen.addstr('Error', curses.color_pair(16))
            else:
                self.screen.addstr(0, 0, ' ')

            

        if current_dimensions != self.screen_dimensions:
            self.screen_dimensions = current_dimensions
            self.screen.clear()

    # draw scene
    def draw(self):
        self.left_corner = (self.screen.getmaxyx()[1])//2 - 36 # ширина
        self.top_corner = (self.screen.getmaxyx()[0])//2 - 14 # высота
        self.has_screen_changed()

        if self.scene == 'menu':
            self.draw_menu()
        elif self.scene == 'game':
            self.draw_game()
        elif self.scene == 'records':
            self.draw_records()

        self.screen.refresh()


    ### draw menu
    def draw_menu(self):
        for i in range(4):
            if self.menu_item==i and self.menu_item!=0:
                self.screen.addstr((self.screen.getmaxyx()[0] - 7+i*4) // 2, (self.screen.getmaxyx()[1]-14) // 2, self.menu_lst[i], curses.color_pair(112))
            else:
                self.screen.addstr((self.screen.getmaxyx()[0] - 7+i*4) // 2, (self.screen.getmaxyx()[1]-14) // 2, self.menu_lst[i])


    ### draw game
    def draw_game(self):

        # drawing the glass
        for i in range(len(self.glass)):
            for j in range(len(self.glass[i])):
                self.screen.move(self.top_corner+5+i, self.left_corner+10+j*2)
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
                self.screen.move(self.top_corner+5+self.x+i, self.left_corner+self.y*2+10+j*2)
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

        # next figure
        self.screen.move(self.top_corner+5, self.left_corner+50)
        self.screen.addstr('Next figure: ', curses.color_pair(12))

        for i in range(4):
            for j in range(4):
                self.screen.move(self.top_corner+8+i, self.left_corner+53+j*2)
                self.screen.addstr('  ', curses.color_pair(10))

        for i in range(len(self.next_figure)):
            for j in range(len(self.next_figure[i])):
                self.screen.move(self.top_corner+8+i, self.left_corner+53+j*2)
                if self.next_figure[i][j]==1:
                    self.screen.addstr('  ', curses.color_pair(1))
                elif self.next_figure[i][j]==2:
                    self.screen.addstr('  ', curses.color_pair(2))
                elif self.next_figure[i][j]==3:
                    self.screen.addstr('  ', curses.color_pair(3))
                elif self.next_figure[i][j]==4:
                    self.screen.addstr('  ', curses.color_pair(4))
                elif self.next_figure[i][j]==5:
                    self.screen.addstr('  ', curses.color_pair(5))
                elif self.next_figure[i][j]==6:
                    self.screen.addstr('  ', curses.color_pair(6))
                elif self.next_figure[i][j]==7:
                    self.screen.addstr('  ', curses.color_pair(14))
                elif self.next_figure[i][j]==8:
                    self.screen.addstr('  ', curses.color_pair(15))

        # lines
        self.screen.move(self.top_corner+15, self.left_corner+51)
        self.screen.addstr('Lines: '+str(self.count_lines), curses.color_pair(11))

    ### draw records
    def draw_records(self):
        pass
    # global screen_dimensions
    # global ttop
    
    # has_screen_changed(screen_results)
    
    # left_corner = (screen_dimensions[1]) // 2 - 14
    # top_corner = (screen_dimensions[0]) // 2 - 12

    # screen_results.addstr(top_corner, left_corner+8, '  Top results')

    # # выводим список рекордов
    # for i in range(1, len(ttop)+1):
    #     j=i-1
    #     screen_results.addstr(top_corner+2*i, left_corner+2, str(i)+' '+ttop[j][0])
    #     screen_results.addstr(top_corner+2*i, left_corner+4+len(ttop[j][0])-1+len(str(j)), '-'*((24-len(ttop[j][0])+1-len(str(j)))+3))
    #     screen_results.addstr(top_corner+2*i, left_corner+4+24+3-len(str(ttop[j][1])), str(ttop[j][1]))
    # # back, clear results 
    # for i in range(2):
    #     if res_num==i:
    #         # выбранная кнопка
    #         screen_results.addstr(top_corner+2+len(ttop)*2, left_corner+18*i, res_lst[i], curses.color_pair(112))
    #     else:
    #         screen_results.addstr(top_corner+2+len(ttop)*2, left_corner+18*i, res_lst[i])

    # screen_results.refresh()




    ### remove lines
    def remove_lines(self):
        for i in range(len(self.glass)-1):
            gaps_in_line=False

            for j in self.glass[i]:
                if j==0:
                    gaps_in_line=True

            if gaps_in_line==False:
                for e in range(i, 0, -1):
                    self.glass[e][1:-1]=self.glass[e-1][1:-1]
                self.count_lines+=1
                self.speed = 500000**(1-0.0005*self.count_lines)


    ### save figure to glass
    def save_figure(self):
        for i in range(len(self.current_figure)):
            for j in range(len(self.current_figure[i])):
                if self.current_figure[i][j]!=0:
                    self.glass[self.x+i][self.y+j]=self.current_figure[i][j]

        self.current_figure=self.next_figure
        self.next_figure=self.figures[random.randint(0, 6)]
    
        self.x, self.y = 0, 5
        self.timer=datetime.datetime.now()

        ### game over
        if self.__can_move(self.x, self.y, self.current_figure)==False:
            self.game_over()


    ### GAME OVER
    def game_over(self):
        box1 = curses.newwin(6, 21, self.top_corner+10, self.left_corner+28)
        box1.box()
        box1.bkgd(' ', curses.color_pair(16))    

        box1.addstr(1, 6, 'Game over', curses.color_pair(16))
        box1.addstr(3, 1, 'Type "y" to restart')
        box1.addstr(4, 3, 'or "n" to quit')
        box1.refresh()

        while True:
            key=self.screen.getch()

            if key==ord('y'):
                self.screen.clear()
                self.screen.refresh()
                self.__init__()
                break
            elif key==ord('n') or key==ord('q'):
                self.screen.clear()
                self.screen.refresh()
                sys.exit(0)
                break

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

        if self.scene == 'game':

            if (datetime.datetime.now()-self.timer).microseconds>=500000:
                self.timer=datetime.datetime.now()
                self.move_figure('tick')

            self.remove_lines()

    ### pause
    def pause(self):
        self.screen.nodelay(False)

        key=0
        while key!=ord('p'):
            box2 = curses.newwin(3, 10, self.screen.getmaxyx()[0]//2, self.screen.getmaxyx()[1]//2)
            box2.box()
            box2.bkgd(' ', curses.color_pair(13))    
            box2.addstr(1, 2, 'Paused', curses.color_pair(13))
            box2.refresh()

            key=self.screen.getch()

            self.draw()

        box2.bkgd(' ', curses.color_pair(0))
        box2.clear()
        box2.refresh()

        self.screen.nodelay(True)


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



    def getinput(self):
        key=self.screen.getch()

        if self.scene == 'game':

            if key==curses.KEY_LEFT:
                self.move_figure('left')
            elif key==curses.KEY_RIGHT:
                self.move_figure('right')
            elif key==curses.KEY_DOWN:
                self.move_figure('drop')
            elif key==curses.KEY_UP:
                self.move_figure('rotate')
            elif key==ord('p'):
                self.pause()
            elif key==ord('q'):
                self.screen.clear()
                self.scene='menu'

        elif self.scene == 'menu':

            if key==ord('q'):
                pass
            elif key==curses.KEY_UP:
                self.menu_item-=1
                if self.menu_item==0:
                    self.menu_item=3
            elif key==curses.KEY_DOWN:
                self.menu_item+=1
                if self.menu_item==4:
                    self.menu_item=1
            elif key == curses.KEY_ENTER or key == 10 or key == 13:
                if self.menu_item==3:       # exit
                    sys.exit(0)
                elif self.menu_item==1:     # start
                    self.screen.clear()
                    self.scene='game' 
                else:                        # top results
                    self.screen.clear()
                    self.scene='records'

        elif self.scene == 'records':

            if key==curses.KEY_RIGHT:
                self.records_item+=1
            elif key==curses.KEY_LEFT:
                self.records_item-=1
            elif key == curses.KEY_ENTER or key == 10 or key == 13:
                if self.records_item==0: # back to menu
                    self.screen.clear()
                    self.scene='menu'
                elif self.records_item==1: # clear records
                    self.screen.clear()
                    ### ... clear records file!!!!!

            if self.records_item==-1:
                self.records_item=1
            elif self.records_item==2:
                self.records_item=0


        










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
    curses.init_pair(11, curses.COLOR_GREEN, curses.COLOR_BLACK) # lines
    curses.init_pair(12, curses.COLOR_YELLOW, curses.COLOR_BLACK) # next figure
    curses.init_pair(13, curses.COLOR_BLACK, 8) # pause
    curses.init_pair(14, 126, 126)
    curses.init_pair(15, 154, 154)
    curses.init_pair(16, 15, 9) # game over
    curses.init_pair(112, curses.COLOR_BLACK, curses.COLOR_WHITE) # menu 



    tetris.screen = screen

    tetris.x = 0 # up, down
    tetris.y = 5 # left, right
    tetris.figure = 2

    screen.nodelay(True)

    tetris.screen_dimensions=tetris.screen.getmaxyx()

    while True:


        tetris.getinput()

        key=screen.getch()


        tetris.draw()
        tetris.tick()








########################################################


tetris = Tetris()



curses.wrapper(run_game)



























