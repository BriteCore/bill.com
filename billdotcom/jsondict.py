"""
.. module:: jsondict
   :synopsis: Provides support for dict-like objects representing Bill.com objects.
"""

import collections
import copy
import time
import datetime
from .exceptions import BilldotcomError


class JSONDict(collections.MutableMapping):
    """Implements a dict-like object that is used .

    Keys must be strings.

    Creation:
        Create a Bill object and create it on the server side with
        with :func:`billdotcom.session.Session.create_bill`. For example:
    """

    def __init__(self, bdc_name, required, **kwargs):
        for key in required:
            if key not in kwargs:
                raise TypeError("{0} is required".format(key))

        self.name = bdc_name
        self.url = bdc_name + '.json'
        self.__payload = dict(
            entity = bdc_name
        )
        self.__payload.update(kwargs)

        # the nested objects are {'objname': [list, of, things]}
        self.nested_object = {}

        # the nested map is {'objname': ChildClass}
        self.nested_map = {}

    def convert_nested(self):
        for key, value in self.__payload.items():
            nested_obj = self.nested_map.get(key)
            if nested_obj:
                children = [ nested_obj(**child) for child in value ]
                self.__payload[key] = children

    def __getitem__(self, key):
        return self.__payload[self.__keytransform__(key)]

    def __setitem__(self, key, value):
        self.__payload[self.__keytransform__(key)] = value

    def __delitem__(self, key):
        del self.__payload[self.__keytransform__(key)]

    def __iter__(self):
        return iter(self.__payload)

    def __len__(self):
        return len(self.__payload)

    def __keytransform__(self, key):
        return str(key)

    def __str__(self):
        import pprint
        return pprint.pformat(self.data)

    def __repr__(self):
        content = ("{0}='{1}'".format(key, value) for key, value in self.__payload.items())
        return '{0}({1})'.format(self.__class__.__name__, ', '.join(content))

    @property
    def data(self):
        """
        Builds a JSON-compatible dict for transport to Bill.com.

        Returns:
            Dict representing the object. Fields are excluded if they aren't provided.

        Raises:
            BilldotcomError when the object was built incorrectly
        """

        obj = copy.deepcopy(self.__payload)

        def format_val(value):
            if type(value) in (datetime.date, datetime.datetime):
                # needs to be in iso8601
                return '{:%Y-%m-%dT%H:%M:%S}{:+06.2f}'.format(value, time.timezone/3600.0)
            else:
                return value

        # filter out None valued keys and format them
        obj = { key: format_val(value) for key, value in obj.items() if value }

        for name, children in self.nested_object.items():
            if name in obj:
                raise BilldotcomError('nested object {} already exists in the {} properties'.format(name, self.url))
            obj[name] = [x.data for x in children]

        return obj

