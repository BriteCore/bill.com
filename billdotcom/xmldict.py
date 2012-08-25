"""
.. module:: xmldict
   :synopsis: Provides support for easy dict to XML serializing.
"""

import collections
import datetime
import xml.dom

class XMLDict(collections.MutableMapping):
    """Implements a dict-like object that can seralize itself as XML.

    Types (such as datetime) are converted to Bill.com compatible strings.

    Keys must be strings.

    Creation:
        Create a Bill object and create it on the server side with
        with :func:`billdotcom.session.Session.create_bill`. For example:
    """

    def __init__(self, root_name, required, **kwargs):

        for key in required:
            if key not in kwargs:
                raise TypeError("{0} is required".format(key))

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


    @classmethod
    def parse(cls, dom):
        """Reads fields from XML to construct a new object.

        Args:
            dom (xml.dom): a DOM object that contains the correct fields.

        Returns:
            A newly constructed object.

        Raises:
            ValueError
        """

        # if dom.tagName != cls.root_name:
            # raise ValueError("expected root tag {0} but got {1}".format(cls.__root_name, dom.tagName))

        dom.normalize()

        def element_children(root):
            return (x for x in root.childNodes if x.nodeType == xml.dom.Node.ELEMENT_NODE)

        data = {
            field.tagName: field.firstChild.data.strip()
            for field in element_children(dom)
        }

        return cls(ignore_required=True, **data)

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

