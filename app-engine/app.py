# To push new version to app engine /usr/local/google_appengine/appcfg.py --noauth_local_webserver --oauth2 update ./

import webapp2

from google.appengine.ext import ndb

class TorRelays(ndb.Model):
    name = ndb.StringProperty()
    last_check_in = ndb.DateTimeProperty()
    guard = ndb.BooleanProperty()
    tor_pid = ndb.BooleanProperty()
    responsive = ndb.BooleanProperty()
    net_connections = ndb.IntegerProperty()

class MonitoredData(ndb.Model):
    tor_relay = ndb.KeyProperty(kind=TorRelays)

class Names(ndb.Model):
    name = ndb.StringProperty()


class MainPageHandler(webapp2.RequestHandler):
    # def get(self):
    #     # Updates to database (probably a post)
    #     name = self.request.get('q')
    #     name_model = Name(name = name)
    #     name_model.put()
    #     self.response.out.write('Hello ' + self.request.get('q'))

    # def get(self):
    #     # Updates to database (probably a post)
    #     name = self.request.get('q')
    #     name_model = TorRelays(name = name)
    #     name_model.put()
    #     self.response.out.write('Hello ' + self.request.get('q'))

    def get(self):
        name = self.request.get('q')
        name_model = Names(name = name)
        name_model.put()
        self.response.out.write('Hello ' + self.request.get('q'))

        # Android data pulls

    # def put(self):
    #     heartbeat = journal.Entry(
    #         user=user,
    #         key_name=user_id + ':' + str(ujd.last_entry),
    #         start_time=start_time,
    #         text=text,
    #         end_time=end_time,
    #         source=source)
    #     entry.put()

# Web App 2 framework stuff (when a request comes in on this path, had it off to this thing):
app = webapp2.WSGIApplication([
    webapp2.Route(r'/', handler=MainPageHandler, name='home'),
    ],
    debug=True)
