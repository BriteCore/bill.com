"""
.. module:: session
   :synopsis: Session management (login, logout, etc).
"""

import iso8601
from config import CONFIG
from https import https_post
from exceptions import BilldotcomError

class Session(object):
    """This models and handles serialization of the Bill object.

    Your configuration should have the minimum requirements listed in :mod:`billdotcom.config`.
    Sessions will time out after 35 minutes.

    You can use it in a with statement:

        >>> with Session():
        >>>     # do stuff
    """

    def __init__(self):
        self.session_id = None
        self.appkey = CONFIG.get('authentication', 'appkey')

    def __build_request__(self, content, **kwargs):
        data = {
            'appkey': self.appkey,
            'sessionId': self.session_id,
            'content': content,
        }

        data.update(kwargs)

        xmlstring = """
        <request version="1.0" applicationkey="{{appkey}}">
            {0}
        </request>
        """.format(content).format(**data)

        return xmlstring

    def getcurrenttime(self):
        """Returns a datetime object representing the Bill.com system time."""
        xmlstring = self.__build_request__("""
            <getcurrenttime sessionId="{sessionId}">
            </getcurrenttime>
        """)

        response = https_post(xmlstring)
        thetime = response.getElementsByTagName('currentTime')[0].firstChild.data
        return iso8601.parse_date(thetime)

    def __enter__(self):
        self.login()
        return self

    def __exit__(self, type, value, traceback):
        self.logout()

    def login(self):
        """Initiate a session on the server."""

        data = {
            'appkey': self.appkey,
            'email': CONFIG.get('authentication', 'email'),
            'password': CONFIG.get('authentication', 'password'),
            'orgId': CONFIG.get('organization', 'id'),
        }

        xmlstring = self.__build_request__("""
            <login>
                <username>{email}</username>
                <password>{password}</password>
                <orgID>{orgId}</orgID>
            </login>
        """, **data)

        response = https_post(xmlstring)

        self.session_id = response.getElementsByTagName('sessionId')[0].firstChild.data

    def logout(self):
        """Shut down a session on the server."""

        if not self.session_id:
            raise BilldotcomError("cannot logout on a session that has not logged in")


        xmlstring = self.__build_request__("""
            <logout sessionId="{sessionId}">
            </logout>
        """)

        https_post(xmlstring)
        self.session_id = None

