""" Module config.py - configuration. """
import logging

"""Select logging mode for Fixer:
INFO - fixings + WARNING, WARNING - dubbs and junk, disable() - disable all. """
LOG_LEV = logging.disable()

""" Select command line width. Default: 79. """
WIN_WIDTH = 79

""" Select CSV encoding (utf-8 or windows-1251). """
ENCODINGS_READ = 'utf-8', 'windows-1251'
ENCODING_WRITE = 'utf-8'

""" Delimiter for CSV. """
DELIMITER = ';'
