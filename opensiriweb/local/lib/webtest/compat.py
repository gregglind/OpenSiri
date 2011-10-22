# -*- coding: utf-8 -*-
import sys

if sys.version_info[0] > 2:
    PY3 = True
    string_types = (str,)
    text_type = str
    binary_type = bytes
    from io import StringIO
    from io import BytesIO
    from urllib.parse import urlencode
    from urllib.parse import splittype
    from urllib.parse import splithost
    import urllib.parse as urlparse
    from http.client import HTTPConnection
    from http.client import CannotSendRequest
    from http.server import HTTPServer
    from http.server import SimpleHTTPRequestHandler
    from http.cookies import SimpleCookie, CookieError
    from http.cookies import _quote as cookie_quote

    def to_bytes(s):
        if isinstance(s, bytes):
            return s
        return s.encode('latin1')

    def to_string(s):
        if isinstance(s, str):
            return s
        return str(s, 'latin1')

    def join_bytes(sep, l):
        l = [to_bytes(e) for e in l]
        return to_bytes(sep).join(l)

else:
    PY3 = False
    string_types = basestring
    text_type = unicode
    binary_type = str
    from urllib import splittype
    from urllib import splithost
    from urllib import urlencode
    from httplib import HTTPConnection
    from httplib import CannotSendRequest
    from BaseHTTPServer import HTTPServer
    from SimpleHTTPServer import SimpleHTTPRequestHandler
    from Cookie import SimpleCookie, CookieError
    from Cookie import _quote as cookie_quote
    try:
        from cStringIO import StringIO
    except ImportError:
        from StringIO import StringIO
    BytesIO = StringIO
    import urlparse

    def to_bytes(s):
        return str(s)

    def to_string(s):
        return str(s)

    def join_bytes(sep, l):
        l = [e for e in l]
        return sep.join(l)


def print_stderr(value):
    if PY3:
        exec('print(value, file=sys.stderr)')
    else:
        exec('print >> sys.stderr, value')
