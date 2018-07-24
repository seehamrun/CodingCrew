from google.appengine.ext import ndb
class StoredDate(ndb.Model):
    day = ndb.StringProperty()
    mood = ndb.StringProperty()
    notes = ndb.StringProperty()
    sleep = ndb.StringProperty()
    activity = ndb.StringProperty()
    color = ndb.StringProperty()
    username =ndb.StringProperty()
