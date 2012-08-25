"""
.. module:: bill
   :synopsis: A model for the Bill object.
"""

from xmldict import XMLDict

class Bill(XMLDict):
    """This models the Bill object.

    Required:
        ============= ========== ===============================================
        *Argument*               *Description*
        ------------------------ -----------------------------------------------
        externalId    (str):     The developer-created ID from your system.
        invoiceNumber (str):     The invoice number or identifier.
        vendorId      (str):     The ID of the vendor that is creating the bill.
        invoiceDate   (date):    The date that the invoice was billed on.
        dueDate       (date):    The date that the invoice must be paid by.
        amount        (Decimal): The amount of money that is billed.
        ============= ========== ===============================================

    Creation:
        Create a Bill object and create it on the server side with
        with :func:`billdotcom.session.Session.create_bill`. For example:

            >>> with Session() as s:
            >>>     a = Bill(
            >>>         externalId = '123456',
            >>>         vendorId = 'abc123',
            >>>         invoiceNumber = 'BC1234',
            >>>         invoiceDate = date(2012,10,1),
            >>>         dueDate = date(2012,11,1),
            >>>         amount = 25.0
            >>>     )
            >>>     a['id'] = s.create_bill(a)

    Retrieval:
        Download a list of Bill objects from the server with the Session.
        For example:

            >>> with Session() as s:
            >>>     print [x['id'] for x in s.get_list('bill')]
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

        super(Bill, self).__init__('bill', required, **kwargs)

        self.nested_map = {
            'billLineItems': BillLineItem
        }

    def add_line_item(self, line_item):
        self.nested_objects.setdefault('billLineItems', [])
        self.nested_objects['billLineItems'].append(line_item)


class BillLineItem(XMLDict):
    """This models the BillLineItem object. It allows you to further describe a Bill,
    assigning amounts among individual line items.

    Required:
        ============= ========== =====================================================
        *Argument*               *Description*
        ------------------------ -----------------------------------------------------
        amount        (Decimal)  The amount of money that is billed on this line item.
        ============= ========== =====================================================

    Creation:
        BillLineItems are created along with a Bill. For example

            >>> with Session() as s:
            >>>     a = Bill(
            >>>         externalId = '123456',
            >>>         vendorId = 'abc123',
            >>>         invoiceNumber = 'BC1234',
            >>>         invoiceDate = date(2012,10,1),
            >>>         dueDate = date(2012,11,1),
            >>>         amount = 5.0
            >>>     )
            >>>     a.add_line_item(BillLineItem(amount=2, description="eggs"))
            >>>     a.add_line_item(BillLineItem(amount=3, description="bacon"))
            >>>     a['id'] = s.create_bill(a)

    Retrieval:
        See the :class:`billdotcom.bill.Bill` class for how you can retrieve bills.
    """

    def __init__(self, ignore_required=False, **kwargs):
        required = (
            'amount',
        )

        if ignore_required == True:
            required = ()

        super(BillLineItem, self).__init__('billLineItem', required, **kwargs)

