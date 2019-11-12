"""
Config Parse class. It is responsible to parse config.txt file.
"""
from configparser import ConfigParser


class Config:
    """Config class."""
    # Load config file
    config = ConfigParser()
    config.read('config.txt')

    # TODO: check duplicate values
    # (keys that have been assigned to more that one commands)

    # Load config data
    colors = config['colors']
    keys = config['keys']
