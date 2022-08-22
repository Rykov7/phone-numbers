""" Module config.py - configuration. """
import logging

"""Select logging mode:
INFO - fixings + WARNING, WARNING - dubbs and junk, disable() - disable all. """
LOG_MODE = logging.disable()

""" Select command line width. """
WIN_WIDTH = 99

""" Select CSV encoding (utf-8 or windows-1251). """
ENCODING_READ = 'windows-1251'
ENCODING_WRITE = 'utf-8'
