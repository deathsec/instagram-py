# Instagram-py , Copyright (C) 2017 The Future Shell , DeathSec
# filename: getfile.py
# Gets and Saves files required by Instagram-py

import requests
import json
import hashlib
import os
from os.path import isfile , expanduser, exists, basename
from datetime import datetime
from .getterminal import get_terminal_size
from .constants import app_error
from .logger import *
from .colors import Fore , Back , Style , init
from .progress import print_progress
from .instagram_bot import get_magic_cookie

init(autoreset=True)

def updateConfigWithCmdParsed(session_config , parsed):
    session_config['username'] = parsed.USERNAME[0]
    session_config['passwordFile'] = parsed.PASSWORD_LIST[0]
    session_config['verbose'] = parsed.verbose

    # report to the user that we are reading!
    sizex, sizey = get_terminal_size() # get terminal size for the progress_bar
    ptotal = int(sizex/3) # we cannot have the progress bar all over screen!

    # Loading configuration files 
    # edit this file to change the scripts actions!
    session_config['progress_status'] = ' [+] searching for config file... '; # this reports to the user in real time!
    print_progress(int(10/100*ptotal) , ptotal , session_config)
    if(isfile('instapy-config.json')):
        config = 'instapy-config.json'
        print_progress(int(30/100*ptotal) , ptotal , session_config)
    else:
        print_progress(int(20/100*ptotal) , ptotal , session_config)
        if(isfile(expanduser('~') + '/instapy-config.json')):
            config = expanduser('~') + '/instapy-config.json'
            print_progress(int(30/100*ptotal) , ptotal , session_config)
        else:
            report_err(app_error['no_config'])

    # Parsing the configuration file
    session_config['progress_status'] = ' [*] parsing config file... ';
    # after checking the if the file exist , then read the config
    print_progress(int(40/100*ptotal) , ptotal , session_config)
    try: # lets try parsing it as json
        with open(config) as json_data:
            session_config['config'] = json.load(json_data)
        print_progress(int(50/100*ptotal) , ptotal , session_config)
    except:
        # if some error in json syntax , exit!
        report_err(app_error['invalid_config'])

    session_config['bot'] = requests.session() # create a new session and set it to constant
    session_config['progress_status']  = ' [+] requesting magic cookie... '
    print_progress(int(80/100*ptotal) , ptotal , session_config)

    tor_proxy_server = str(
                       session_config['config']['tor']['protocol'] + '://' +
                       session_config['config']['tor']['server'] + ':' +
                       session_config['config']['tor']['port']
    )

    # lets configure requests bot!
    session_config['bot'].proxies = { # set proxy so that we can brute force instagram forever 
            # tor socks proxy!
            "https" : tor_proxy_server ,
            "http"  : tor_proxy_server
    }

    # build headers 

    session_config['bot'].headers.update(
            {
                'Connection' : 'close', # make sure requests closes the sockets instead of keep-alive!
                'Accept' : '*/*',
                'Content-type' : 'application/x-www-form-urlencoded; charset=UTF-8',
                'Cookie2' : '$Version=1',
                'Accept-Language' : 'en-US',
                'User-Agent' : session_config['config']['user-agent']
            }
    )

    # get the magic cookie!
    try: # and check if the proxy is working correctly!
        session_config['magic_cookie'] = get_magic_cookie(session_config)
    except KeyboardInterrupt:
        report_err(app_error['user_cancel']) # user must canceled the process
    except:
        report_err(app_error['tor_down']) # the must be in tor!

    # check if we got the cookie good!
    if not session_config['magic_cookie']:
        report_err(app_error['magic_fail'])

    # celebrate victory on getting the cookie!
    session_config['progress_status'] = ' [+] got cookie:: '+ session_config['magic_cookie']
    print_progress(int(100/100*ptotal) , ptotal , session_config)

    print ('\n') # graceful finish!

def writeSave(session_config , current_line):
    savefile = open(session_config['checkpoint'] , 'w')
    savefile.write(
    '{ "username" : "'+ session_config['username']+
    '" , "passwordFile" : "'+ basename(session_config['passwordFile'])+
    '" ,"line-count" : "'+ str(current_line)+
    '"}'
    )
    savefile.close()

def readSave(session_config):
    with open(session_config['checkpoint']) as json_data:
            session_config['save'] = json.load(json_data)

def loadSavefile(session_config):
   ### lets see if we have a save file!
   savefile_dir = expanduser('~') + '/.instagram-py' # the default save directory
   if not exists(savefile_dir) :
        os.makedirs(savefile_dir)
   session_config['checkpoint'] = str(
                savefile_dir + '/' +
                str(hashlib.sha224(session_config['username'].encode('utf-8')).hexdigest()) + '.dat'
   )
   if isfile(session_config['checkpoint']):
        readSave(session_config)
        if basename(session_config['save']['passwordFile']) == basename(session_config['passwordFile']):
            choose = input(Fore.CYAN + '[*] Previous attack found.... do you wish to resume? '+Fore.WHITE + Style.BRIGHT +'[Y/n] ')
            if(choose.lower() == 'y' or choose.lower() == 'yes'):
                readSave(session_config)
                session_config['resume'] = True
            else:
                writeSave(session_config , 1)
                session_config['resume'] = False

def getPasswordList(session_config):
    if(isfile(session_config['passwordFile'])):
        with open(session_config['passwordFile'] , encoding='utf-8', errors='ignore') as f:
            session_config['password_file_length'] = sum(1 for _ in f)
    else:
        report_err(app_error['no_file_p']) # report and exit if password file does not exist!
