import datetime
import random
import curses
import copy
### FUNCTIONS


def create_borders(m):
    matrix=m
    for i in range(len(matrix)):

        if i<=18:

            for j in range(len(matrix[i])):
                if j==0 or j==11:
                    matrix[i][j]=1

        else:
            for j in range(len(matrix[i])):
                matrix[i][j]=1
    return matrix




def render_scene(sdr, m, current_figure, x, y): # copy matrix + figure
    global next_figure
    global count_lines
    global screen_dimensions

    stdscr=sdr
    stdscr.move(0,0)

    stdscr.addstr(1, 0, str(screen_dimensions))
    has_screen_changed(stdscr)

    
    if screen_dimensions[0]<23 or screen_dimensions[1]<55:
        stdscr.move(screen_dimensions[0]//2, screen_dimensions[1]//2)
        stdscr.addstr('Error', curses.color_pair(50))
    else:

        left_corner = (screen_dimensions[1])//2 - 36
        top_corner = (screen_dimensions[0])//2 - 14
        # maxyx=current_terminal_size
        # maxx=int(maxyx[1]/2-38) # по горизонтали ## min 55
        # maxy=int(maxyx[0]/2-16) # по вертикали ## min 23


        scene = copy.deepcopy(m)


        # copying figure into scene
        for i in range(len(current_figure)): 
            for j in range(len(current_figure[i])):
                if current_figure[i][j]!=0:
                    scene[x+i][y+j] = current_figure[i][j]


    
        

        curses.init_pair(10, curses.COLOR_BLACK, curses.COLOR_BLACK)
        curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_WHITE)
        curses.init_pair(2, curses.COLOR_BLUE, curses.COLOR_BLUE)
        curses.init_pair(3, curses.COLOR_CYAN, curses.COLOR_CYAN)
        curses.init_pair(4, 11, 11)
        curses.init_pair(5, curses.COLOR_RED, curses.COLOR_RED)
        curses.init_pair(6, curses.COLOR_GREEN, curses.COLOR_GREEN)
        curses.init_pair(11, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(12, curses.COLOR_YELLOW, curses.COLOR_BLACK)
        curses.init_pair(14, 126, 126)
        curses.init_pair(15, 154, 154)


        curses.init_pair(13, curses.COLOR_BLACK, 8) # pause
        curses.init_pair(50, 15, 9) # game over

        #drawing the scene
        for i in range(len(scene)):
            for j in range(len(scene[i])):

                    stdscr.move(top_corner+5+i, left_corner+10+j*2)
                    if scene[i][j]==1:
                        stdscr.addstr('  ', curses.color_pair(1))
                    elif scene[i][j]==2:
                        stdscr.addstr('  ', curses.color_pair(2))
                    elif scene[i][j]==3:
                        stdscr.addstr('  ', curses.color_pair(3))
                    elif scene[i][j]==4:
                        stdscr.addstr('  ', curses.color_pair(4))
                    elif scene[i][j]==5:
                        stdscr.addstr('  ', curses.color_pair(5))
                    elif scene[i][j]==6:
                        stdscr.addstr('  ', curses.color_pair(6))
                    elif scene[i][j]==7:
                        stdscr.addstr('  ', curses.color_pair(14))
                    elif scene[i][j]==8:
                        stdscr.addstr('  ', curses.color_pair(15))
                    else:
                        stdscr.addstr('  ', curses.color_pair(10))

        # next figure
        stdscr.move(top_corner+5, left_corner+50)
        stdscr.addstr('Next figure: ', curses.color_pair(12))

        for i in range(4): 
            for j in range(4):
                stdscr.move(top_corner+8+i, left_corner+53+j*2)
                stdscr.addstr('  ', curses.color_pair(10))
                
        for i in range(len(next_figure)): 
            for j in range(len(next_figure[i])):
                    stdscr.move(top_corner+8+i, left_corner+53+j*2)
                    if next_figure[i][j]==1:
                        stdscr.addstr('  ', curses.color_pair(1))
                    elif next_figure[i][j]==2:
                        stdscr.addstr('  ', curses.color_pair(2))
                    elif next_figure[i][j]==3:
                        stdscr.addstr('  ', curses.color_pair(3))
                    elif next_figure[i][j]==4:
                        stdscr.addstr('  ', curses.color_pair(4))
                    elif next_figure[i][j]==5:
                        stdscr.addstr('  ', curses.color_pair(5))
                    elif next_figure[i][j]==6:
                        stdscr.addstr('  ', curses.color_pair(6))
                    elif next_figure[i][j]==7:
                        stdscr.addstr('  ', curses.color_pair(14))
                    elif next_figure[i][j]==8:
                        stdscr.addstr('  ', curses.color_pair(15))
                    else:
                        stdscr.addstr('  ', curses.color_pair(10))

        # lines
        stdscr.move(top_corner+15, left_corner+52)
        stdscr.addstr('Lines: '+str(count_lines), curses.color_pair(11))



    stdscr.refresh()







def has_screen_changed(screen):
    # Функция проверяет, изменился ли размер экрана, и, если да, очищает экран. 
    # Вызывающие функции должны подразумевать, что экран может быть очищен после вызова этой функции

    global screen_dimensions

    current_dimensions = screen.getmaxyx()

    if screen_dimensions != current_dimensions:
        screen_dimensions = current_dimensions
        screen.clear()

    while screen.getmaxyx()[0]<23 or screen.getmaxyx()[1]<55:
        screen.move(screen_dimensions[0]//2, screen_dimensions[1]//2)
        screen.addstr('Error', curses.color_pair(50))
        screen.refresh()





def move_figure(m, figure, new_x, new_y):
    #print(figure)
    #print(m)
    for i in range(len(figure)):
        for j in range(len(figure[i])):
            if figure[i][j]!=0:
                if m[new_x+i][new_y+j]!=0:
                    return False

    return True



def copy_to_matrix(m, figure, x, y):
    global t
    for i in range(len(figure)): 
        for j in range(len(figure[i])):
            if figure[i][j]!=0:
                m[x+i][y+j] = figure[i][j]
    t=datetime.datetime.now()
    return m


def rotate(m, figure, x, y):
    new_figure=[[0 for _ in range(len(figure[0]))] for _ in range(len(figure))]

    for i in range(len(figure)):
        for j in range(len(figure[i])):

            new_figure[j][len(figure[i])-i-1]=figure[i][j]

    if move_figure(m, new_figure, x, y)==True:
        return new_figure
    else:
        return figure


def remove_lines(m):
    global count_lines
    global speed

    for i in range(len(m)-1):
        gaps_in_line=False

        for j in m[i]:
            if j==0:
                gaps_in_line=True

        if gaps_in_line==False:
            for e in range(i, 0, -1):
                m[e][1:-1]=m[e-1][1:-1]
            count_lines+=1
            speed = 500000**(1-0.0005*count_lines) 
    return m



def full_drop(m, current_figure, drop_x, drop_y):
    matrix=m
    x=drop_x
    while move_figure(matrix, current_figure, x+1, drop_y)==True:
        x+=1
    return x
















### MAIN LOOP #########################################################################

def play_tetris(stdscr):
    global maxx
    global maxy
    global current_terminal_size
    global speed

    stdscr.clear()

    nodelay=True

    while nodelay==True:
        stdscr.nodelay(True)

        quit=False


        ### VARIABLES

        matrix =[[0 for x in range(12)] for x in range(20)]
        matrix = create_borders(matrix)

        #scene = [[0 for x in range(12)] for x in range(20)]

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
        x = 0
        y = 5

        global count_lines
        count_lines=0

        global next_figure
        current_figure=figures[random.randint(0, len(figures)-1)]
        next_figure=figures[random.randint(0, len(figures)-1)]

        global t
        t = datetime.datetime.now()

        curses.curs_set(0)

        speed = 500000

        curses.start_color()

        while True:
            current_terminal_size=stdscr.getmaxyx()

            if current_terminal_size[0]>=23 and current_terminal_size[1]>=55:                

                key=stdscr.getch()

                temp_x = x
                temp_y = y

                stdscr.move(0, 0)

                if key == curses.KEY_UP:
                    # stdscr.addstr("ROTATE")
                    current_figure=rotate(matrix, current_figure, x, y)

                elif key == curses.KEY_DOWN:
                    # stdscr.addstr("DOWN    ")
                    x=full_drop(matrix, current_figure, temp_x, temp_y)
                    #t=datetime.datetime.now()

                    
                elif key == curses.KEY_LEFT:
                    # stdscr.addstr("LEFT     ")
                    if move_figure(matrix, current_figure,temp_x, temp_y-1)==True:
                        x=temp_x
                        y=temp_y-1

                elif key == curses.KEY_RIGHT:
                    # stdscr.addstr("RIGHT    ")
                    if move_figure(matrix, current_figure,temp_x, temp_y+1)==True:
                        x=temp_x
                        y=temp_y+1

                elif key == ord('p'):
                    stdscr.nodelay(False)


                    box2 = curses.newwin(3, 10, maxy+12, maxx+36)
                    box2.box()
                    box2.bkgd(' ', curses.color_pair(13))    

                    box2.addstr(1, 2, 'Paused', curses.color_pair(13))
                    box2.refresh()


                    # stdscr.addstr('Paused', curses.color_pair(13))
                    # stdscr.refresh()

                    key=stdscr.getch()
                    while key!=ord('p'):
                        key=stdscr.getch()

                    box2.clear()
                    box2.bkgd(' ', curses.color_pair(0))
                    box2.refresh()

                    stdscr.nodelay(True)

                elif key == ord('q'):
                    quit=True                
                    break



                t2 = datetime.datetime.now()
                delta = t2 - t

                stdscr.addstr(str(speed)) 

                if delta.microseconds > speed:
                    t = t2

                    # надо опускать на шаг вниз

                    if move_figure(matrix, current_figure, x+1, y)==False:
                        matrix = copy_to_matrix(matrix, current_figure, x, y)
                        matrix = remove_lines(matrix)
                        x=0
                        y=5

                        current_figure=next_figure
                        next_figure=figures[random.randint(0, len(figures)-1)]

                        if move_figure(matrix, current_figure, x, y)==False: ### GAME OVER
                            

                            box1 = curses.newwin(6, 21, maxy+10, maxx+28)
                            box1.box()
                            box1.bkgd(' ', curses.color_pair(50))    

                            box1.addstr(1, 6, 'Game over', curses.color_pair(50))
                            box1.addstr(3, 1, 'Type "y" to restart')
                            box1.addstr(4, 3, 'or "n" to quit')
                            box1.refresh()


                            break
                    else:
                        x+=1

            else:
                key=stdscr.getch()
                if key==ord('q'):
                    quit=True
                    break


            render_scene(stdscr, matrix, current_figure, x, y)

        if quit==True:
            quit=False
            break

        stdscr.nodelay(False)
        key=stdscr.getkey()

        while True:
            if key=='y':
                stdscr.clear()
                stdscr.refresh()
                nodelay=True
                break
            elif key=='n' or key=='q':
                stdscr.clear()
                stdscr.refresh()
                nodelay=False
                break
            else:
                key=stdscr.getkey()
    
        


    stdscr.nodelay(True)






























########### MENU ##########################################################################

def render_results(screen_results, res_num, res_lst):
    global screen_dimensions
    global ttop

    has_screen_changed(screen_results)
    
    left_corner = (screen_dimensions[1]) // 2 - 14
    top_corner = (screen_dimensions[0]) // 2 - 12

    screen_results.addstr(top_corner, left_corner+8, '  Top results')

    # выводим список рекордов
    for i in range(1, len(ttop)+1):
        screen_results.addstr(top_corner+2*i, left_corner+2, str(i)+' '+ttop[i][0])
        screen_results.addstr(top_corner+2*i, left_corner+4+len(ttop[i][0]), '-'*((24-len(ttop[i][0]))+3))
        screen_results.addstr(top_corner+2*i, left_corner+4+24+3-len(ttop[i][1]), str(ttop[i][1]))
    # back, clear results 
    for i in range(2):
        if res_num==i:
            # выбранная кнопка
            screen_results.addstr(top_corner+2+len(ttop)*2, left_corner+18*i, res_lst[i], curses.color_pair(112))
        else:
            screen_results.addstr(top_corner+2+len(ttop)*2, left_corner+18*i, res_lst[i])

    screen_results.refresh()


def display_results(screen_results):
    global ttop
    global screen_dimensions

    has_screen_changed(screen_results)

    left_corner = (screen_dimensions[1]) // 2 - 10
    top_corner = (screen_dimensions[0]) // 2 - 23


    res_num=0
    res_lst=[' Back ', ' Clear results ']

  
    #screen_results.nodelay(False)

    screen_results.clear()


    render_results(screen_results, res_num, res_lst)

    while True:
        key=screen_results.getch()

        if key==curses.KEY_RIGHT:
            res_num+=1
        elif key==curses.KEY_LEFT:
            res_num-=1
        elif key == curses.KEY_ENTER or key == 10 or key == 13:
            if res_num==0: # back
                screen_results.clear()
                screen_results.nodelay(True)
                return
            elif res_num==1: # clear
                screen_results.clear()
                #screen_results.addstr(top_corner, left_corner, '  Top results')
                ttop={}

        if res_num==-1:
            res_num=1
        elif res_num==2:
            res_num=0

        render_results(screen_results, res_num, res_lst)










def render_menu(num, lst, screen):
    global screen_dimensions

    has_screen_changed(screen)

    left_corner = (screen_dimensions[1]-14) // 2
    top_corner = (screen_dimensions[0] - 7) // 2

    for i in range(4):
        if num==i and num!=0:
            screen.addstr(top_corner + i*2, left_corner, lst[i], curses.color_pair(112))
        else:
            screen.addstr(top_corner + i*2, left_corner, lst[i])

    screen.refresh()



def start_menu(screen):

    global screen_dimensions


    curses.start_color()
    curses.init_pair(112, curses.COLOR_BLACK, curses.COLOR_WHITE)
    curses.curs_set(0)

    screen.nodelay(True)

    screen_dimensions = screen.getmaxyx()


    lst=['    TETRIS', 'Start new game', ' Top results  ', '     Exit     ']
    num=1


    while True:    

        key=screen.getch()

        if key==ord('q'):
            break
        elif key==curses.KEY_UP:
            num-=1
            if num==0:
                num=3
        elif key==curses.KEY_DOWN:
            num+=1
            if num==4:
                num=1
        elif key == curses.KEY_ENTER or key == 10 or key == 13:
            if num==3: # exit
                break
            elif num==1: # start
                #screen.addstr(maxy, maxx, ('  '*10+'\n')*16)
                play_tetris(screen)

            else: # top results
                display_results(screen)  
                #screen.clear()


        render_menu(num, lst, screen)


ttop={ 1: ['Name', str(123)], 
        2: ['Name2',str(43)],
        3: ['Name3',str(10)],
        4: ['Name4',str(68)],
        5: ['Name',str(123)], 
        6: ['Name2',str(43)],
        7: ['Name3',str(10)],
        8: ['Name4',str(68)],
        9: ['Name3',str(10)],
        10: ['Name4',str(68)]
        }

curses.wrapper(start_menu)











