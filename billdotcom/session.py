"""
.. module:: session
   :synopsis: Session management (login, logout, etc).
"""

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

    def __enter__(self):
        self.login()

    def __exit__(self, type, value, traceback):
        self.logout()

    def login(self):
        """Initiate a session on the server."""

        data = {
            'appkey': CONFIG.get('authentication', 'appkey'),
            'email': CONFIG.get('authentication', 'email'),
            'password': CONFIG.get('authentication', 'password'),
            'orgid': CONFIG.get('organization', 'id'),
        }

        xmlstring = """
        <request version="1.0" applicationkey="{appkey}">
            <login>
                <username>{email}</username>
                <password>{password}</password>
                <orgID>{orgid}</orgID>
            </login>
        </request>
        """.format(**data)

        response = https_post(xmlstring)

        self.session_id = response.getElementsByTagName('sessionId')[0].firstChild.data

        print response.toprettyxml()

    def logout(self):
        """Shut down a session on the server."""

        if not self.session_id:
            raise BilldotcomError("cannot logout on a session that has not logged in")

        data = {
            'appkey': CONFIG.get('authentication', 'appkey'),
            'sessionId': self.session_id
        }

        xmlstring = """
        <request version="1.0" applicationkey="{appkey}">
            <logout sessionId="{sessionId}">
            </logout>
        </request>
        """.format(**data)

        response = https_post(xmlstring)

        print response.toprettyxml()

