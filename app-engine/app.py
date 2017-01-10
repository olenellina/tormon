# To push new version to app engine /usr/local/google_appengine/appcfg.py --noauth_local_webserver --oauth2 update ./

import webapp2

from google.appengine.ext import ndb

class Names(ndb.Model):
    name = ndb.StringProperty()

class Heartbeats(ndb.Model):
    # type pass in Python for empty blocks
   pass

class MainPageHandler(webapp2.RequestHandler):
    def get(self):
        # Updates to database (probably a post)
        name = self.request.get('q')
        name_model = Names(name = name)
        name_model.put()
        self.response.out.write('Hello ' + self.request.get('q'))

        # Android data pulls

# Web App 2 framework stuff (when a request comes in on this path, had it off to this thing):
app = webapp2.WSGIApplication([
    webapp2.Route(r'/', handler=MainPageHandler, name='home'),
    ],
    debug=True)
