import os
import hashlib
import unittest2
from google.appengine.api import users
from google.appengine.ext import testbed

class BaseTest(unittest2.TestCase):
    """
    A base class for App Engine unit tests that sets up API proxy
    stubs for all available services, using testbed.

    Note: the images stub is only set up if PIL is found.

    To use, simply inherit from this class:

        import agar
        
        class MyTestCase(agar.test.BaseTest):
            
            def test_datastore(self):
                model = MyModel(foo='foo')
                model.put()

                # will always be true because the datastore is cleared
                # between test method runs.
                self.assertEqual(1, MyModel.all().count())
    """

    def setUp(self):
        os.environ['HTTP_HOST'] = 'localhost'

        self.testbed = testbed.Testbed()
        self.testbed.activate()
        
        self.testbed.init_datastore_v3_stub()
        self.testbed.init_memcache_stub()
        self.testbed.init_taskqueue_stub()
        self.testbed.init_urlfetch_stub()
        self.testbed.init_user_stub()
        self.testbed.init_xmpp_stub()
        self.testbed.init_mail_stub()

        try:
            from google.appengine.api.images import images_stub
            self.testbed.init_images_stub()
        except ImportError:
            pass

    def tearDown(self):
        # deactivate testbed; also has effect of clearning any
        # environment variables set during the test.
        self.testbed.deactivate()

    def log_in_user(self, email):
        # stolen from dev_appserver_login
        user_id_digest = hashlib.md5(email.lower()).digest()
        user_id = '1' + ''.join(['%02d' % ord(x) for x in user_id_digest])[:20]

        os.environ['USER_EMAIL'] = email
        os.environ['USER_ID'] = user_id

        return users.User(email=email, _user_id=user_id)
    
    def get_sent_messages(self, to=None, sender=None, subject=None, body=None, html=None):
        return self.testbed.get_stub('mail').get_sent_messages(to=to, sender=sender, subject=subject, body=body, html=html)

    def assertEmailSent(self, to=None, sender=None, subject=None, body=None, html=None):
        messages = self.get_sent_messages(to=to, sender=sender, subject=subject, body=body, html=html)
        self.assertNotEqual(0, len(messages),
                            "No matching email messages were sent.")

    def assertEmailNotSent(self, to=None, sender=None, subject=None, body=None, html=None):
        messages = self.get_sent_messages(to=to, sender=sender, subject=subject, body=body, html=html)
        self.assertLength(0, messages, "Expected no emails to be sent, but %s were sent." % len(messages))

    def assertLength(self, expected, iterable, message=None):
        length = len(list(iterable))
        message = message or 'Expected length: %s but was length: %s' % (expected, length)
        self.assertEqual(expected, length, message)
    
    def assertEmpty(self, iterable):
        self.assertLength(0, iterable)
