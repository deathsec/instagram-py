# The MIT License.
# Copyright (C) 2017 The Future Shell , DeathSec.
#
# @filename    : InstagramPyCLI.py
# @description : Simple command line interface to display progress
#                and efficiently show response too.

import datetime
import sys
from InstagramPy import AppInfo
from .colors import *


class InstagramPyCLI:
    username = None
    started = None
    verbose = 0

    def __init__(self, appinfo, started, verbose_level, username):
        try:
            self.verbose = int(verbose_level)
            self.started = started
            self.username = username
            if not appinfo == None:
                appinfo = appinfo
        except:
            self.verbose = 0
            self.started = started
            appinfo = AppInfo.appInfo
            if username == None or username == '':
                self.ReportError("username not provided!")
            else:
                self.username = username

        self.HEADER = "{} {} , {}.\nCopyright (C) {} {} , {}.\n".format(appinfo['name'],
                                                                        appinfo['version'],
                                                                        appinfo['description'],
                                                                        appinfo['year'],
                                                                        appinfo['company'],
                                                                        appinfo['author'])
        self.HEADER = Fore.MAGENTA + self.HEADER + Style.RESET_ALL

    def ReportError(self, error):
        print('{}{}fatal error::{} {}'.format(
            Style.BRIGHT, Fore.RED, Style.RESET_ALL, error))
        sys.exit(-1)

    def PrintHeader(self):
        print(self.HEADER)
        return True

    def PrintDatetime(self):
        print('{}[{}+{}{}]{} {}Started{} @ {}'.format(Style.BRIGHT,
                                                      Fore.YELLOW,
                                                      Style.RESET_ALL,
                                                      Style.BRIGHT,
                                                      Style.RESET_ALL,
                                                      Fore.MAGENTA,
                                                      Style.RESET_ALL + Fore.YELLOW,
                                                      str(self.started) +
                                                      Style.RESET_ALL
                                                      ))
        return True

    def PrintChangingIP(self):
        print('[{}*{}] {}Changing IP Address... {}'.format(Fore.YELLOW,
                                                           Style.RESET_ALL, Fore.GREEN, Style.RESET_ALL))
        return True

    def PrintIPAddress(self, ip):
        print('[{}+{}] {}Current IP{} :: {}{}{}'.format(Fore.RED,
                                                        Style.RESET_ALL,
                                                        Fore.YELLOW,
                                                        Style.RESET_ALL,
                                                        Style.BRIGHT,
                                                        str(ip),
                                                        Style.RESET_ALL
                                                        ))
        return True

    def PrintPassword(self, password):
        print('[{}+{}] {}Trying [FOR] @{} {} :: {}{}{}'.format(Fore.GREEN,
                                                               Style.RESET_ALL,
                                                               Fore.CYAN,
                                                               self.username,
                                                               Style.RESET_ALL,
                                                               Style.BRIGHT,
                                                               password,
                                                               Style.RESET_ALL
                                                               ))
        return True

    def PrintRequest(self, req):
        print('\n[{}-{}] --:: {}REQUEST START -> @{} {} ::--'.format(Fore.MAGENTA,
                                                                     Style.RESET_ALL, Back.CYAN + Style.BRIGHT, self.username, Style.RESET_ALL))
        print('{}{}{} {}{}{}'.format(Fore.GREEN, req.method,
                                     Style.RESET_ALL, Style.BRIGHT, req.url, Style.RESET_ALL))
        print('{}{}{}'.format(Fore.YELLOW, '\n'.join('{}: {}'.format(k, v)
                                                     for k, v in req.headers.items()), Style.RESET_ALL))
        print('{}{}{}'.format(Style.BRIGHT, req.body, Style.RESET_ALL))
        print('[{}+{}] --:: {}REQUEST   END{} ::--'.format(Fore.GREEN,
                                                           Style.RESET_ALL, Back.GREEN + Style.BRIGHT, Style.RESET_ALL))
        return True

    def PrintResponse(self, resp):
        print('\n[{}-{}] --:: {}RESPONSE START -> @{} {} ::--'.format(Fore.MAGENTA,
                                                                      Style.RESET_ALL, Back.CYAN + Style.BRIGHT, self.username, Style.RESET_ALL))
        print('{}{}{}'.format(Style.BRIGHT, str(resp), Style.RESET_ALL))
        print('[{}+{}] --:: {}RESPONSE   END{} ::--'.format(Fore.GREEN,
                                                            Style.RESET_ALL, Back.GREEN + Style.BRIGHT, Style.RESET_ALL))
        return True

    def PrintProgress(self, password, ip, request, response):
        if self.verbose == 0:
            self.PrintPassword(password)
        elif self.verbose == 1:
            self.PrintPassword(password)
            self.PrintResponse(response)
        elif self.verbose == 2:
            self.PrintPassword(password)
            self.PrintResponse(response)
            self.PrintIPAddress(ip)
        else:
            self.PrintPassword(password)
            self.PrintRequest(request)
            self.PrintResponse(response)
            self.PrintIPAddress(ip)
        return True

    def ReportAttack(self, password):
        print('\n[{}+{}] --:: {}Completed -> @{} {} ::--'.format(Fore.YELLOW,
                                                                 Style.RESET_ALL, Back.YELLOW + Style.BRIGHT, self.username, Style.RESET_ALL),
              end='')
        if not password == None:
            print('{}[{}*{}{}]{} {}Password Found!{}  :: {}'.format(Style.BRIGHT,
                                                                    Fore.RED,
                                                                    Style.RESET_ALL,
                                                                    Style.BRIGHT,
                                                                    Style.RESET_ALL,
                                                                    Fore.CYAN,
                                                                    Style.RESET_ALL + Style.BRIGHT + Fore.GREEN,
                                                                    password + Style.RESET_ALL
                                                                    ))
        else:
            print('{}{}Password not found , Try using another wordlist.{}'.format(
                Style.BRIGHT, Fore.RED, Style.RESET_ALL))

        print('{}[{}+{}{}]{} {}Finnished in {}{}'.format(Style.BRIGHT,
                                                         Fore.YELLOW,
                                                         Style.RESET_ALL,
                                                         Style.BRIGHT,
                                                         Style.RESET_ALL,
                                                         Fore.MAGENTA,
                                                         Style.RESET_ALL + Fore.YELLOW,
                                                         str(datetime.datetime.now(
                                                         ) - self.started) + Style.RESET_ALL
                                                         ))
        return True

    def PrintFooter(self):
        print('\n{}Report bug, suggestions and new features at {}{}https://github.com/deathsec/instagram-py{}'.format(Fore.GREEN,
                                                                                                                      Style.RESET_ALL,
                                                                                                                      Style.BRIGHT,
                                                                                                                      Style.RESET_ALL
                                                                                                                      ))
        return True
