# To push new version to app engine /usr/local/google_appengine/appcfg.py --noauth_local_webserver --oauth2 update ./

import webapp2
from pyfcm import FCMNotification
import socket

from google.appengine.ext import ndb
from google.appengine.api import urlfetch

# Ask Rhett to explain datastore model
class TorRelays(ndb.Model):
    name = ndb.StringProperty()
    # last_check_in = ndb.DateTimeProperty()
    # guard = ndb.BooleanProperty()
    # tor_pid = ndb.BooleanProperty()
    # responsive = ndb.BooleanProperty()
    # net_connections = ndb.IntegerProperty()

class Heartbeats(ndb.Model):
    tor_relay = ndb.KeyProperty(kind=TorRelays)
    name = ndb.StringProperty()
    last_check_in = ndb.DateTimeProperty()
    guard = ndb.BooleanProperty()
    tor_pid = ndb.BooleanProperty()
    responsive = ndb.BooleanProperty()
    net_connections = ndb.IntegerProperty()

class MainPageHandler(webapp2.RequestHandler):
    # SEnd push notifications to Android
    # Post request from torrelaymon
    # rrespond to Get requests fron Android to display last status

    def fcm_send(self):
        pass
        # response = urlfetch.fetch(
        #     url="https://fcm.googleapis.com/fcm/send",
        #     payload="hello",
        #     method=urlfetch.POST,
        #     headers={
        #          'Content-Type': 'application/json',
        #          'Authorization': 'key='
        #      })
        # return response

        # Send notifications to single device.

    def get(self):
        # Updates to database (probably a post)
        name = self.request.get('q')
        name_model = Heartbeats(name = name)
        name_model.put()
        self.fcm_send()
        self.response.out.write('Hello ' + self.request.get('q'))
        # self.fail_check(heartbeat)

#              https://fcm.googleapis.com/fcm/send
# Content-Type:application/json
# Authorization:key=
#
# { "data": {
#     "score": "5x1",
#     "time": "15:10"
#   },
#   "to" : ""
# }

          #       def UpdateRegisteredClients(ujd):
          # # Skip if the user has not registered for GCM
          # if len(ujd.registration_ids) == 0:
          #   return
          # gcmPush = {
          #   # No need to send every message, we only send a message saying we need to
          #   # sync.
          #   "collapse_key": "new_entry",
          #   # No need to wake the device.
          #   "delay_while_idle": True,
          #   "registration_ids": ujd.registration_ids
          # }
          # response = urlfetch.fetch(
          #     url="https://android.googleapis.com/gcm/send",
          #     payload=json.dumps(gcmPush),
          #     method=urlfetch.POST,
          #     headers={
          #         'Content-Type': 'application/json',
          #         'Authorization': ''
          #     })
          # logging.info('push: ' + str(response.status_code) + ': ' + response.content)


        # Android data pulls

    # def fail_check(self, heartbeat):
    #     pass

push_service = FCMNotification(api_key="")

message_title = "Tor relay status"
message_body = "Your relay is having some troubles"
firebase_result = push_service.notify_single_device(registration_id="", message_title=message_title, message_body=message_body)

print firebase_result

# Web App 2 framework stuff (when a request comes in on this path, hand it off to this thing):
app = webapp2.WSGIApplication([
    webapp2.Route(r'/', handler=MainPageHandler, name='home'),
    ],
    debug=True)
