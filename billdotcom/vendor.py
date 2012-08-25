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

    Retrieval:
        Download a list of Vendor objects from the server with the Session.
        For example:

            >>> with Session() as s:
            >>>     print [x['id'] for x in s.get_list('vendor')]
    """

    def __init__(self, ignore_required=False, **kwargs):
        required = (
            'name',
        )

        if ignore_required == True:
            required = ()

        super(Vendor, self).__init__('vendor', required, **kwargs)

