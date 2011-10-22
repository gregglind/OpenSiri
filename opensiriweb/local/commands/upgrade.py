""" Pulls the latest version of substrate to ~/.substrate and replaces the project files."""

import argparse
import os
import shutil
import yaml

from subprocess import call

# TODO can we assume no user libs are in local/lib?
# TODO add user_lib for these?
# TODO use hg tags for releases?  major/minor/dev(default) options?
# TODO make substrate repo public
# TODO check to see if project to be upgraded has no uncommitted files



if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--url', help='The hg repository url to use for upgrading substrate.')
    parser.add_argument('--reset-url', help='Uses the default repository for upgrades.')
    parser.add_argument('--local-only', help='Substrate env files only (manage.py, local/*, etc)')
    args = parser.parse_args()
    
    agar = ['env_setup.py', 'lib/agar']
    upgrade_items = ['manage.py', 'local/commands', 'local/lib']

    if not args.local_only:
        upgrade_items += agar

    current_dir = os.path.abspath('.')
    substrate_home_dir = os.path.expanduser('~/.substrate')
    substrate_repo = os.path.expanduser('%s/substrate' % substrate_home_dir)
    settings_yaml = '%s/%s' % (substrate_home_dir, 'settings.yaml')

    if not os.path.isdir(substrate_home_dir):
        os.mkdir(os.path.expanduser(substrate_home_dir))

    if not os.path.isfile(settings_yaml):
        _file = open(settings_yaml, 'w')
        y = yaml.load('version: 1')
        yaml.dump(y, stream=_file, default_flow_style=False)
        _file.close()
    
    if args.url:
        _file = open(settings_yaml, 'r+')
        y = yaml.load(_file)
        y['url'] = os.path.expanduser(args.url)
        _file.seek(0)
        _file.truncate()
        yaml.dump(y, stream=_file, default_flow_style=False)
        _file.close()
    
    if args.reset_url:
        _file = open(settings_yaml, 'r+')
        y = yaml.load(_file)
        if y.get('url'):
            del y['url']
            _file.seek(0)
            _file.truncate()
            yaml.dump(y, stream=_file, default_flow_style=False)
        _file.close()
    
    settings = yaml.load(open(settings_yaml, 'r'))
    if settings.get('url'):
        upgrade_url = settings.get('url')
    else:
        upgrade_url = 'default url'
    
    print 'URL of merurial repo to be used for upgrade: %s' % upgrade_url

    confirm = raw_input('This will delete and copy substrate files/dirs, continue? (y/N) ')

    if not confirm or confirm.upper() != 'Y':
        print 'Upgrade canceled.'
        import sys
        sys.exit(1)

    if os.path.isdir(substrate_repo):
        pull = ['hg', 'pull']
        up = ['hg', 'update', '-C']

        if settings.get('url'):
            pull.append(settings.get('url'))

        call(pull, cwd=substrate_repo)
        call(up, cwd=substrate_repo)
    else:
        url = 'ssh://hg@bitbucket.org/gumptioncom/substrate'
        clone = ['hg', 'clone', url, substrate_repo]
        call(clone, cwd=substrate_home_dir)


    for item in upgrade_items:
        item_path = '%s/%s' % (substrate_repo, item)

        if os.path.isfile(item_path):
            print 'Replacing project file: %s' % item
            shutil.copy(item_path, current_dir)
        
        if os.path.isdir(item_path):
            print 'Replacing project dir: %s' % item
            shutil.rmtree('%s/%s' % (current_dir, item))
            shutil.copytree(item_path, '%s/%s' % (current_dir, item))
