#-------------------------------------------------------------------------------
# Name:        redsbrowser.py
# Purpose:     Copies stored login information from firefox for use in python
# Author:      AmazingRed (some code copied from guy rutenberg)
# Created:     7/30/2013 2:10:49 PM
# Licence:     Free for all just kredit me if you use my code....
#-------------------------------------------------------------------------------
import mechanize, cookielib, urllib, re, os, urllib2
from BeautifulSoup import BeautifulSoup

"""This is a little code I've customized for myself from Guy Rutenberg's Firefox
Cookiesharing code to make my own customized browser helper that I've found extremely
handy.

Essentially, this code will copy and load all of the cookies stored in your
firefox browser for use in a python script...I love this little shortcut because
for most websites, if you're logged in with firefox, you're then automatically
logged in with the python script so you don't have to spend more lines of code
handling Site Auth.

I have this script saved as a module named redsbrowser.py and just import it
for every script i write.  It returns a urllib2 opener, mechanize browser, and
preloaded cookiejar all with cookies copied from Firefox.  (note: i had it return
both mechanize and the urllib2 opener because I use one or the other of them
very frequently depending on what kind of task i'm performing.

Usage:
    Save file in python directory:
        (~/python2.7/redsbrowser.py)
        at the begining of a new script;

        import redsbrowser
        opener, br, cj=redsbrowser.redsbrowser()
        """

def _getFFcookiedir():
    """
    Don't call this function directly
    """
    profilesdir=os.getenv('appdata')+'\\Mozilla\\Firefox\\Profiles\\'
    filesinfodict={}
    for file in os.listdir(profilesdir):
        filesinfodict[os.path.getatime(profilesdir+file)]=file
    profile=filesinfodict[max(filesinfodict)]
    return profilesdir+profile+'\\cookies.sqlite'

def _makeCookieJar(): #kudos to Guy Rutenberg for the heart of this function
    """
    Don't call this function directly!
    """
    from StringIO import StringIO
    from pysqlite2 import dbapi2 as sqlite
    cj=cookielib.LWPCookieJar()
    cookiefile=_getFFcookiedir()
    con = sqlite.connect(cookiefile)
    cur = con.cursor()
    cur.execute("SELECT host, path, isSecure, expiry, name, value FROM moz_cookies")
    for item in cur.fetchall():
        c = cookielib.Cookie(0, item[4], item[5], None, False, item[0], item[0].startswith('.'), item[0].startswith('.'), item[1], False, item[2], item[3], item[3]=="", None, None, {})
        cj.set_cookie(c)
    return cj

def redsbrowser():
    cj=_makeCookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    opener.addheaders.append(('User-Agent','Mozilla/5.0'))
    br=mechanize.Browser()
    br.set_cookiejar(cj)
    br.set_handle_robots(False)
    return opener, br, cj