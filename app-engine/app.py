import webapp2
from pyfcm import FCMNotification
import socket
from datetime import datetime
from google.appengine.ext import db
from google.appengine.ext import ndb
from google.appengine.api import urlfetch

# Ask Rhett to explain datastore model
class TorRelays(ndb.Model):
    name = ndb.StringProperty()

class Heartbeats(ndb.Model):
    # tor_relay = ndb.KeyProperty(kind=TorRelays)
    name = ndb.StringProperty()
    # This is not something I want to pass in the heartbeat but set when the heartbeat received
    last_check_in = ndb.DateTimeProperty()
    # I'll add this once I can figure out how to get this info from Tor
    # guard = ndb.BooleanProperty()
    tor_pid = ndb.BooleanProperty()
    net_connections = ndb.IntegerProperty()

class MainPageHandler(webapp2.RequestHandler):
    def get(self):
        # q = get_records()
        # q = Heartbeats.query().order(Heartbeats.name)
        # self.response.out.write(str(q))
        query = Heartbeats.query()
        last = query.order(-Heartbeats.last_check_in).get()
        self.response.out.write(str(last))

    def post(self):
        # Updates to database (probably a post)
        name = self.request.get('name')
        heartbeat = Heartbeats(name = name)
        if self.request.get('tor_pid') == "True":
            pid = True
        else:
            pid = False
        heartbeat.tor_pid = pid
        # heartbeat.last_check_in = str(datetime.now())
        heartbeat.net_connections = int(self.request.get('net_connections'))
        heartbeat.put()
        self.response.out.write('Hello ' + name + ' Your Tor Pid is: ' + str(pid))
        heartbeat_check(name, pid)

def heartbeat_check(name, pid):
    net_connections = 4

    if pid == False:
        fcm_send('Tor process is down')
    if net_connections < 3:
        fcm_send('Drop in Tor traffic')

def fcm_send(title):
    push_service = FCMNotification(api_key="")

    message_title = "Tor relay status"
    message_body = title
    firebase_response = push_service.notify_single_device(registration_id="", message_title=message_title, message_body=message_body)

@db.transactional
def get_records():
    return Heartbeats.get_by_id(6315704580046848)

# Web App 2 framework stuff (when a request comes in on this path, hand it off to this thing):
app = webapp2.WSGIApplication([
    webapp2.Route(r'/', handler=MainPageHandler, name='home'),
    ],
    debug=True)

# Old Code:

#              https://fcm.googleapis.com/fcm/send
# Content-Type:application/json
# Authorization:key=
#
# { "data": {
#     "score": "5x1",
#     "time": "15:10"
#   },
#   "to" : "..."
# }

#       def UpdateRegisteredClients(ujd):
# # Skip if the user has not registered for GCM
# if len(ujd.registration_ids) == 0:
#   return
# heartbeat = {
#   # No need to send every message, we only send a message saying we need to
#   # sync.
#   "collapse_key": "new_entry",
#   # No need to wake the device.
#   "delay_while_idle": True,
#   "registration_ids": ujd.registration_ids
# }
# response = urlfetch.fetch(
#     url="https://android.googleapis.com/gcm/send",
#     payload=json.dumps(heartbeat),
#     method=urlfetch.POST,
#     headers={
#         'Content-Type': 'application/json',
#         'Authorization': 'key='
#     })
# logging.info('push: ' + str(response.status_code) + ': ' + response.content)


# Android data pulls

# To push new version to app engine /usr/local/google_appengine/appcfg.py --noauth_local_webserver --oauth2 update ./
