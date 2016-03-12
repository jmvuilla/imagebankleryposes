from google.appengine.api import urlfetch
from google.appengine.ext import ndb
import webapp2
import datetime

class ImageDB(ndb.Model):
    date = ndb.DateTimeProperty('d',auto_now_add=True)
    img  = ndb.BlobProperty('i')
    
class MainPage(webapp2.RequestHandler):
    def get(self):

        url = 'http://meteocamtroislacs.dtdns.net/axis-cgi/jpg/image.cgi?resolution=1280x720'
        result = urlfetch.fetch(url,deadline=15)
        if result.status_code == 200:
            reqdata = result.content

            dtnow = datetime.datetime.now()
            newentity = ImageDB(date=dtnow, img=reqdata)
            newentity.put()

        self.response.headers['Content-Type'] = 'text/plain'
        self.response.http_status_message(200)

app = webapp2.WSGIApplication([('/tasks/getimg', MainPage)], debug=True)

