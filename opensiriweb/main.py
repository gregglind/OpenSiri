#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import cgi
import os

from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
from google.appengine.ext import db
from google.appengine.api import users
from google.appengine.ext.webapp import template


## since I am clearly an idiot and can't figure this out...!
TEMPLATE_DIRS = ['templates',]

def render(fname,template_values):
    """ """
    for D in TEMPLATE_DIRS:
        path = os.path.join(os.path.dirname(__file__),D, fname)
        return template.render(path,template_values)


class SiriInteraction(db.Model):
    """Models an individual Guestbook entry with an author, content, and date."""
    author = db.UserProperty()
    asked = db.StringProperty(multiline=True)
    said = db.StringProperty(multiline=True)
    action = db.StringProperty()
    date = db.DateTimeProperty(auto_now_add=True)
    tags = db.StringListProperty()
    verified = db.BooleanProperty(default=False)
    correctaction =  db.BooleanProperty(default=False)

class MainHandler(webapp.RequestHandler):
    def get(self):
        d = dict(knownactions=sorted(['map','alarm','note','phone','ipod','music',
            'messages','calendar','reminders','email','weather','stocks',
            'clock','timer','address-book', 'web', 'wolfram-alpha' ]))
        self.response.out.write(render('index.html',d))

    def post(self):
        asked = self.request.get('asked')
        said = self.request.get('said')
        action = self.request.get('action')
        siri = SiriInteraction(asked=asked,said=said,action=action)
        
        if users.get_current_user():
            siri.author = users.get_current_user()

        siri.put()
        self.redirect('/recent')


class RecentHandler(webapp.RequestHandler):
    def get(self):
        siris = db.GqlQuery("SELECT * "
                            "FROM SiriInteraction "
                            "ORDER BY date DESC LIMIT 100",)
        
        self.response.out.write(render('recent.html',dict(recent=siris)))

class UserHandler(webapp.RequestHandler):
    def get(self):
        user = users.get_current_user()

        if user:
            self.response.headers['Content-Type'] = 'text/plain'
            self.response.out.write('Hello, ' + user.nickname())
        else:
            self.redirect(users.create_login_url(self.request.uri))


# i am sure this bs is already done too!  REINVENTED WHEEL...
class T(webapp.RequestHandler):
    def get(self):
        d = dict(knownactions=['map','alarm','note',])
        self.response.out.write(render('index.html',d))


def main():
    application = webapp.WSGIApplication([('/', MainHandler),
                                          ('/user',UserHandler),
                                          ('/recent',RecentHandler),
                                        ],
                                         debug=True)
    util.run_wsgi_app(application)


if __name__ == '__main__':
    main()
