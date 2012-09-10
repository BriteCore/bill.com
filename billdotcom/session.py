"""
.. module:: session
   :synopsis: Session management (login, logout, etc).
"""

import iso8601
import uuid
from bill import Bill
from chartofaccount import ChartOfAccount
from customer import Customer
from invoice import Invoice
from item import Item
from vendor import Vendor
from vendorcredit import VendorCredit
from config import CONFIG, get_logger
from https import https_post, https_post_operation
from exceptions import BilldotcomError, ServerResponseError
from xmldict import XMLDict

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
        except (AttributeError, KeyError):
            message = operationresults['failed'][transaction]['message']
            LOG.error(message)
            raise ServerResponseError(message)

    def __request(self, name, payload):
        transaction = uuid.uuid4()

        xmlstring = self.__build_request__("""
            <operation transactionId="{transaction}" sessionId="{sessionId}">
                <{name}>
                    {payload}
                </{name}>
            </operation>
        """, name=name, payload=payload, transaction=transaction)

        response = https_post_operation(xmlstring)
        return self.__get_result_or_fail(response, transaction)

    def custom_request(self, name, **kwargs):
        """Construct and send a custom request.

        Args:
            name: The name of the operation. For instance, 'send_vendor_invite'.
            kwargs: Key values of data to send in the payload.

        Returns:
            XML dom response.

        Raises:
            ServerReponseError
        """

        payload = [
            '<{0}>{1}</{0}>'.format(key, XMLDict.valuetransform(value))
            for key, value in kwargs.items()
        ]

        return self.__request(name, payload)

    def create_bill(self, bill):
        """Creates a Bill object on the server.

        Args:
            bill: A Bill object with the required fields filled in.

        Returns:
            The newly created Bill's ID.

        Raises:
            ServerResponseError
        """
        result = self.__request('create_bill', bill.xml())
        return result.getElementsByTagName('id')[0].firstChild.data

    def create_chartofaccount(self, chartOfAccount):
        """Creates a Chart of Account object on the server.

        Args:
            chartOfAccount: A Chart of Account object with the required fields filled in.

        Returns:
            The newly created created Chart of Account's ID.

        Raises:
            ServerResponseError
        """
        result = self.__request('create_chartofaccount', chartOfAccount.xml())
        return result.getElementsByTagName('id')[0].firstChild.data


    def create_customer(self, customer):
        """Creates a Customer object on the server.

        Args:
            customer: A Customer object with the required fields filled in.

        Returns:
            The newly created created Customer's ID.

        Raises:
            ServerResponseError
        """
        result = self.__request('create_customer', customer.xml())
        return result.getElementsByTagName('id')[0].firstChild.data


    def create_invoice(self, invoice):
        """Creates a Invoice object on the server.

        Args:
            invoice: An Invoice object with the required fields filled in.

        Returns:
            The newly created Invoice's ID.

        Raises:
            ServerResponseError
        """
        result = self.__request('create_invoice', invoice.xml())
        return result.getElementsByTagName('id')[0].firstChild.data

    def create_item(self, item):
        """Creates an Item object on the server.

        Args:
            item: An Item object with the required fields filled in.

        Returns:
            The newly created created Item's ID.

        Raises:
            ServerResponseError
        """
        result = self.__request('create_item', item.xml())
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
        result = self.__request('create_vendor', vendor.xml())
        return result.getElementsByTagName('id')[0].firstChild.data

    def update_vendor(self, vendor):
        """Updates a Vendor object on the server. Update with 'isActive'=2 to deactivate it.

        Args:
            vendor: A Vendor object with the required fields filled in.

        Returns:
            The updated Vendor's ID.

        Raises:
            ServerResponseError
        """
        result = self.__request('update_vendor', vendor.xml())
        return result.getElementsByTagName('id')[0].firstChild.data

    def send_vendor_invite(self, vendorId, email):
        """Updates a Vendor object on the server. Update with 'isActive'=2 to deactivate it.

        Args:
            vendor: A Vendor object with the required fields filled in.

        Returns:
            The updated Vendor's ID.

        Raises:
            ServerResponseError
        """

        return self.custom_request('send_vendor_invite', vendorId=vendorId, email=email)

    def create_vendorcredit(self, vendorcredit):
        """Creates a Vendor Credit object on the server.

        Args:
            vendorcredit: A Vendor Credit object with the required fields filled in.

        Returns:
            The newly created Vendor Credit's ID.

        Raises:
            ServerResponseError
        """
        result = self.__request('create_vendorcredit', vendorcredit.xml())
        return result.getElementsByTagName('id')[0].firstChild.data

    def get_list(self, object_name, filters=[], **kwargs):
        """Gets data back from the server. Filters can be used to select specific objects by fields.
        The objects will be transformed into the corresponding classes and returned.

        Args:
            object_name: The type of object to list. Supported object types and their mappings:
                * "bill" for Bill objects
                * "chartOfAccount" for ChartOfAccount objects
                * "customer" for Customer objects
                * "invoice" for Invoice objects
                * "item" for Item objects
                * "vendor" for Vendor objects
                * "vendorcredit" for VendorCredit objects
            filters: A list of tuples representing filters to query with. Supported operators are:
                    =, <, >, !=, <=, >=, IN
                These operators can be used with any field in the model you are querying, as long
                as it has a data type of ID, date, Enum, IntegrationId, or ExternalId. Notice
                that String is **not** included!  See the official Bill.com documentation for more.
                An example of using a filter:
                    >>> with Session() as s:
                    >>>     s.get_list('bill', filters=[('invoiceDate', '<', date.today())])

            kwargs: You can also specify filters are simple kwargs. For example:
                >>> with Session() as s:
                >>>     s.get_list('bill', id='testID')

        Returns:
            A list of object classes, such as a list of :class:`billdotcom.bill.Bill`s.

        Raises:
            ServerResponseError
        """

        object_mapper = {
            "bill": Bill,
            "chartofaccount": ChartOfAccount,
            "customer": Customer,
            "invoice": Invoice,
            "item": Item,
            "vendor": Vendor,
            "vendorcredit": VendorCredit,
        }

        rename_dict = {
            "chartofaccount": 'chartOfAccount'
        }

        if object_name not in object_mapper:
            raise ValueError("{0} is not a supported object type".format(object_name))

        transaction = uuid.uuid4()


        def filter_to_xml(name, op, value):
            valid_ops = ('=', '<', '>', '!=', '<=', '>=', 'IN')
            if op not in valid_ops:
                raise ValueError('filter operator {0} is not supported'.format(op))

            op = op.replace('>', '&gt;').replace('<', '&lt;')

            value = XMLDict.valuetransform(value)

            return '''
                <expression>
                    <field>{0}</field>
                    <operator>{1}</operator>
                    <value>{2}</value>
                </expression>'''.format(name, op, value)


        filter_xml = []
        for name, op, value in filters:
            filter_xml.append(filter_to_xml(name, op, value))

        for key, value in kwargs.items():
            filter_xml.append(filter_to_xml(key, '=', value))

        if filter_xml:
            filter_xml = '''
                <filter>
                    {0}
                </filter>'''.format('\n'.join(filter_xml))
        else:
            filter_xml = ''

        xmlstring = self.__build_request__("""
            <operation transactionId="{transaction}" sessionId="{sessionId}">
                <get_list object="{object_name}">
                    {filter_xml}
                </get_list>
            </operation>
        """, object_name=object_name, transaction=transaction, filter_xml=filter_xml)

        response = https_post_operation(xmlstring)
        result = self.__get_result_or_fail(response, transaction)

        constructor = object_mapper[object_name]

        # gross
        if object_name in rename_dict:
            object_name = rename_dict[object_name]

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

