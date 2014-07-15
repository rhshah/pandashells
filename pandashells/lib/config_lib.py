#! /usr/bin/env python
import os
import sys
import json

CONFIG_FILE_NAME = '.pandashells'


# "notebook", and the other contexts are "paper", "talk", and "poster"

CONFIG_OPTS = sorted([
    ('io_input_type', ['csv', 'table']),
    ('io_output_type', ['csv', 'table', 'html']),
    ('io_input_header', ['header', 'noheader']),
    ('io_output_header', ['header', 'noheader']),
    ('io_output_index', ['noindex', 'index']),
    ('plot_context', ['talk', 'poster', 'paper', 'notebook']),
    ('plot_theme', ['darkgrid', 'whitegrid', 'dark', 'white']),
    ('plot_palette', ['muted', 'deep', 'dark', 'colorblind', 'pastel'])])

DEFAULT_DICT = {t[0]: t[1][0] for t in CONFIG_OPTS}

HOME = os.path.expanduser('~')
CONFIG_FILE_NAME = os.path.join(HOME, CONFIG_FILE_NAME)


# ============================================================================
def set_config(configDict):
    with open(CONFIG_FILE_NAME, 'w') as configFile:
        configFile.write(json.dumps(configDict, indent=2))


# ============================================================================
def get_config():
    if os.path.isfile(CONFIG_FILE_NAME):
        with open(CONFIG_FILE_NAME, 'r') as configFile:
            configDict = json.loads(configFile.read())
    else:
        configDict = DEFAULT_DICT
        set_config(configDict)
    return configDict


# ============================================================================
if __name__ == '__main__':
    print get_config()
