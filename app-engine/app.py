# To push new version to app engine /usr/local/google_appengine/appcfg.py --noauth_local_webserver --oauth2 update ./

import webapp2
from pyfcm import FCMNotification
import socket

from google.appengine.ext import ndb
from google.appengine.api import urlfetch

# Ask Rhett to explain datastore model
class TorRelays(ndb.Model):
    name = ndb.StringProperty()

class Heartbeats(ndb.Model):
    tor_relay = ndb.KeyProperty(kind=TorRelays)
    name = ndb.StringProperty()
    # This is not something I want to pass in the heartbeat but set when the heartbeat received
    last_check_in = ndb.DateTimeProperty()
    # I'll add this once I can figure out how to get this info from Tor
    # guard = ndb.BooleanProperty()
    tor_pid = ndb.BooleanProperty()
    net_connections = ndb.IntegerProperty()

class MainPageHandler(webapp2.RequestHandler):

    def get(self):
        # Updates to database (probably a post)
        name = self.request.get('name')
        name_model = Heartbeats(name = name)
        name_model.put()
        tor_pid = self.request.get('tor_pid')
        if tor_pid == "True":
            tor_pid = True
        else:
            tor_pid = False
        tor_pid_model = Heartbeats(tor_pid = tor_pid)
        tor_pid_model.put()
        self.response.out.write('Hello ' + name + ' Your Tor Pid is: ' + str(tor_pid))
        # self.fail_check(heartbeat)
        title = "hello there"
        heartbeat_check(name, tor_pid)

    def post(self):
        # Updates to database (probably a post)
        name = self.request.get('name')
        name_model = Heartbeats(name = name)
        name_model.put()
        tor_pid = self.request.get('tor_pid')
        if tor_pid == "True":
            tor_pid = True
        else:
            tor_pid = False
        tor_pid_model = Heartbeats(tor_pid = tor_pid)
        tor_pid_model.put()
        self.response.out.write('Hello ' + name + ' Your Tor Pid is: ' + str(tor_pid))
        # self.fail_check(heartbeat)
        title = "hello there"
        heartbeat_check(name, tor_pid)

def heartbeat_check(name, tor_pid):
    net_connections = 4

    if name != "bob":
        fcm_send(name + ' is not correct')
    if tor_pid == False:
        fcm_send('Tor process is down')
    if net_connections < 3:
        fcm_send('Drop in Tor traffic')


def fcm_send(title):
    push_service = FCMNotification(api_key="")

    message_title = "Tor relay status"
    message_body = title
    firebase_response = push_service.notify_single_device(registration_id="", message_title=message_title, message_body=message_body)

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
