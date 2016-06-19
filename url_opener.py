import cookielib
import urllib2

CHROME = 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'

def create(use_cookies=True):
  if use_cookies:
    cj = cookielib.CookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
  else:
    opener = urllib2.build_opener()
  opener.addheaders = [('User-Agent', CHROME)]
  return opener
