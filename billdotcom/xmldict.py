"""
.. module:: xmldict
   :synopsis: Provides support for easy dict to XML serializing.
"""

import collections
import datetime

class XMLDict(collections.MutableMapping):
    """Implements a dict-like object that can seralize itself as XML.

    Types (such as datetime) are converted to Bill.com compatible strings.

    Keys must be strings.

    Creation:
        Create a Bill object and create it on the server side with
        with :func:`billdotcom.session.Session.create_bill`. For example:
    """

    def __init__(self, root_name, **kwargs):
        self.__root_name = root_name
        self.__payload = {}
        self.__payload.update(kwargs)

    def __getitem__(self, key):
        return self.__payload[self.__keytransform__(key)]

    def __setitem__(self, key, value):
        self.__payload[self.__keytransform__(key)] = value

    def __delitem__(self, key):
        del self.__payload[self.__keytransform__(key)]

    def __iter__(self):
        return iter(self.__payload)

    def __len__(self):
        return len(self.store)

    def __keytransform__(self, key):
        return str(key)

    def __str__(self):
        return self.xml()

    def xml(self):
        """Renders the dict payload as an XML object

        Args:
            root_name (str): the name of the root node

        Returns:
            String representing the dict. Fields are excluded if they aren't provided.
        """

        def valuetransform(value):
            if type(value) in (datetime.datetime, datetime.date):
                return value.strftime('%m/%d/%y')
            else:
                return str(value)

        fields = [
            '<{0}>{1}</{0}>'.format(key, valuetransform(value))
            for (key, value) in self.__payload.items()
        ]

        return '<{0}>\n{1}\n</{0}>'.format(self.__root_name, '\n'.join(fields))

