#! /usr/bin/env python

import webapp2
from datetime import datetime
from google.appengine.ext import ndb
import app

class MainPageHandler(webapp2.RequestHandler):
    def get(self):
        query = app.Heartbeats.query()
        last = query.order(-app.Heartbeats.last_check_in).get();
        current_time = datetime.now()
        diff = current_time - last.last_check_in
        min_diff = diff.total_seconds() / 60
        if min_diff > 3 and last.server_responsive == True and last.name == "Testing":
            app.fcm_send("Tor server unresponsive")
            last.server_responsive = False
            last.put()
        else:
            last.server_responsive = True
            last.put()
        self.response.out.write(min_diff)

status = webapp2.WSGIApplication([
    webapp2.Route(r'/status', handler=MainPageHandler, name='status'),
    ],
    debug=True)

# dev_appserver.py ./ --port=8080 --admin_port=8000
