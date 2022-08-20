""" Module config.py - configuration. """
import logging

"""Select logging mode:
INFO - fixings + WARNING, WARNING - dubbs and junk, disable() - disable all. """
LOG_MODE = logging.disable()

""" Select command line width. """
WIN_WIDTH = 99

""" Select CSV encoding. """
ENCODING = 'windows-1251'  # utf-8 или windows-1251
