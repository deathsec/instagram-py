# Instagram-py , Copyright (C) 2017 The Future Shell , DeathSec
# filename: logger.py
# Colorful print functions for Instagram-py

from .colors import Fore , Back , Style , init
from .constants import appInfo
from datetime import datetime

init(autoreset=True) # set to automatically reset colors!

def log_result(session_config):
     print(
        Style.BRIGHT + '[ ' + Style.RESET_ALL + Fore.CYAN +
             'PASSWORD FOUND!'
        + Style.RESET_ALL + Style.BRIGHT + ' ]'
     )
     print(
        Style.BRIGHT + 'username: ' + session_config['username'] + '\n' +
        'password: ' + Fore.CYAN + session_config['password']
     )
     print (
        Fore.YELLOW + '\nReport bugs , suggestions and new features at ' +
        Fore.BLUE + Style.BRIGHT + 'https://github.com/DeathSec/instagram-py'
     )
     print(Fore.CYAN + '[*] processed in ' + Style.RESET_ALL + Style.BRIGHT +
             str(datetime.now() - session_config['start']) + ' hours'
     )
     print (Fore.GREEN + 'Thank you for using Intagram-py')
     exit(0)

def print_head(get_string):
    ret = str(
        Fore.MAGENTA + Style.BRIGHT + appInfo['name'] + Style.RESET_ALL + Fore.CYAN + ' v' + appInfo['version'] + ', ' + appInfo['description'] + '\n' +
        'Copyright (C) ' + appInfo['year'] + ' ' + appInfo['author'] + '\n'
        + Style.RESET_ALL
    )
    if not get_string:
            print(ret)
    else:
        return ret


def report_err(err): # reports error and exits!
    print (Fore.RED + Style.BRIGHT + err)
    print (
           Fore.YELLOW + 'Report bugs , suggestions and new features at ' +
           Fore.BLUE + Style.BRIGHT + 'https://github.com/DeathSec/instagram-py'
    )
    print (Fore.GREEN + 'Thank you for using Intagram-py')
    exit(-1) # report error to operating system!

