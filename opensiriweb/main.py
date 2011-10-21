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


from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
from google.appengine.ext import db
from google.appengine.api import users
from google.appengine.ext.webapp import template



t = """
<form method="POST" action=''>
<textarea name='asked'>what did you ask Siri to do?</textarea>
<br />
<textarea name='got'>what was her response?</textarea>
<input type='submit' />
</form>


<p>other possible actions:  verfiy, view leaderboard, read discussion</p>
"""

class SiriReport(db.Model):
    """Models an individual Guestbook entry with an author, content, and date."""
    author = db.UserProperty()
    asked = db.StringProperty(multiline=True)
    got = db.StringProperty(multiline=True)
    date = db.DateTimeProperty(auto_now_add=True)
    

class MainHandler(webapp.RequestHandler):
    def get(self):
        self.response.out.write(t)

    def post(self):
        
        asked = self.request.get('asked')
        got = self.request.get('got')
        siri = SiriReport(asked=asked,got=got)
        
        if users.get_current_user():
            siri.author = users.get_current_user()

        siri.put()
        self.response.out.write('<html><body>You wrote:<pre>')
        self.response.out.write(cgi.escape(asked))
        self.response.out.write(cgi.escape(got))
        self.response.out.write('</pre></body></html>')


class ViewAll(webapp.RequestHandler):
    def get(self):
        greetings = db.GqlQuery("SELECT * "
                            "FROM SiriReport "
                            "ORDER BY date DESC LIMIT 1000",)
        
        for g in greetings:
            self.response.out.write('<p>%s</p>' % g)

class UserHandler(webapp.RequestHandler):
    def get(self):
        user = users.get_current_user()

        if user:
            self.response.headers['Content-Type'] = 'text/plain'
            self.response.out.write('Hello, ' + user.nickname())
        else:
            self.redirect(users.create_login_url(self.request.uri))


def main():
    application = webapp.WSGIApplication([('/', MainHandler),
                                          ('/user',UserHandler),
                                          ('/all',ViewAll),
                                        ],
                                         debug=True)
    util.run_wsgi_app(application)


if __name__ == '__main__':
    main()
