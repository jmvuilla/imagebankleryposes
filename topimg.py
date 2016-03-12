# -*- coding: utf-8 -*-
import cgi
from google.appengine.ext import ndb
import webapp2
import datetime
import time
import numpy
import numpy.random
from pytz.gae import pytz

MAIN_PAGE_HTML = """
<html>
<head>
<body>
"""

END_PAGE_HTML = """
</body>
</html>
"""

class ImageDB(ndb.Model):
    date = ndb.DateTimeProperty('d',auto_now_add=True)
    img  = ndb.BlobProperty('i')

class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.write(MAIN_PAGE_HTML)
        self.response.write("""<h1>Banque d'images de Léry-Poses</h1>""")
        self.response.write("""

<script>
  (function(i,s,o,g,r,a,m){i['GoogleAnalyticsObject']=r;i[r]=i[r]||function(){
  (i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o),
  m=s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m)
  })(window,document,'script','//www.google-analytics.com/analytics.js','ga');

  ga('create', 'UA-65403806-2', 'auto');
  ga('send', 'pageview');

</script>


            <script>

            var curdate;
            var curtime;

            function getpicture() {
                var img = new Image();
                img_src = "http://imagebankleryposes.appspot.com/dispimg?date=";
                img_src = img_src + document.getElementById("datetimeform")[0].value;
                img_src = img_src + "&time=" + document.getElementById("datetimeform")[1].value;
                curdate = document.getElementById("datetimeform")[0].value;
                curtime = document.getElementById("datetimeform")[1].value;
                var node = document.getElementById("pictureform");
                node.innerHTML = "<img src='"+img_src+"'>";
                document.getElementById("currenttime").innerHTML = curtime; 
            }

            function dectimeby1mn(intime) {
                // assume intime has the format HH:MM
                var newmn=parseInt(intime.substring(3,5));
                var newhr=parseInt(intime.substring(0,2));

                if (newmn==0) {
                    newmn=59;
                    if (newhr==0) {
                        newhr=23;
                    } else {
                        newhr = newhr - 1;
                    }
                } else {
                    newmn = newmn - 1;
                }
                var newhr2;
                if (newhr<10) {
                   newhr2 = "0"+newhr.toString();
                } else {
                   newhr2 = newhr.toString();
                }
                var newmn2;
                if (newmn<10) {
                   newmn2 = "0"+newmn.toString();
                } else {
                   newmn2 = newmn.toString();
                }
                return newhr2+":"+newmn2;
            }


            function inctimeby1mn(intime) {
                // assume intime has the format HH:MM
                var newmn=parseInt(intime.substring(3,5));
                var newhr=parseInt(intime.substring(0,2));

                if (newmn==59) { 
                    newmn=0; 
                    if (newhr==23) { 
                        newhr=0; 
                    } else {
                        newhr = newhr + 1;
                    }
                } else {
                    newmn = newmn +1;
                }
                var newhr2;
                if (newhr<10) {
                   newhr2 = "0"+newhr.toString();
                } else {
                   newhr2 = newhr.toString();
                }
                var newmn2;
                if (newmn<10) {
                   newmn2 = "0"+newmn.toString();
                } else {
                   newmn2 = newmn.toString();
                }
                return newhr2+":"+newmn2;
            } 

            function getprevpicture() {
                var img = new Image();
                img_src = "http://imagebankleryposes.appspot.com/dispimg?date=";
                img_src = img_src + curdate;
                curtime = dectimeby1mn(curtime);
                img_src = img_src + "&time=" + curtime;
                var node = document.getElementById("pictureform");
                node.innerHTML = "<img src='"+img_src+"'>";
                document.getElementById("currenttime").innerHTML = curtime;
            }
 
            function getnextpicture() {
                var img = new Image();
                img_src = "http://imagebankleryposes.appspot.com/dispimg?date=";
                img_src = img_src + curdate;
                curtime = inctimeby1mn(curtime);
                img_src = img_src + "&time=" + curtime;
                var node = document.getElementById("pictureform");
                node.innerHTML = "<img src='"+img_src+"'>";
                document.getElementById("currenttime").innerHTML = curtime;
            }

            </script>
        """)
        self.response.write("""<form id="datetimeform">""")
        self.response.write("""Date (JJ-MM-AAAA): <input type="text" name="date"> """)
        self.response.write("""Heure (HH:MM): <input type="text" name="time">""")
        self.response.write("""<input type="button" value="Prev" onclick="getprevpicture()">""")
        self.response.write("""<input type="button" value="Submit" onclick="getpicture()">""")
        self.response.write("""<input type="button" value="Next" onclick="getnextpicture()">""")
        self.response.write("""</form>""")
        self.response.write("""<form id="currenttime">""")
        self.response.write("""<input type="text">""")  
        self.response.write("""</form>""")
        self.response.write("""<form id="pictureform">""")
        self.response.write("""</form>""")
        self.response.write(END_PAGE_HTML)

app = webapp2.WSGIApplication([
    ('/', MainPage),
], debug=True)
