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
            - loads configuration from specified file
            - starts a save file instance
            - sets class variables for later use.
    '''

    magic_cookie    = None
    api_url         = None
    user_agent      = None
    ig_sig_key      = None
    ig_sig_version  = None
    tor_proxy       = None
    tor_controler   = None
    save_data       = None
    current_save    = None
    username        = ''
    password        = ''
    password_list   = None
    password_list_buffer = None
    password_list_length = 0
    current_line    = 1
    ip              = None
    reporter        = None
    bot             = requests.Session()

    def __init__(self , username , password_list , configuration , save_location , reporter):

        self.username = username
        self.reporter = reporter

        if not os.path.isfile(password_list):
            reporter.FindError("password list not found at {}.".format(password_list) , True)
        self.password_list = password_list
        self.password_list_buffer = open(password_list , encoding='utf-8' , errors='ignore')

        with open(password_list , encoding='utf-8' , errors='ignore') as f:
            for line in f:
                self.password_list_length += 1

        if configuration == DEFAULT_PATH:
            configuration = "{}instapy-config.json".format(DEFAULT_PATH)
        if save_location == DEFAULT_PATH:
            save_location = "{}.instagram-py/".format(DEFAULT_PATH)

        if not os.path.isfile(configuration):
            reporter.FindError("configuration file not found at {}".format(configuration) , True)
        else:
            try:
                with open(configuration , "r") as fp:
                    configuration = json.load(fp)
            except Exception as err:
                reporter.FindError("invalid configuration file at {}".format(configuraion) , True) 

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
            self.ip = self.bot.get('https://icanhazip.com').content.rstrip().decode()

        if not os.path.exists(save_location):
            reporter.Try(os.mkdir(save_location))
            self.save_data = save_location
        else:
            self.save_data = save_location

        self.bot.get(
        "{}si/fetch_headers/?challenge_type=signup&guid={}".format(self.api_url , str(uuid.uuid4()).replace('-' , ''))
        )
        self.magic_cookie = self.bot.cookies['csrftoken']

    def ReadSaveFile(self):
        if self.current_save == None:
            self.CreateSaveFile()
        self.current_line = (json.load(open(self.current_save , 'r')))['line-count']
        if self.password_list == (json.load(open(self.current_save , 'r')))['password-file']:
            c_line = 1
            for line in self.password_list_buffer:
                self.password = str(line)
                if c_line == self.current_line:
                    break
                c_line += 1

    def UpdateSaveFile(self):
        if not self.current_save == None:
            updatefile = open(self.current_save , 'w')
            updatefile.write(
            '{"username" : "'+str(self.username)+'" ,"password-file" : "'+str(self.password_list)+'" ,"line-count" : '+str(self.current_line)+' }'
            )
            updatefile.close()

    def CreateSaveFile(self):
        if self.current_save == None and not self.save_data == None:
            save = '{}{}.dat'.format(self.save_data , hashlib.sha224(self.username.encode('utf-8')).hexdigest())
            if not os.path.isfile(save):
                savefile = open(save, 'w')
                savefile.write(
                '{"username" : "'+str(self.username)+'" ,"password-file" : "'+str(self.password_list)+'" ,"line-count" : 1}'
                )
                savefile.close()
            self.current_save = save


    def CurrentPassword(self):
        return self.password

    def NextPassword(self):
        if not self.password_list_buffer == None:
            for line in self.password_list_buffer:
                self.password = str(line.rstrip())
                self.current_line += 1
                break
        else:
            reporter.FindError("calling NextPassword without password file." , True)

    def GetUsername(self):
        return self.username

    def md5sum(self , fp , block_size=2**20):
        md5 = hashlib.md5()
        while True:
            data = fp.read(block_size)
            if not data:
                break
            md5.update(data)
        return md5.digest()

    def ChangeIPAddress(self):
        if not self.tor_controller == None:
            self.tor_controller.signal(Signal.NEWNYM) # signal tor to change ip
            self.ip = self.bot.get('https://icanhazip.com').content.rstrip().decode()
            return True
        return False

    def OpenTorController(self, port , password):
        self.tor_controller = Controller.from_port(port = int(port))
        if  password == None:
            self.reporter.Try(self.tor_controller.authenticate)
        else:
            try:
                self.tor_controller.authenticate(password = password)
            except BaseException as err:
                reporter.FindError(err , True)
