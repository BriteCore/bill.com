"""
.. module:: vendor
   :synopsis: A model for the Vendor object.
"""

from xmldict import XMLDict

class Vendor(XMLDict):
    """This models the Vendor object. In Bill.com vendors are the targets 
    that payments are sent to.

    Required:
        ==== ===== =======================
        *Argument* *Description*
        ---------- -----------------------
        name (str) The name of the vendor
        ==== ===== =======================

    Creation:
        Create a Vendor object and create it on the server side with
        with :func:`billdotcom.session.Session.create_vendor`. For example:

            >>> with Session() as s:
            >>>     a = Vendor(name="Test Vendor")
            >>>     a['id'] = s.create_vendor(a)

    Updates:
        It's easy to create and update your contacts and vendors.
        For example, to activate a given vendor:
            >>> vendor = s.get_list('vendor', id='00901YYOFDJNAHP2xlg9')[0]
            >>> vendor['isActive'] = 1
            >>> s.update_vendor(vendor)

        If you want to deactivate all your vendors, you might try something like this:
            >>> for vendor in s.get_list('vendor'):
            >>>     vendor['isActive'] = 2
            >>>     s.update_vendor(vendor)

    Retrieval:
        Download a list of Vendor objects from the server with the Session.
        For example:

            >>> with Session() as s:
            >>>     print s.get_list('vendor')
    """

    def __init__(self, ignore_required=False, **kwargs):
        required = (
            'name',
        )

        if ignore_required == True:
            required = ()

        super(Vendor, self).__init__('vendor', required, **kwargs)

