from InstagramPyReports import InstagramPyReports
import constants

Reporter = InstagramPyReports(appinfo = constants.appInfo , verbose = True)

Reporter.CheckPackage("requests")
import requests

def post():
    requests.get('http://gsaddsfsdf.com')

Reporter.Try(post)
