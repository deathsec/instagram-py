from InstagramPySession import *
from InstagramPyReports import InstagramPyReports
from constants import appInfo

Reports = InstagramPyReports(appInfo , True)
Current_Session = InstagramPySession(
        username = 'instatestgod__' , password_list = '/home/antonyjr/Developer/.exploits/facebook-phished.txt',
        configuration = DEFAULT_PATH , save_location = DEFAULT_PATH , reporter=Reports
        )

Current_Session.CreateSaveFile()
Current_Session.ReadSaveFile()
print(Current_Session.CurrentPassword())
Current_Session.NextPassword()
print(Current_Session.CurrentPassword())
Current_Session.NextPassword()
print(Current_Session.CurrentPassword())
