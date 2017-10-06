# The MIT License.
# Copyright (C) 2017 The Future Shell , DeathSec.
#
# @filename    : InstagramPyReports.py
# @description : reports and exits the program if error occurs with specific
#                error code with ease!
from colors import *
import requests

class InstagramPyReports:

    HEADER       = ""
    appInfo      = ""
    VERBOSE_MODE = False

    def __init__(self , appinfo , verbose):
        self.VERBOSE_MODE = verbose
        self.appInfo = appinfo
        self.HEADER = "{} {} , {}.\nCopyright (C) {} {} , {}.\n".format(appinfo['name'] , appinfo['version'] , appinfo['description'] , appinfo['year'] , appinfo['company'] , appinfo['author'])

    def ExitsNow(self):
        exit(-1)

    def FindError(self , error , withHeader):
        if withHeader:
            self.HEADER = Fore.CYAN + self.HEADER + Style.RESET_ALL
            print(self.HEADER)
        print(Style.BRIGHT + Fore.RED + "fatal error:: " + Style.RESET_ALL + str(error))
        self.ExitsNow()

    def CheckPackage(self , package):
        try:
            exec("import {}".format(package))
        except Exception as err:
            self.FindError(err)

    def Try(self , callback):
        try:
            callback()
        except BaseException as err:
            self.FindError(err)
