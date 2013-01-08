"""
.. module:: customer
   :synopsis: A model for the Customer object.
"""

from .jsondict import JSONDict

class Customer(JSONDict):
    """This models the Customer object. In Bill.com customers are what
    payments are sent from.

    Required:
        ==== ===== =========================
        *Argument* *Description*
        ---------- -------------------------
        name (str) The name of the customer
        ==== ===== =========================

    Creation:
        Create a Customer object and create it on the server side with
        with :func:`billdotcom.session.Session.create_customer`. For example:

            >>> with Session() as s:
            >>>     a = Customer(name="John Doe")
            >>>     a['id'] = s.create(a)

    Retrieval:
        Download a list of Vendor objects from the server with the Session.
        For example:

            >>> with Session() as s:
            >>>     print [x['id'] for x in s.list('Customer')]
    """

    def __init__(self, ignore_required=False, **kwargs):
        required = (
            'name',
        )

        if ignore_required == True:
            required = ()

        super(Customer, self).__init__('Customer', required, **kwargs)

