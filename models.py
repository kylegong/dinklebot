import webapp2
from google.appengine.ext import ndb

class Spoiler(ndb.Model):
  username = ndb.StringProperty()
  channel = ndb.StringProperty()
  message = ndb.StringProperty()
  created = ndb.DateTimeProperty(auto_now_add=True)

  @staticmethod
  def lookup(key):
    return ndb.Key(urlsafe=key).get()

  @staticmethod
  def save(username, channel, message):
    spoiler = Spoiler(username=username, channel=channel, message=message)
    spoiler.put()
    key = spoiler.key.urlsafe()
    url = webapp2.uri_for('spoiler', key=key)
    return url
