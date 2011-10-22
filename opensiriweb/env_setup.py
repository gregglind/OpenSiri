"""
Functions to initialize environment settings.
"""

def setup():
    """Adds <project_root>/lib to the python path.  
    
    Starts in current working directory and traverses up until app.yaml is found.
    Assumes app.yaml is in project root.
    """
    import os, sys
    start_path = os.path.abspath('.')
    search_path = start_path
    while search_path:
        app_yaml_path = os.path.join(search_path, 'app.yaml')
        if os.path.exists(app_yaml_path):
            lib_path = os.path.join(search_path, 'lib')
            if lib_path not in sys.path:
                sys.path.insert(0, lib_path)
            break
        search_path, last_dir = os.path.split(search_path)
    else:
        raise os.error('app.yaml not found for env_setup.setup().%sSearch started in: %s'% (os.linesep, start_path))

def setup_django(settings='settings', version='1.2', ):
    """
    Sets up the django libraries.

    :param settings: The name of the settings file. Default: ``'settings'``.
    :param version: The django version to set up. Default: ``'1.2'``.
    """
    import os
    os.environ['DJANGO_SETTINGS_MODULE'] = settings
    from google.appengine.dist import use_library
    use_library('django', version)
    from django.conf import settings
    _ = settings.TEMPLATE_DIRS
