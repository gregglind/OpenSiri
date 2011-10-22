""" Run an interactive console after including AppEngine and project libraries. """

from google.appengine.tools import os_compat

import getopt
import logging
import os
import signal
import sys
import traceback
import tempfile

logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)-8s %(asctime)s %(filename)s:%(lineno)s] %(message)s')

from google.appengine.api import yaml_errors
from google.appengine.dist import py_zipimport
from google.appengine.tools import appcfg
from google.appengine.tools import appengine_rpc
from google.appengine.tools import dev_appserver
from google.appengine.tools import dev_appserver_main

config = matcher = None

try:
    config, matcher = dev_appserver.LoadAppConfig(".", {})
except yaml_errors.EventListenerError, e:
    logging.error('Fatal error when loading application configuration:\n' +
                                    str(e))
except dev_appserver.InvalidAppConfigError, e:
    logging.error('Application configuration file invalid:\n%s', e)


dev_appserver.SetupStubs(config.application, **dev_appserver_main.DEFAULT_ARGS)
#os.environ['APPLICATION_ID'] = config.application

"""
datastore_path = dev_appserver.DEFAULT_ARGS[dev_appserver.ARG_DATASTORE_PATH]
history_path = dev_appserver.DEFAULT_ARGS[dev_appserver.ARG_HISTORY_PATH]

apiproxy_stub_map.apiproxy = apiproxy_stub_map.APIProxyStubMap()
if False: #use_sqlite:
    from google.appengine.datastore import datastore_sqlite_stub
    stub = datastore_sqlite_stub.DatastoreSqliteStub(appid, datastore_path,
                history_path)
else:
    stub = datastore_file_stub.DatastoreFileStub(appid, datastore_path,
                history_path)
    apiproxy_stub_map.apiproxy.RegisterStub('datastore_v3', stub)

"""

if __name__ == "__main__":
    banner = "Interactive App Engine Shell for app-id '%s'" % config.application
    try:
        import IPython
        sh = IPython.Shell.IPShellEmbed(argv='', banner=banner)
        sh(global_ns={}, local_ns={})
    except:
        import code
        console = code.InteractiveConsole()
        console.interact(banner)
