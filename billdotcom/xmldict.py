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

        self.root_name = root_name
        self.__payload = {}
        self.__payload.update(kwargs)

        # the nested objects are {'rootname': [list, of, things]}
        self.nested_object = {}

        # the nested map is {'rootname': ChildClass}
        self.nested_map = {}

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

    def __repr__(self):
        content = ("{0}='{1}'".format(key, value) for key, value in self.__payload.items())
        return '{0}({1})'.format(self.__class__.__name__, ', '.join(content))

    @classmethod
    def valuetransform(cls, value):
        if type(value) == datetime.date:
            return value.strftime('%m/%d/%y')
        elif type(value) == datetime.datetime:
            return value.strftime('%m/%d/%Y %H:%M:%S')
        else:
            return str(value).replace('<', '&lt;').replace('>', '&gt;')

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

        def child_filter(root, node_type):
            return [x for x in root.childNodes if x.nodeType == node_type]

        data = {}
        nested = {}

        for field in child_filter(dom, xml.dom.Node.ELEMENT_NODE):
            # some nodes will have children (nested data)
            children = child_filter(field, xml.dom.Node.ELEMENT_NODE)

            if children:
                nested[field.tagName] = children
            else:
                data[field.tagName] = field.firstChild.data.strip()

        result = cls(ignore_required=True, **data)

        for name, dom_list in nested.items():
            if name not in result.nested_map:
                print result.root_name
                print result.nested_map
                raise ValueError('child node {0} is not expected to be a member of {1}'.format(name, result.root_name))

            nested_cls = result.nested_map[name]
            result.nested_object[name] = [nested_cls.parse(x) for x in dom_list]

        return result

    def xml(self, indent=0):
        """Renders the dict payload as an XML object. Attempts to pad out nested stuff
        for easier reading.

        Args:
            root_name (str): the name of the root node

        Returns:
            String representing the dict. Fields are excluded if they aren't provided.
        """

        pad = indent*'\t'

        fields = [
            '\t{pad}<{0}>{1}</{0}>'.format(key, XMLDict.valuetransform(value), pad=pad)
            for (key, value) in self.__payload.items()
        ]

        for root, nodes in self.nested_object.items():
            sep = '\n{pad}'.format(pad=pad)
            xml_nodes = sep.join([x.xml(indent+2) for x in nodes])
            fields.append('\t{pad}<{0}>\n{1}\n\t{pad}</{0}>'.format(root, xml_nodes, pad=pad))

        return '{pad}<{0}>\n{1}\n{pad}</{0}>'.format(self.root_name, '\n'.join(fields), pad=indent*'\t')

