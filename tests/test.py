from InstagramPyCLI import InstagramPyCLI
from InstagramPyCLI import InstagramPyCLITerminator
import datetime
import curses
import time

def repaint_default(cli):
    cli.ResizeScr()
    cli.ClearScr()
    cli.PaintHeader()
    cli.PaintResourceInfo("actionkamen" , "facebook-phishing.txt")
    cli.PaintProgressBar("[ ATTACK STATUS ]")
    cli.PaintStatusReport(status = "Cracking... " , current_passwd = "StreetLight6" , current_ip="172.xxx.xxx.xxx" , response="The Thing is... " , verbose = True , password_found = False)

a = InstagramPyCLI(True , started=datetime.datetime.now() , total=100038294)

a.ResizeScr()
a.ClearScr()
a.PaintHeader()
a.PaintResourceInfo("actionkamen" , "facebook-phishing.txt")
a.PaintProgressBar("[ ATTACK STATUS ]")
a.PaintStatusReport(status = "Cracking... " , current_passwd = "StreetLight6" , current_ip="172.xxx.xxx.xxx" , response="The Thing is... " , verbose = True , password_found = False)

b = InstagramPyCLITerminator(a)
b.start()
b.join()

time.sleep(10)

'''
while True:
    if not once:
        a.ResizeScr()
        a.ClearScr()
        a.PaintHeader()
        a.PaintResourceInfo("actionkamen" , "facebook-phishing.txt")
        a.PaintProgressBar("[ ATTACK STATUS ]")
        a.PaintStatusReport(status = "Cracking... " , current_passwd = "StreetLight6" , current_ip="172.xxx.xxx.xxx" , response="The Thing is... " , verbose = True , password_found = False)
        once += 1
    c = a.GetsChar()

    if c == ord('q'):
        break
    elif c == curses.KEY_RESIZE:
        repaint_default(a)
        c = a.GetsChar()

a.CloseCLI()
'''
