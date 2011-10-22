====
agar
====
.. automodule:: agar

---------
agar.auth
---------
.. automodule:: agar.auth
    :members: authentication_required, https_authentication_required, AuthConfig

-----------
agar.config
-----------
.. automodule:: agar.config
.. autoclass:: agar.config.Config
    :members: _prefix, get_config, get_config_as_dict

----------
agar.dates
----------
.. automodule:: agar.dates
    :members:

-----------
agar.django
-----------
.. automodule:: agar.django

^^^^^^^^^^^^^^^^^^^^^^
agar.django.decorators
^^^^^^^^^^^^^^^^^^^^^^
.. automodule:: agar.django.decorators
    :members:

^^^^^^^^^^^^^^^^^^^^^^
agar.django.forms
^^^^^^^^^^^^^^^^^^^^^^
.. automodule:: agar.django.forms
    :members:

--------
agar.env
--------
.. automodule:: agar.env
    :members:

----------
agar.image
----------
.. automodule:: agar.image
.. autoclass:: agar.image.Image()
    :members:
    :exclude-members: create

    .. automethod:: create(blob_info=None, data=None, filename=None, url=None, mime_type=None, parent=None, key_name=None)

.. autoclass:: agar.image.ImageConfig
    :members:

---------
agar.json
---------
.. autoclass:: agar.json.JsonRequestHandler
    :members:
    :undoc-members:

.. autoclass:: agar.json.MultiPageHandler
    :members:
    :undoc-members:

.. autoclass:: agar.json.CorsMultiPageHandler
    :members:

-----------
agar.models
-----------
.. automodule:: agar.models

.. autoclass:: agar.models.NamedModel
    :members:
    :exclude-members: create_new_entity

    .. automethod:: create_new_entity(key_name=None, parent=None, \*\*kwargs)

.. autoclass:: DuplicateKeyError
.. autoclass:: ModelException

-------------
agar.sessions
-------------
.. automodule:: agar.sessions
    :members:

-----------------
agar.templatetags
-----------------
.. autodata:: agar.templatetags.webapp2.url_for
.. autodata:: agar.templatetags.webapp2.on_production_server

--------
agar.url
--------
.. automodule:: agar.url

.. autofunction:: agar.url.uri_for

.. autoclass:: agar.url.UrlConfig
    :members:

.. Links

.. _Google App Engine python: http://code.google.com/appengine/docs/python/overview.html
.. _Key: http://code.google.com/appengine/docs/python/datastore/keyclass.html
.. _key().name(): http://code.google.com/appengine/docs/python/datastore/keyclass.html#Key_name
.. _Model: http://code.google.com/appengine/docs/python/datastore/modelclass.html
.. _Query: http://code.google.com/appengine/docs/python/datastore/queryclass.html
.. _Blobstore: http://code.google.com/appengine/docs/python/blobstore/
.. _BlobInfo: http://code.google.com/appengine/docs/python/blobstore/blobinfoclass.html
.. _BlobKey: http://code.google.com/appengine/docs/python/blobstore/blobkeyclass.html
.. _BlobReader: http://code.google.com/appengine/docs/python/blobstore/blobreaderclass.html
.. _Image: http://code.google.com/appengine/docs/python/images/imageclass.html
.. _Image.format: http://code.google.com/appengine/docs/python/images/imageclass.html#Image_format
.. _Image.width: http://code.google.com/appengine/docs/python/images/imageclass.html#Image_width
.. _Image.height: http://code.google.com/appengine/docs/python/images/imageclass.html#Image_height
.. _Image.get_serving_url: http://code.google.com/appengine/docs/python/images/functions.html#Image_get_serving_url
.. _google.appengine.api.lib_config: http://code.google.com/p/googleappengine/source/browse/trunk/python/google/appengine/api/lib_config.py

.. _django: http://www.djangoproject.com/
.. _django forms: https://docs.djangoproject.com/en/dev/topics/forms/
.. _django form class: https://docs.djangoproject.com/en/1.3/ref/forms/api/#django.forms.Form
.. _django template tags: https://docs.djangoproject.com/en/dev/howto/custom-template-tags/

.. _webapp2: http://code.google.com/p/webapp-improved/
.. _webapp2 configuration: http://webapp-improved.appspot.com/guide/app.html#guide-app-config
.. _webapp2 extras: http://webapp-improved.appspot.com/#api-reference-webapp2-extras
.. _webapp2_extras.sessions: http://webapp-improved.appspot.com/api/webapp2_extras/sessions.html
.. _webapp2_extras.sessions.SessionStore: http://webapp-improved.appspot.com/api/webapp2_extras/sessions.html#webapp2_extras.sessions.SessionStore
.. _webapp2.WSGIApplication: http://webapp-improved.appspot.com/api/webapp2.html#webapp2.WSGIApplication
.. _webapp2.Request: http://webapp-improved.appspot.com/api/webapp2.html#webapp2.Request
.. _webapp2.Response: http://webapp-improved.appspot.com/api/webapp2.html#webapp2.Response
.. _webapp2.RequestHandler: http://webapp-improved.appspot.com/api/webapp2.html#webapp2.RequestHandler
.. _webapp2.RequestHandler.abort: http://webapp-improved.appspot.com/api/webapp2.html#webapp2.RequestHandler.abort
.. _webapp2.uri_for: http://webapp-improved.appspot.com/api/webapp2.html#webapp2.uri_for
.. _uuid4: http://docs.python.org/library/uuid.html#uuid.uuid4

.. _mime type: http://en.wikipedia.org/wiki/Internet_media_type
