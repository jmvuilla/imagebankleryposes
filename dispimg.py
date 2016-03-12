import cgi
from google.appengine.ext import ndb
import webapp2
import datetime
import time
import numpy
import numpy.random
from pytz.gae import pytz

class ImageDB(ndb.Model):
    date = ndb.DateTimeProperty('d',auto_now_add=True)
    img  = ndb.BlobProperty('i')

class MainPage(webapp2.RequestHandler):
    def get(self):
        dateparam = cgi.escape(self.request.get('date'))
        timeparam = cgi.escape(self.request.get('time'))
        datetimep = datetime.datetime.strptime(dateparam+' '+timeparam, '%d-%m-%Y %H:%M')
        local_tz = pytz.timezone('Europe/Paris')
        utcdatetimep = local_tz.localize(datetimep).astimezone(pytz.UTC)
	qry1=ImageDB.query(ndb.AND(ImageDB.date>=utcdatetimep,ImageDB.date< utcdatetimep+datetime.timedelta(minutes=1)))
        i=0
        for ientity in qry1:

            i=i+1 
        self.response.headers['Content-Type']= 'image/jpeg'
        self.response.out.write(ientity.img)

app = webapp2.WSGIApplication([
    ('/dispimg', MainPage),
], debug=True)
