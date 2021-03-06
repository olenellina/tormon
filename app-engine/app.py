import webapp2
from pyfcm import FCMNotification
import socket
from datetime import datetime
from google.appengine.ext import db
from google.appengine.ext import ndb
from google.appengine.api import urlfetch
import json

class TorRelays(ndb.Model):
    name = ndb.StringProperty()

class Heartbeats(ndb.Model):
    # tor_relay = ndb.KeyProperty(kind=TorRelays)
    name = ndb.StringProperty()
    last_check_in = ndb.DateTimeProperty()
    guard = ndb.BooleanProperty()
    tor_pid = ndb.BooleanProperty()
    net_connections = ndb.IntegerProperty()
    server_responsive = ndb.BooleanProperty()
    low_connections = ndb.BooleanProperty()
    tor_down = ndb.BooleanProperty()

class MainPageHandler(webapp2.RequestHandler):
    def get(self):
        query = Heartbeats.query()
        last = query.order(-Heartbeats.last_check_in).get()
        last_check = last.last_check_in.strftime('%m/%d/%Y %H:%M:%S %Z')
        current_time = datetime.now()
        diff = current_time - last.last_check_in
        min_diff = diff.total_seconds() / 60
        dmp = {
        "name": last.name,
        "check_in": last_check,
        "tor_pid": last.tor_pid,
        "net_connections": last.net_connections,
        "server_responsive": last.server_responsive,
        "min_diff": int(round(min_diff)),
        "guard": last.guard
        }
        self.response.out.write(json.dumps(dmp))

    def post(self):
        query = Heartbeats.query()
        pre_entry = query.order(-Heartbeats.last_check_in).get()
        name = self.request.get('name')
        heartbeat = Heartbeats(name = name)
        if self.request.get('tor_pid') == "True":
            pid = True
        else:
            pid = False
        if self.request.get('guard') == "True":
            guard_status = True
        else:
            guard_status = False
        heartbeat.guard = guard_status
        heartbeat.tor_pid = pid
        heartbeat.last_check_in = datetime.now()
        connections = int(self.request.get('net_connections'))
        heartbeat.server_responsive = True
        heartbeat.low_connections = False
        heartbeat.tor_down = False
        heartbeat.net_connections = connections
        key2 = heartbeat.put()
        self.response.out.write('Hello ' + name + ' Your Tor Pid is: ' + str(pid))
        heartbeat_check(name, pid, pre_entry, key2)

def heartbeat_check(connections, pid, pre_entry, key2):
    this_entry = key2.get()
    if pid == False and pre_entry.tor_down == False:
        fcm_send('Tor process is down')
        this_entry.tor_down = True
        this_entry.put()
    elif pid == False and pre_entry.tor_down == True:
        this_entry.tor_down = True
        this_entry.put()
    if connections < 3 and pre_entry.low_connections == False:
        fcm_send('Drop in Tor traffic')
        this_entry.low_connections = True
        this_entry.put()
    elif connections < 3 and pre_entry.low_connections == True:
        this_entry.tor_down = True
        this_entry.put()


def fcm_send(title):
    push_service = FCMNotification(api_key="")
    message_title = "Tor relay status"
    message_body = title
    firebase_response = push_service.notify_single_device(registration_id="", message_title=message_title, message_body=message_body)

app = webapp2.WSGIApplication([
    webapp2.Route(r'/', handler=MainPageHandler, name='home'),
    ],
    debug=True)

# To push new version to app engine /usr/local/google_appengine/appcfg.py --noauth_local_webserver --oauth2 update ./
