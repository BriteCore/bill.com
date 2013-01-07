"""
.. module:: bill
   :synopsis: A model for the Bill object.
"""

from jsondict import JSONDict

class Bill(JSONDict):
    """This models the Bill object.

    Required:
        ============= ========== ===============================================
        *Argument*               *Description*
        ------------------------ -----------------------------------------------
        invoiceNumber (str):     The invoice number or identifier.
        vendorId      (str):     The ID of the vendor that is creating the bill.
        invoiceDate   (date):    The date that the invoice was billed on.
        dueDate       (date):    The date that the invoice must be paid by.
        ============= ========== ===============================================

    Creation:
        Create a Bill object and create it on the server side with
        with :func:`billdotcom.session.Session.create_bill`. For example:

            >>> with Session() as s:
            >>>     a = Bill(
            >>>         vendorId = 'abc123',
            >>>         invoiceNumber = 'BC1234',
            >>>         invoiceDate = date(2012,10,1),
            >>>         dueDate = date(2012,11,1),
            >>>         amount = 25.0
            >>>     )
            >>>     a['id'] = s.create(a)

    Retrieval:
        Download a list of Bill objects from the server with the Session.
        For example:

            >>> with Session() as s:
            >>>     print [x['id'] for x in s.list('Bill')]
    """

    def __init__(self, ignore_required=False, **kwargs):
        required = (
            'vendorId',
            'invoiceNumber',
            'invoiceDate',
            'dueDate',
            'externalId',
            'amount',
            'vendorId',
        )

        if ignore_required == True:
            required = ()

        super(Bill, self).__init__('Bill', required, **kwargs)

        self.nested_map = {
            'billLineItems': BillLineItem
        }

    def add_line_item(self, line_item):
        self.nested_object.setdefault('billLineItems', [])
        self.nested_object['billLineItems'].append(line_item)


class BillLineItem(JSONDict):
    """This models the BillLineItem object. It allows you to further describe a Bill,
    assigning amounts among individual line items.

    Required:
        ============= ========== =====================================================
        *Argument*               *Description*
        ------------------------ -----------------------------------------------------
        ============= ========== =====================================================

    Creation:
        BillLineItems are created along with a Bill. For example

            >>> with Session() as s:
            >>>     a = Bill(
            >>>         vendorId = 'abc123',
            >>>         invoiceNumber = 'BC1234',
            >>>         invoiceDate = date(2012,10,1),
            >>>         dueDate = date(2012,11,1),
            >>>         amount = 5.0
            >>>     )
            >>>     a.add_line_item(BillLineItem(amount=2, description="eggs"))
            >>>     a.add_line_item(BillLineItem(amount=3, description="bacon"))
            >>>     a['id'] = s.create(a)

    Retrieval:
        See the :class:`billdotcom.bill.Bill` class for how you can retrieve bills.
    """

    def __init__(self, ignore_required=False, **kwargs):
        required = ()

        if ignore_required == True:
            required = ()

        super(BillLineItem, self).__init__('BillLineItem', required, **kwargs)

