# The MIT License.
# Copyright (C) 2017 The Future Shell , DeathSec.
#
# @filename    : InstagramPyReports.py
# @description : reports and exits the program if error occurs with specific
#                error code with ease!
from colors import *

class InstagramPyReports:

    HEADER       = ""
    appInfo      = ""
    VERBOSE_MODE = False

    def __init__(self , appinfo , verbose):
        self.VERBOSE_MODE = verbose
        self.appInfo = appinfo
        self.HEADER = "{} {} , {}.\nCopyright (C) {} {} , {}.\n".format(appinfo['name'] , appinfo['version'] , appinfo['description'] , appinfo['year'] , appinfo['company'] , appinfo['author'])
        self.HEADER = Fore.MAGENTA + self.HEADER + Style.RESET_ALL
    def ExitsNow(self):
        exit(-1)

    def ReportPassword(password , username):
        print(self.HEADER)
        print(Style.BRIGHT + Fore.GREEN + "attack success:: " + Fore.CYAN + "[ USERNAME -> " + username + " ] [ PASSWORD -> " + password+ " ]."+ Style.RESET_ALL)
        exit(0)

    def FindError(self , error , withHeader):
        if withHeader:
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
        except (BaseException,Exception) as err:
            self.FindError(err)
