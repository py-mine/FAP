import importlib
import shutil
import yaml
import git
import os
import re

valid_url_regex = re.compile(
    r'^(?:http)s?://'  # http:// or https://
    # domain...
    r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'
    r'localhost|'  # localhost...
    r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
    r'(?::\d+)?'  # optional port
    r'(?:/?|[/?]\S+)$',
    re.IGNORECASE
)

plugin_dirs = []


def dump_default():
    default = [('https://github.com/py-mine/FAP.git', 'FAP', 'fap')]

    with open('plugins.yml', 'w+') as f:
        f.write(yaml.dump(default))

    return default


def load_plugin_list():
    try:
        with open('plugins.yml', 'r') as f:
            plugin_list = yaml.safe_load(f.read())
    except FileNotFoundError:
        plugin_list = dump_default()

    if plugin_list is None:
        plugin_list = []

    if not isinstance(plugin_list, list):
        plugin_list = dump_default()

    return tuple(plugin_list)


async def setup():
    plugin_dir = os.listdir('plugins')

    # Update self!

    try:
        plugin_dir.remove('fap')
    except ValueError:
        pass
    else:
        fap_dir = os.path.join('plugins', 'FAP')
        fap_repo = git.Git(fap_dir)

        if os.path.isdir(os.path.join(fap_dir, '.git')):
            fap_repo.pull()
        else:
            shutil.rmtree(fap_dir)
            fap_repo.clone('https://github.com/py-mine/FAP.git')

    for plugin_url, plugin_root, plugin_dir in load_plugin_list():
        if re.match(valid_url_regex, plugin_url) is None:
            raise ValueError(f'Entry in plugins.yml "{plugin}" is not a valid git clone/repository url.')

        plugin_repo = git.Git(os.path.join('plugins', plugin_root))

        if not os.path.isdir(plugin_root):
            plugin_repo.clone(plugin_url)
        elif os.path.isdir(os.path.join('plugins', plugin_root, '.git')):
            plugin_repo.pull()

        plugin_dirs.append(os.path.join(plugin_root, plugin_dir).replace('/', '.'))
