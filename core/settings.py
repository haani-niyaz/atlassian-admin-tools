#!/usr/bin/env python

import os

import simplejson as json


class ConfigFileError(Exception):
    """An error that occurs when reading a config file"""
    pass


def read_config_file(file):
    """Returns a dictionary of objects created from a JSON config file"""

    if not os.path.exists(file):
        raise ConfigFileError("Ensure config file path is valid")
    # Nesting required to use 'finally' prior to python 2.5
    try:
        try:
            fh = open(file, 'r')
            return json.load(fh)
        except ValueError, e:
            raise ConfigFileError(
                "Configuration file has an error. %s while attempting to open %s" % (str(e), file))
    finally:
        fh.close()
