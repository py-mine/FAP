import importlib
import shutil
import yaml
import git
import os
import re

DEFAULT = [['https://github.com/py-mine/FAP.git', 'FAP', '']]
VALID_URL_REGEX = re.compile(
    r'^(?:http)s?://'  # http:// or https://
    # domain...
    r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'
    r'localhost|'  # localhost...
    r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
    r'(?::\d+)?'  # optional port
    r'(?:/?|[/?]\S+)$',
    re.IGNORECASE
)

loaded_plugins = []


def dump_default():
    with open('plugins.yml', 'w+') as f:
        f.write(yaml.dump(DEFAULT))

    return DEFAULT.copy()


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

    return plugin_list


async def setup():
    plugins_dir = git.Git('plugins')

    for plugin_url, plugin_root, plugin_dir in load_plugin_list():
        if re.match(VALID_URL_REGEX, plugin_url) is None:
            raise ValueError(f'Entry in plugins.yml "{plugin_url}" is not a valid git clone/repository url.')

        plugin_root = os.path.join('plugins', plugin_root)

        if not os.path.isdir(os.path.join(plugin_root, '.git')):
            shutil.rmtree(plugin_root)
            plugins_dir.clone(plugin_url)  # clone plugin repository to plugins directory
        else:
            res = git.Git(plugin_root).pull()  # update plugin repository

            if res != 'Already up to date.' and plugin_root == 'FAP':  # There was changes
                self = importlib.import_module(os.path.normpath(os.path.join(plugin_root, plugin_dir)).replace('/', '.'))
                await self.setup()
                return

        loaded_plugins.append(os.path.join(plugin_root, plugin_dir).replace('/', '.'))