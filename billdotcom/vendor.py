"""
.. module:: vendor
   :synopsis: A model for the Vendor object.
"""

from xmldict import XMLDict

class Vendor(XMLDict):
    """This models the Vendor object. In Bill.com vendors are the targets 
    that payments are sent to.

    Required:
        name (str): The name of the vendor

    Creation:
        Create a Vendor object and create it on the server side with
        with :func:`billdotcom.session.Session.create_vendor`. For example:

            >>> with Session() as s:
            >>>     a = Vendor(name)
            >>>     a['id'] = s.create_vendor(a)
    """

    def __init__(self, name):
        payload = {
            'name': name,
        }

        super(Vendor, self).__init__('vendor', **payload)

