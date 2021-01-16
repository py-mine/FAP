import importlib
import yaml
import os
import re

valid_url_regex = re.compile(
    r'^(?:http)s?://'  # http:// or https://
    r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...
    r'localhost|'  # localhost...
    r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
    r'(?::\d+)?'  # optional port
    r'(?:/?|[/?]\S+)$',
    re.IGNORECASE
)


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

    for plugin_url, plugin_root, plugin_dir in load_plugin_list():
        if re.match(valid_url_regex, plugin_url) is None:
            raise ValueError(f'Entry in plugins.yml "{plugin}" is not a valid git clone/repository url.')
            continue

        if not os.path.isdir(plugin_root):
            pass  # clone the repo
        elif os.path.isdir(plugin_root + os.sep + '.git'):
            pass  # pull latest from repo
