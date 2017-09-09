# Instagram-py , Copyright (C) 2017 The Future Shell , DeathSec
# filename : progress.py
# Progress bar for Instagram-py
from .colors import Fore , Back , Style , init

init(autoreset=True) # set to automatically reset colors!

def print_progress(complete , total , session_config):
    print('\r' , end='')
    complete_width = int(total*3)
    progress_bar = str(Style.BRIGHT + '[' + Style.DIM)
    progress_bar += str(Back.YELLOW)
    progress_bar += complete * str(' ')
    progress_bar += Style.RESET_ALL
    progress_bar += (total-complete) * str(' ')
    progress_bar += str(Style.BRIGHT + ']' + Style.RESET_ALL)
    progress_bar += Style.BRIGHT + session_config['progress_status'] + Style.RESET_ALL
    progress_bar += int(complete_width-int(total+len(session_config['progress_status']) + 1)) * str(' ')
    print(progress_bar,end='' ,  flush=True)
