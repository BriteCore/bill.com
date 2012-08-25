"""
.. module:: session
   :synopsis: Session management (login, logout, etc).
"""

import iso8601
import uuid
from bill import Bill
from vendor import Vendor
from config import CONFIG, get_logger
from https import https_post, https_post_operation
from exceptions import BilldotcomError, ServerResponseError

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
        """Gets Bill.com's system time.

        Returns:
            datetime. System time as reported by Bill.com
        """
        xmlstring = self.__build_request__("""
            <getcurrenttime sessionId="{sessionId}">
            </getcurrenttime>
        """)

        response = https_post(xmlstring)
        thetime = response.getElementsByTagName('currentTime')[0].firstChild.data
        return iso8601.parse_date(thetime)

    def __get_result_or_fail(self, operationresults, transaction):
        LOG = get_logger()
        transaction = str(transaction)
        try:
            return operationresults['OK'][transaction]
        except AttributeError:
            message = operationresults['failed'][transaction]['message']
            LOG.error(message)
            raise ServerResponseError(message)

    def create_bill(self, bill):
        """Creates a Bill object on the server.

        Args:
            bill: A Bill object with the required fields filled in.

        Returns:
            The newly created Bill's ID.

        Raises:
            ServerResponseError
        """
        transaction = uuid.uuid4()

        xmlstring = self.__build_request__("""
            <operation transactionId="{transaction}" sessionId="{sessionId}">
                <create_bill>
                    {bill}
                </create_bill>
            </operation>
        """, bill=bill.xml(), transaction=transaction)

        response = https_post_operation(xmlstring)
        result = self.__get_result_or_fail(response, transaction)
        return result.getElementsByTagName('id')[0].firstChild.data

    def create_vendor(self, vendor):
        """Creates a Vendor object on the server.

        Args:
            vendor: A Vendor object with the required fields filled in.

        Returns:
            The newly created Vendor's ID.

        Raises:
            ServerResponseError
        """
        transaction = uuid.uuid4()

        xmlstring = self.__build_request__("""
            <operation transactionId="{transaction}" sessionId="{sessionId}">
                <create_vendor>
                    {vendor}
                </create_vendor>
            </operation>
        """, vendor=vendor.xml(), transaction=transaction)

        response = https_post_operation(xmlstring)
        result = self.__get_result_or_fail(response, transaction)
        return result.getElementsByTagName('id')[0].firstChild.data


    def get_list(self, object_name, filters=None):
        """Gets data back from the server. Filters can be used to select specific objects by fields.
        The objects will be transformed into the corresponding classes and returned.

        Args:
            object_name: The type of object to list. Supported object types and their mappings:
                * "bill" for Bill objects
                * "vendor" for Vendor objects

        Returns:
            A list of object classes, such as a list of :class:`billdotcom.bill.Bill`s.

        Raises:
            ServerResponseError
        """

        object_mapper = {
            "bill": Bill,
            "vendor": Vendor,
        }

        if object_name not in object_mapper:
            raise ValueError("{0} is not a supported object type".format(object_name))

        transaction = uuid.uuid4()

        xmlstring = self.__build_request__("""
            <operation transactionId="{transaction}" sessionId="{sessionId}">
                <get_list object="{object_name}">
                </get_list>
            </operation>
        """, object_name=object_name, transaction=transaction)

        response = https_post_operation(xmlstring)
        result = self.__get_result_or_fail(response, transaction)

        constructor = object_mapper[object_name]
        object_data = [constructor.parse(x) for x in result.getElementsByTagName(object_name)]
        return object_data

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

