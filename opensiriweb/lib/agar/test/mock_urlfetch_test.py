from google.appengine.api import apiproxy_stub
from google.appengine.api import urlfetch
from google.appengine.api.urlfetch import DownloadError

from google.appengine.ext import testbed

from agar.test import BaseTest

class MockURLFetchServiceStub(apiproxy_stub.APIProxyStub):

    _responses = {}
    
    def __init__(self, service_name='urlfetch'):
        super(MockURLFetchServiceStub, self).__init__(service_name)

    @classmethod
    def set_response(cls, url, content, status_code=None, headers=None):
        MockURLFetchServiceStub._responses[url] = {'content': content,
                                                   'status_code': status_code,
                                                   'headers': headers}
    @classmethod
    def clear_responses(cls):
        MockURLFetchServiceStub._responses.clear()
            
    def _Dynamic_Fetch(self, request, response):
        url = request.url()
        http_response = MockURLFetchServiceStub._responses.get(url)

        if http_response is None:
            raise Exception("No HTTP response was found for the URL '%s' %s" % (url, repr(MockURLFetchServiceStub._responses)))

        if isinstance(http_response['content'], DownloadError):
            raise http_response['content']

        response.set_statuscode(http_response.get('status_code') or 200)
        response.set_content(http_response.get('content'))

        if http_response.get('headers'):
            for header_key, header in http_response['headers']:
                header_proto = response.add_header()
                header_proto.set_key(header_key)
                header_proto.set_value(header_value)



class MockUrlfetchTest(BaseTest):
    def setUp(self):
        super(MockUrlfetchTest, self).setUp()

        stub = MockURLFetchServiceStub()
        self.testbed._register_stub(testbed.URLFETCH_SERVICE_NAME, stub)

    def tearDown(self):
        MockURLFetchServiceStub.clear_responses()
        super(MockUrlfetchTest, self).tearDown()
        
    def set_response(self, url, content, status_code=None, headers=None):
        MockURLFetchServiceStub.set_response(url, content, status_code, headers)
