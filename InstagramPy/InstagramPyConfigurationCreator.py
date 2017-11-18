# The MIT License.
# Copyright (C) 2017 The Future Shell , DeathSec.
#
# @filename    : InstagramPyConfigurationCreator.py
# @description : Create a Configuration file for Instagram-Py with ease.
import os
import json
from .colors import *


class InstagramPyConfigurationCreator:
    config_path = None
    default_config = {
        "api-url": "https://i.instagram.com/api/v1/",
        "user-agent": "Instagram 10.26.0 Android (18/4.3; 320dpi; 720x1280; Xiaomi; HM 1SW; armani; qcom; en_US)",
        "ig-sig-key": "4f8732eb9ba7d1c8e8897a75d6474d4eb3f5279137431b2aafb71fafe2abe178",
        "ig-sig-version": "4",
        "tor": {
            "server": "127.0.0.1",
            "port": "9050",
            "protocol": "socks5",
            "control": {
                "password": "",
                "port": "9051"
            }
        }
    }

    def __init__(self, path):
        self.config_path = path

    '''
    create():
        - Simply Creates a Configuration with the default settings.
    '''

    def create(self):
        with open(self.config_path, 'w') as f:
            json.dump(self.default_config, f)
        print("{}Written Configuration at {}{}".format(
            Style.BRIGHT, self.config_path, Style.RESET_ALL))
        return True

    def easy_create(self):
        tor_server_ip = None
        tor_port = None
        tor_control_port = None
        tor_control_password = None
        print("{}Welcome to Instagram-Py Configuration Creator!{}".format(Style.BRIGHT, Style.RESET_ALL))
        tor_server_ip = input("{}Tor Server IP(default=[Press Enter]):: {}"
                              .format(Style.BRIGHT + Fore.MAGENTA, Style.RESET_ALL))
        tor_port = input("{}Tor Server Port(default=[Press Enter]):: {}"
                         .format(Style.BRIGHT + Fore.MAGENTA, Style.RESET_ALL))
        tor_control_port = input("{}Tor Control Port(default=[Press Enter]):: {}"
                                 .format(Style.BRIGHT + Fore.MAGENTA, Style.RESET_ALL))
        tor_control_password = input("{}Tor Authentication Password(default=[Press Enter]):: {}"
                                     .format(Style.BRIGHT + Fore.MAGENTA, Style.RESET_ALL))

        print("{}Writing Configuration...{}".format(
            Style.BRIGHT, Style.RESET_ALL))

        if tor_server_ip is not '':
            self.default_config['tor']['server'] = tor_server_ip
        if tor_port is not '':
            self.default_config['tor']['port'] = tor_port
        if tor_control_port is not '':
            self.default_config['tor']['control']['port'] = tor_control_port
        if tor_control_password is not '':
            self.default_config['tor']['control']['password'] = tor_control_password

        with open(self.config_path, 'w') as f:
            json.dump(self.default_config, f)

        print("{}Written Configuration at {}{}".format(
            Style.BRIGHT, self.config_path, Style.RESET_ALL))
        return True
