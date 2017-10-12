# The MIT License.
# Copyright (C) 2017 The Future Shell , DeathSec.
#
# @filename    : __init__.py
# @description : The traditional python package __init__ file

import argparse
from .InstagramPyCLI import InstagramPyCLI
from .InstagramPySession import InstagramPySession,DEFAULT_PATH
from .InstagramPyInstance import InstagramPyInstance
from datetime import datetime
from .AppInfo import appInfo as AppInformation

__version__ = AppInformation['version']


'''
Arguments for instagram-py command-line tool
'''
cli_parser = argparse.ArgumentParser(
        epilog=AppInformation['example']
)

# nargs = '+' , makes them positional argument.
cli_parser.add_argument('USERNAME' ,  # parse username from command line
                        type=str ,
                        help='username for Instagram account' ,
                        nargs = '+'
)

cli_parser.add_argument('PASSWORD_LIST' , # parse path to password list file
                        type=str ,
                        default='./' ,
                        help='password list file to try with the given username.' ,
                        nargs='+'
)

cli_parser.add_argument('--countinue',
                        '-c' ,
                        action='count',
                        help='Countinue the previous attack if found.'
)
cli_parser.add_argument('--verbose' , # check if the user wants verbose mode enabled
                        '-v' ,
                        action='count' ,
                        help='Activate Verbose mode. ( Verbose level )'
)

def ExecuteInstagramPy():
    Parsed = cli_parser.parse_args()
    cli = InstagramPyCLI(appinfo = AppInformation , started = datetime.now() , verbose_level = Parsed.verbose)

    cli.PrintHeader()
    cli.PrintResource(Parsed.USERNAME[0] , Parsed.PASSWORD_LIST[0])
    cli.PrintDatetime()

    session = InstagramPySession(Parsed.USERNAME[0] , Parsed.PASSWORD_LIST[0] , DEFAULT_PATH , DEFAULT_PATH , cli)
    session.ReadSaveFile(Parsed.countinue)
    cli.PrintMagicCookie(session.magic_cookie)

    instagrampy = InstagramPyInstance(cli ,session)
    while not instagrampy.PasswordFound():
        instagrampy.TryPassword()
    exit(0)

