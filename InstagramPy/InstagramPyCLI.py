# The MIT License.
# Copyright (C) 2017 The Future Shell , DeathSec.
#
# @filename    : InstagramPyCLI.py
# @description : Simple and easy higher level api for Instagram-Py CLI Interface
#                using Python's ncurses library.
import curses
import threading
import AppInfo

class InstagramPyCLI:
    '''
        @progress_win -> Progress bar that will be repainted every time
        @status       -> Shows the current motive of the program
        @appInfo      -> JSON which contains all required information for
                         Instagram-Py
        @screen       -> Curses init object
        @progress_win -> progress bar window
        @started      -> Start Date and Time.
        @progress_title -> Title for @progress_win
        @total        -> Total passwords in file
        @tried        -> Finished passwords from the file
    '''
    status              = ""
    progress_win        = ""
    screen              = ""
    appInfo             = ""
    started             = ""
    progress_title      = ""
    total               = 1
    tried               = 1

    '''
        __init__ :
            - Updates @appInfo
            - Initialize curses to @screen

        @appInfo = @param info
        @started = @param started
        @total   = @param total

    '''

    def __init__(self , info , started , total):
        '''
            -- Update @appInfo --
        '''
        try:
            if info['name'] and info['author']: # try if we got the info's right
                self.appInfo = info
            else:
                self.appInfo = AppInfo.appInfo # or revert to default info!
        except:
                self.appInfo = AppInfo.appInfo

        self.started = started # the attack begin!
        self.total   = int(total)
        '''
            -- Update @screen to init curses --
        '''
        self.screen = curses.initscr()
        curses.noecho()
        curses.cbreak()
        if curses.has_colors():
            curses.start_color()
            curses.use_default_colors()
            curses.init_pair(1 , curses.COLOR_MAGENTA, curses.COLOR_WHITE) # NAME [COLOR MAGENTA]
            curses.init_pair(2 , curses.COLOR_GREEN, curses.COLOR_WHITE) # DD:HH:MM [COLOR GREEN]
            curses.init_pair(3 , curses.COLOR_WHITE, curses.COLOR_WHITE) # SPACE
            curses.init_pair(4 , curses.COLOR_BLUE, curses.COLOR_WHITE) # VERSION [COLOR BLUE]
            curses.init_pair(5 , curses.COLOR_YELLOW , 0)
            curses.init_pair(6 , curses.COLOR_BLUE   , 0)
            curses.init_pair(7 , curses.COLOR_RED , curses.COLOR_WHITE)
            curses.init_pair(8 , curses.COLOR_WHITE , 0)
            curses.init_pair(9 , curses.COLOR_YELLOW , curses.COLOR_YELLOW)
            curses.init_pair(10 , curses.COLOR_WHITE , curses.COLOR_YELLOW)

        curses.curs_set(0)

    def PaintHeader(self):
        '''
            ------------------------------------------
            | NAME          DD:HH:MM         VERSION |
            ------------------------------------------
        '''

        self.screen.addstr(0 , 0 , self.appInfo['name'] , curses.color_pair(1))
        current_pos = len(self.appInfo['name'])
        while current_pos < int(curses.COLS//2 - len(str(self.started))//2):
            self.screen.addstr(0 , current_pos , ' ' , curses.color_pair(3))
            current_pos += 1
        self.screen.addstr(0 , current_pos , str(self.started) , curses.color_pair(2))
        current_pos += len(str(self.started))
        while current_pos < int(curses.COLS - len(self.appInfo['version'])):
            self.screen.addstr(0 , current_pos , ' ' , curses.color_pair(3))
            current_pos += 1
        self.screen.addstr(0 , current_pos , self.appInfo['version'] , curses.color_pair(4))
        self.screen.refresh()
        return True

    '''
        @param username -> Target Account
        @param password_list -> password list path
    '''

    def PaintResourceInfo(self , username , password_list):
        '''
            [TARGET USERNAME]: <username>    [ PASSWORD LIST ]: <password_list>
        '''

        bold_yellow = curses.A_BOLD
        bold_yellow |= curses.color_pair(5)
        bold_blue = curses.A_BOLD
        bold_blue |= curses.color_pair(6)

        USERNAME = "[TARGET USERNAME]: "
        PASSWORD_LIST = "[ PASSWORD LIST ]: "


        current_pos = curses.COLS//2 - (4 + len(USERNAME)//2 + len(username)//2 + len(PASSWORD_LIST)//2 + len(password_list)//2)

        self.screen.addstr(2 , current_pos , USERNAME ,bold_yellow)
        current_pos += len(USERNAME)

        self.screen.addstr(2 , current_pos , username , bold_blue)
        current_pos += len(username) + 4

        self.screen.addstr(2 , current_pos , PASSWORD_LIST, bold_yellow)
        current_pos += len(PASSWORD_LIST)

        self.screen.addstr(2 , current_pos , password_list , bold_blue)

        self.screen.refresh()
        return True

    '''
        @progress_title = @param title
    '''

    def PaintProgressBar(self , title):
        '''
                        [ <TITLE> ]
        |==========================================|

        '''


        self.progress_title = title
        self.progress_win = curses.newwin(4 , curses.COLS , 4 , 0)
        bold_white = curses.A_BOLD | curses.color_pair(8)

        self.progress_win.addstr(0 , curses.COLS//2 - len(self.progress_title)//2 , self.progress_title , curses.color_pair(7))
        current_pos = curses.COLS//6
        self.progress_win.addstr(2 , current_pos , '[' , bold_white)
        current_pos += 1
        self.progress_win.addstr(2 , int(curses.COLS - current_pos) , ']' , bold_white)

        percentage = int((self.tried/self.total*100)/100 * (curses.COLS - current_pos))

        while current_pos < percentage:
            self.progress_win.addstr(2 , current_pos , ' ' , curses.color_pair(9))
            current_pos += 1

        self.progress_win.addstr(2 , curses.COLS//2 - len(str(self.tried) + " Finished.")//2 , str(self.tried) + " Finished." , curses.color_pair(10))
        self.progress_win.refresh()
        return True

    def UpdateProgressBar(self , tried):
        self.progress_win.clear()
        self.progress_win.refresh()
        self.PaintProgressBar(self.progress_title)
        self.tried = tried
        return True


    def PaintStatusReport(self , current_passwd , status , current_ip , response , password_found , verbose):
        '''
                [ TRYING ] : <current_passwd>
                [ STATUS ] : <status>

            [ CURRENT IP ]: 255.255.255.255
            [  RESPONSE  ]: <response>
        '''
        CUR_IP_TEXT = "[ CURRENT IP ]: "
        STATUS_TEXT = "     [   STATUS   ]: "
        RESPON_TEXT = "[  RESPONSE  ]: "
        CUR_PW_TEXT = "[   TRYING   ]: "
        PASSW_FOUND = "[ PASSWORD FOUND ]: "

        bold_white = curses.A_BOLD | curses.color_pair(8)

        if password_found == False:
            current_pos  = curses.COLS//2 - len(CUR_PW_TEXT)//2 - len(STATUS_TEXT)//2 - len(current_passwd)//2 - len(status)//2
            self.screen.addstr(9 , current_pos , CUR_PW_TEXT)
            current_pos += len(CUR_PW_TEXT)
            self.screen.addstr(9 , current_pos , current_passwd , bold_white)
            current_pos += len(current_passwd)
            self.screen.addstr(9 , current_pos ,STATUS_TEXT)
            current_pos += len(STATUS_TEXT)
            self.screen.addstr(9 , current_pos , status , bold_white)
        else:
            '''
                [ PASSWORD FOUND ]: <current_passwd>
            '''
            current_pos = curses.COLS//2 - len(PASSW_FOUND)//2 - len(current_passwd)//2
            self.screen.addstr(9 , current_pos , PASSW_FOUND , bold_white)
            current_pos += len(PASSW_FOUND)
            self.screen.addstr(9 , current_pos , current_passwd , bold_white)

        if  verbose == True:

            current_pos = curses.COLS//6
            self.screen.addstr(12 , current_pos , CUR_IP_TEXT , curses.color_pair(7))
            current_pos += len(CUR_IP_TEXT)
            self.screen.addstr(12 , current_pos , " " + current_ip , bold_white)
            current_pos = curses.COLS//6
            self.screen.addstr(14 , current_pos , RESPON_TEXT , curses.color_pair(7))
            current_pos += len(RESPON_TEXT)
            self.screen.addstr(14 , current_pos , " " + response , bold_white)

        self.screen.refresh()

        return True

    '''
        Kind of a Low level curses functions useful for the users.
    '''

    def ResizeScr(self):
        (height , width) = self.screen.getmaxyx()
        curses.resizeterm(height, width)

    def SoundBeep(self):
        curses.beep()

    def ClearScr(self):
        self.screen.clear()

    def GetsChar(self):
        return self.screen.getch()

    def Refreshs(self):
        self.screen.refresh()

    def CloseCLI(self):
        curses.endwin()
