"""
The ``agar.auth`` module contains classes, functions, and decorators to help secure a `webapp2.Requesthandler`_.
"""
from functools import wraps

from agar.config import Config


class AuthConfig(Config):
    """
    :py:class:`~agar.config.Config` settings for the ``agar.auth`` library.
    Settings are under the ``agar_auth`` namespace.

    The following settings (and defaults) are provided::

        agar_auth_AUTHENTICATION_PROPERTY = 'user'
        def agar_auth_authenticate(request):
            return None

    To override ``agar.auth`` settings, define values in the ``appengine_config.py`` file in the root of your project.
    """
    _prefix = 'agar_auth'

    #: The property name under which to place the authentication object on the request.
    AUTHENTICATION_PROPERTY = 'user'
    
    def authenticate(request):
        """
        The authenticate function. It takes a single `webapp2.Request`_ argument, and returns a non-``None`` value if
        the request can be authenticated. If the request can not be authenticated, the function should return ``None``.
        The type of the returned value can be anything, but it should be a type that your `webapp2.RequestHandler`_ expects.
        The default implementation always returns ``None``.

        :param request: The `webapp2.Request`_ object to authenticate.
        :return: A non-``None`` value if the request can be authenticated. If the request can not be authenticated, the
            function should return ``None``.
        """
        return None

#: The configuration object for ``agar.auth`` settings.
config = AuthConfig.get_config()

def authentication_required(authenticate=None, require_https=False):
    """
    A decorator to authenticate a `RequestHandler <http://webapp-improved.appspot.com/api.html#webapp2.RequestHandler>`_.
    If the authenticate function returns a non-``None`` value, it will assign it to the request ``user`` attribute
    (or any re-configured name), that is passed to the decorated handler. If the authenticate function returns ``None``,
    it will call the `webapp2.RequestHandler.abort`_ method with a status of ``403``.

    :param authenticate: The authenticate function to use to authenticate a request. The function should take a single
        `webapp2.Request`_ argument, and return a non-``None`` value if the request can be authenticated. If the request
        can not be authenticated, the function should return ``None``. The type of the returned value can be anything,
        but it should be a type that your `webapp2.RequestHandler`_ expects.
        If ``None``, the config function :py:meth:`~agar.auth.AuthConfig.authenticate` will be used.
    :param require_https: If ``True``, this will enforce that a request was made via HTTPS, otherwise a ``403`` response
        will be returned.
    """
    if authenticate is None:
        authenticate = config.authenticate
    def decorator(request_method):
        @wraps(request_method)
        def wrapped(self, *args, **kwargs):
            if require_https:
                import urlparse
                from agar.env import on_server
                scheme, netloc, path, query, fragment = urlparse.urlsplit(self.request.url)
                if on_server and scheme and scheme.lower() != 'https':
                    self.abort(403)
            authentication = authenticate(self.request)
            if authentication is not None:
                setattr(self.request, config.AUTHENTICATION_PROPERTY, authentication)
                request_method(self, *args, **kwargs)
            else:
                self.abort(403)
        return wrapped
    return decorator

def https_authentication_required(authenticate=None):
    """
    A decorator to authenticate a secure request to a `webapp2.RequestHandler`_.
    """
    return authentication_required(authenticate=authenticate, require_https=True)
