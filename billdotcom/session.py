"""
.. module:: session
   :synopsis: Session management (login, logout, etc).
"""

from config import LOG, CONFIG

# TODO: abstract away this crap
from xml.etree import ElementTree as ET

class Session(object):
    """This models and handles serialization of the Bill object.
    """

    def __init__(self):
        pass

    def __enter__(self):
        pass

    def __exit__(self, type, value, traceback):
        pass

    def login(self):
        appkey = CONFIG.get('authentication', 'appkey')
        request = ET.Element('request', version='1.0', applicationkey=appkey)
        pass

    def logout(self):
        pass

