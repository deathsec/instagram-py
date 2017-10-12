# The MIT License.
# Copyright (C) 2017 The Future Shell , DeathSec.
#
# @filename    : InstagramPyCLI.py
# @description : Simple command line interface to display progress
#                and efficiently show response too.

from InstagramPy import AppInfo
import datetime
from .colors import *

class InstagramPyCLI:
    username = None
    password_list = None
    started = None
    verbose = 0

    def __init__(self , appinfo , started , verbose_level):
        try:
            self.verbose = int(verbose_level)
            self.started = started
            if not appinfo == None:
                appinfo = appinfo
        except:
            self.verbose = 0
            self.started = started
            appinfo = AppInfo.appInfo

        self.HEADER = "{} {} , {}.\nCopyright (C) {} {} , {}.\n".format(appinfo['name'] ,
                                                                        appinfo['version'] ,
                                                                        appinfo['description'] ,
                                                                        appinfo['year'] ,
                                                                        appinfo['company'] ,
                                                                        appinfo['author'])
        self.HEADER = Fore.MAGENTA + self.HEADER + Style.RESET_ALL

    def ReportError(self , error):
        print('{}{}fatal error::{} {}'.format(Style.BRIGHT , Fore.RED , Style.RESET_ALL , error))
        exit(-1)

    def PrintHeader(self):
        print(self.HEADER)
        return True

    def PrintMagicCookie(self , magic_cookie):
        print('[{}+{}] {}Magic Cookie{} :: {}{}{}'.format(Fore.GREEN ,
                                                    Style.RESET_ALL ,
                                                    Fore.YELLOW ,
                                                    Style.RESET_ALL ,
                                                    Style.BRIGHT ,
                                                    magic_cookie,
                                                    Style.RESET_ALL
        ))
        return True

    def PrintDatetime(self):
        print('{}[{}+{}{}]{} {}Started{} @ {}'.format(Style.BRIGHT ,
                                                            Fore.YELLOW ,
                                                            Style.RESET_ALL ,
                                                            Style.BRIGHT ,
                                                            Style.RESET_ALL ,
                                                            Fore.MAGENTA ,
                                                            Style.RESET_ALL + Fore.YELLOW ,
                                                            str(self.started) + Style.RESET_ALL
        ))
        return True

    def PrintResource(self , username , password_list):
        self.username       = username
        self.password_list  = password_list
        print('{}[{}*{}{}]{} {}USERNAME{} :: {}'.format(Style.BRIGHT ,
                                                            Fore.RED ,
                                                            Style.RESET_ALL ,
                                                            Style.BRIGHT ,
                                                            Style.RESET_ALL + Style.BRIGHT ,
                                                            Fore.CYAN ,
                                                            Style.RESET_ALL ,
                                                            self.username
        ))
        print('{}[{}*{}{}]{} {}WORDLIST{}  :: {}'.format(Style.BRIGHT ,
                                                            Fore.RED ,
                                                            Style.RESET_ALL ,
                                                            Style.BRIGHT ,
                                                            Style.RESET_ALL + Style.BRIGHT ,
                                                            Fore.CYAN ,
                                                            Style.RESET_ALL ,
                                                            self.password_list
        ))
        return True

    def PrintChangingIP(self):
        print('[{}*{}] {}Changing IP Address... {}'.format(Fore.YELLOW,Style.RESET_ALL , Fore.GREEN , Style.RESET_ALL))
        return True

    def PrintIPAddress(self , ip):
        print('[{}+{}] {}Current IP{} :: {}{}{}'.format(Fore.RED ,
                                                    Style.RESET_ALL ,
                                                    Fore.YELLOW ,
                                                    Style.RESET_ALL ,
                                                    Style.BRIGHT ,
                                                    str(ip),
                                                    Style.RESET_ALL
        ))
        return True

    def PrintPassword(self , password):
        print('[{}+{}] {}Trying{} :: {}{}{}'.format(Fore.GREEN ,
                                                    Style.RESET_ALL ,
                                                    Fore.CYAN ,
                                                    Style.RESET_ALL ,
                                                    Style.BRIGHT ,
                                                    password,
                                                    Style.RESET_ALL
        ))
        return True

    def PrintRequest(self , req):
        print('\n[{}-{}] --:: {}REQUEST START{} ::--'.format(Fore.MAGENTA , Style.RESET_ALL , Back.CYAN+Style.BRIGHT, Style.RESET_ALL))
        print('{}{}{} {}{}{}'.format(Fore.GREEN , req.method , Style.RESET_ALL , Style.BRIGHT , req.url , Style.RESET_ALL))
        print('{}{}{}'.format(Fore.YELLOW , '\n'.join('{}: {}'.format(k, v) for k, v in req.headers.items()) , Style.RESET_ALL))
        print('{}{}{}'.format(Style.BRIGHT , req.body , Style.RESET_ALL))
        print('[{}+{}] --:: {}REQUEST   END{} ::--'.format(Fore.GREEN , Style.RESET_ALL , Back.GREEN+Style.BRIGHT , Style.RESET_ALL))
        return True

    def PrintResponse(self ,resp):
        print('\n[{}-{}] --:: {}RESPONSE START{} ::--'.format(Fore.MAGENTA , Style.RESET_ALL , Back.CYAN+Style.BRIGHT , Style.RESET_ALL))
        print('{}{}{}'.format(Style.BRIGHT , str(resp) , Style.RESET_ALL))
        print('[{}+{}] --:: {}RESPONSE   END{} ::--'.format(Fore.GREEN , Style.RESET_ALL , Back.GREEN+Style.BRIGHT , Style.RESET_ALL))
        return True

    def PrintProgress(self , password , ip , request , response):
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

    def ReportAttack(self , password , username = '' , password_list = ''):
        print('\n[{}+{}] --:: {}ATTACK REPORT{} ::--'.format(Fore.YELLOW , Style.RESET_ALL , Back.YELLOW+Style.BRIGHT , Style.RESET_ALL))
        if self.username == None or self.password_list == None:
            self.username = username
            self.password_list = password_list

        self.PrintResource(self.username , self.password_list)
        if not password == None:
            print('{}[{}*{}{}]{} {}PASSWORD{}  :: {}\n'.format(Style.BRIGHT ,
                                                                Fore.RED ,
                                                                Style.RESET_ALL ,
                                                                Style.BRIGHT ,
                                                                Style.RESET_ALL ,
                                                                Fore.CYAN ,
                                                                Style.RESET_ALL + Style.BRIGHT + Fore.GREEN,
                                                                password + Style.RESET_ALL
            ))
        else:
            print('\n{}{}Password not found , Try using another wordlist.{}\n'.format(Style.BRIGHT , Fore.RED , Style.RESET_ALL))

        print('{}[{}+{}{}]{} {}Finnished in {}{}'.format(Style.BRIGHT ,
                                                      Fore.YELLOW ,
                                                      Style.RESET_ALL ,
                                                      Style.BRIGHT ,
                                                      Style.RESET_ALL ,
                                                      Fore.MAGENTA ,
                                                      Style.RESET_ALL + Fore.YELLOW  ,
                                                      str(datetime.datetime.now() - self.started) + Style.RESET_ALL
        ))
        print('{}Report bug, suggestions and new features at {}{}https://github.com/deathsec/instagram-py{}'.format(Fore.GREEN,
                                                                                                                    Style.RESET_ALL,
                                                                                                                    Style.BRIGHT,
                                                                                                                    Style.RESET_ALL
        ))
        return True



