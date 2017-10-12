# The MIT License.
# Copyright (C) 2017 The Future Shell , DeathSec.
#
# @filename    : InstagramPySession.py
# @description : creates a new session , checks for configuration and gets critical data
#                , loads save and saves data too.
import json
import os
import uuid
import hashlib
import requests
from stem import Signal
from stem.control import Controller

DEFAULT_PATH = "{}/".format(os.path.expanduser('~'))

class InstagramPySession:
    '''
        __init__:
            - loads configuration from specified file.
            - gets the perfect place for the save file.
            - sets class variables for later use.
    '''

    magic_cookie    = None
    api_url         = None
    user_agent      = None
    ig_sig_key      = None
    ig_sig_version  = None
    tor_proxy       = None
    tor_controller   = None
    save_data       = None
    current_save    = None
    username        = ''
    password        = ''
    password_list   = None
    password_list_md5_sum= None
    password_list_buffer = None
    password_list_length = 0
    eopl            = False
    current_line    = 1
    ip              = None
    cli        = None
    bot             = requests.Session()

    def __init__(self , username , password_list , configuration , save_location , cli):

        self.username = username
        self.cli = cli

        if not os.path.isfile(password_list):
            self.cli.ReportError("password list not found at {}.".format(password_list) )
        self.password_list = password_list
        '''
            Note: Always open password list with errors ignored because all password list
                  mostly has a wrong encoding or the users pc does not support it!
        '''
        self.password_list_buffer = open(password_list , encoding='utf-8' , errors='ignore')
        self.password_list_md5_sum = str(self.md5sum(open(password_list , "rb")).hexdigest())

        with open(password_list , encoding='utf-8' , errors='ignore') as f:
            for line in f:
                self.password_list_length += 1

        if configuration == DEFAULT_PATH:
            configuration = "{}instapy-config.json".format(DEFAULT_PATH)
        if save_location == DEFAULT_PATH:
            save_location = "{}.instagram-py/".format(DEFAULT_PATH)

        if not os.path.isfile(configuration):
            self.cli.ReportError("configuration file not found at {}".format(configuration) )
        else:
            try:
                with open(configuration , "r") as fp:
                    configuration = json.load(fp)
            except Exception as err:
                self.cli.ReportError("invalid configuration file at {}".format(configuraion) ) 

            self.api_url        = configuration['api-url']
            self.user_agent     = configuration['user-agent']
            self.ig_sig_key     = configuration['ig-sig-key']
            self.ig_sig_version = configuration['ig-sig-version']
            self.tor_proxy      = "{}://{}:{}".format(configuration['tor']['protocol'] , configuration['tor']['server'] , configuration['tor']['port'])
            if not configuration['tor']['control']['password'] == "":
                self.OpenTorController(configuration['tor']['control']['port'] , configuration['tor']['control']['password'])
            else:
                self.OpenTorController(configuration['tor']['control']['port'] , None)

            self.bot.proxies = {
                # tor socks proxy!
                "https" : self.tor_proxy ,
                "http"  : self.tor_proxy
            }

            # build headers 

            self.bot.headers.update(
                {
                    'Connection' : 'close', # make sure requests closes the sockets instead of keep-alive!
                    'Accept' : '*/*',
                    'Content-type' : 'application/x-www-form-urlencoded; charset=UTF-8',
                    'Cookie2' : '$Version=1',
                    'Accept-Language' : 'en-US',
                    'User-Agent' : self.user_agent
                }
            )

            '''
                Note: https://icanhazip.com is a free domain to get your current tor ip
                      this is not a dangerous website for sure , thank you @majorhayden
            '''
            try:
                self.ip = self.bot.get('https://icanhazip.com').content.rstrip().decode()
            except KeyboardInterrupt:
                self.cli.ReportError("process aborted by the user")
            except (BaseException,Exception) as err:
                self.cli.ReportError("Connection to host failed , check your connection and tor configuration." )

        if not os.path.exists(save_location):
            try:
                os.mkdir(save_location)
            except (BaseException , Exception) as err:
                self.cli.ReportError(err)

            self.save_data = save_location
        else:
            self.save_data = save_location

        try:
            self.bot.get(
            "{}si/fetch_headers/?challenge_type=signup&guid={}".format(self.api_url , str(uuid.uuid4()).replace('-' , ''))
            )
            self.magic_cookie = self.bot.cookies['csrftoken']
        except KeyboardInterrupt:
            self.cli.ReportError("cannot get the magic cookie , aborted by the user")
        except (BaseException , Exception) as err:
            self.cli.ReportError(err)


    '''
        ReadSaveFile()
            - Checks if we have located the save file
            - if not creates one
            - opens the save file and load it as json data
            - check if the user uses the same password list file for the same user
            - set the current password pointer to the given data
    '''
    def ReadSaveFile(self , isResume):
        if self.current_save == None:
            self.CreateSaveFile(isResume)
        SaveFile = json.load(open(self.current_save , 'r'))
        self.current_line = SaveFile['line-count']
        if self.password_list_md5_sum == SaveFile['password-file-md5'] and self.username == SaveFile['username']:
                c_line = 1
                for line in self.password_list_buffer:
                    self.password = str(line).rstrip()
                    if c_line == self.current_line:
                        break
                    c_line += 1
        return True

    '''
        UpdateSaveFile()
            - check if we have created a save file
            - if yes , rewrite the the save file with the current session!
    '''
    def UpdateSaveFile(self):
        if not self.current_save == None:
            updatefile = open(self.current_save , 'w')
            json.dump(
                {
                    "username"          : str(self.username) ,
                    "password-file-md5" : str(self.password_list_md5_sum) ,
                    "line-count"        : self.current_line
                }
            , updatefile)
            updatefile.close()


    '''
        CreateSaveFile()
            - checks if we have not openned any save file but know the save location.
            - if yes , creates with default settings to the location.
    '''
    def CreateSaveFile(self , isResume):
        if self.current_save == None and not self.save_data == None:
            save = '{}{}.dat'.format(self.save_data , hashlib.sha224(self.username.encode('utf-8')).hexdigest())
            self.current_save = save
            if not os.path.isfile(save):
                self.UpdateSaveFile()
            else:
                if not isResume:
                    self.UpdateSaveFile()

    '''
        CurrentPassword()
            - returns the current password pointed to the password list
    '''
    def CurrentPassword(self):
        return self.password


    '''
        NextPassword()
            - increaments and sets the next password as our current password
    '''
    def NextPassword(self):
        if not self.current_line > self.password_list_length:
            for line in self.password_list_buffer:
                self.password = str(line.rstrip())
                break
            self.current_line += 1
        else:
            self.eopl = True

    '''
        GetUsername()
            - returns current session username
    '''
    def GetUsername(self):
        return self.username

    '''
        md5sum( FILE POINTER , BLOCK SIZE)
            - opens large files from FILE POINTER
            - calculates md5 with BLOCK SIZE with respect to FILE POINTER
            - finalizes and returns a hashlib object!
    '''
    def md5sum(self , fp , block_size=2**20):
        md5 = hashlib.md5()
        while True:
            data = fp.read(block_size)
            if not data:
                break
            md5.update(data)
        return md5

    '''
        ChangeIPAddress()
            - stem <-> Signal
            - Changes Tor Identity with the controller!
    '''
    def ChangeIPAddress(self):
        if not self.tor_controller == None:
            self.tor_controller.signal(Signal.NEWNYM) # signal tor to change ip
            self.ip = self.bot.get('https://icanhazip.com').content.rstrip().decode()
            return True
        return False

    '''
        OpenTorController(PORT , PASSWORD)
            - Creates a fresh tor controller instance to the session
    '''
    def OpenTorController(self, port , password):
        try:
            self.tor_controller = Controller.from_port(port = int(port))
            if password == None:
                self.tor_controller.authenticate()
            else:
                self.tor_controller.authenticate(password = password)
        except Exception as err:
            self.cli.ReportError("Tor configuration invalid or server down :: {}".format(err) )
