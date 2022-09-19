""" Module config.py - configuration. """
import logging

"""Select logging mode:
INFO - fixings + WARNING, WARNING - dubbs and junk, disable() - disable all. """
LOG_MODE = logging.disable()

""" Select command line width. """
WIN_WIDTH = 89

""" Select CSV encoding (utf-8 or windows-1251). """
ENCODING_READ = 'windows-1251'
ENCODING_WRITE = 'windows-1251'

""" Number of column where phone numbers are in multicolumn mode. """
COLUMN = 6

""" How much columns in Header to be chopped. """
CHOP_HEAD = 2

""" Delimiter for CSV. """
DELIMITER = ';'
