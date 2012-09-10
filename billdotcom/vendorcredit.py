"""
.. module:: vendorcredit
   :synopsis: A model for the Vendor Credit object.
"""

from xmldict import XMLDict

class VendorCredit(XMLDict):
    """This models the VendorCredit object.

    Required:
        ============= ========== ===============================================
        *Argument*               *Description*
        ------------------------ -----------------------------------------------
        vendorId      (str):     The ID of the vendor that is creating the credit.
        invoiceNumber (str):     The invoice number or identifier.
        invoiceDate   (date):    The date that the invoice was billed on.
        dueDate       (date):    The date that the invoice must be paid by.
        externalId    (str):     The developer-created ID from your system.
        amount        (Decimal): The amount of money that is billed.
        ============= ========== ===============================================

    Creation:
        Create a Vendor Credit object and create it on the server side with
        with :func:`billdotcom.session.Session.create_vendorcredit`. For example:

            >>> with Session() as s:
            >>>     a = VendorCredit(
            >>>                 vendorId = "VENDORID"
            >>>                 externalId = '123456',
            >>>                 invoiceNumber = 'BC1234',
            >>>                 invoiceDate = date(2012,10,1),
            >>>                 dueDate = date(2012,11,1),
            >>>                 amount = 25.0
            >>>         )
            >>>     a['id'] = s.create_vendorcredit(a)

    Retrieval:
        Download a list of Bill objects from the server with the Session.
        For example:

            >>> with Session() as s:
            >>>     print [x['id'] for x in s.get_list('vendorcredit')]
    """

    def __init__(self, ignore_required=False, **kwargs):
        required = (
            'vendorId',
            'invoiceNumber',
            'invoiceDate',
            'dueDate',
            'externalId',
            'amount'
        )

        if ignore_required == True:
            required = ()

        super(VendorCredit, self).__init__('vendorcredit', required, **kwargs)

        self.nested_map = {
            'vendorCreditLineItems': VendorCreditLineItem
        }

    def add_line_item(self, line_item):
        self.nested_object.setdefault('vendorCreditLineItems', [])
        self.nested_object['vendorCreditLineItems'].append(line_item)


class VendorCreditLineItem(XMLDict):
    """This models the VendorCreditLineItem object. It allows you to further describe a VendorCredit,
    assigning amounts among individual line items.

    Required:
        ============= ========== =====================================================
        *Argument*               *Description*
        ------------------------ -----------------------------------------------------
        amount        (Decimal)  The amount of money that is vendor credited on this line item.
        ============= ========== =====================================================

    Creation:
        VendorCreditLineItems are created along with a VendorCredit. For example

            >>> with Session() as s:
            >>>     a = VendorCredit(
            >>>         externalId = '123456',
            >>>         vendorId = 'abc123',
            >>>         invoiceNumber = 'BC1234',
            >>>         invoiceDate = date(2012,10,1),
            >>>         creditDate = date(2012,11,1),
            >>>         amount = 5.0
            >>>     )
            >>>     a.add_line_item(VendorCreditLineItem(amount=2, description="eggs"))
            >>>     a.add_line_item(VendorCreditLineItem(amount=3, description="bacon"))
            >>>     a['id'] = s.create_vendor credit(a)

    Retrieval:
        See the :class:`billdotcom.vendorcredit.VendorCredit` class for how you can retrieve vendor credits.
    """

    def __init__(self, ignore_required=False, **kwargs):
        required = (
            'amount',
        )

        if ignore_required == True:
            required = ()

        super(VendorCreditLineItem, self).__init__('vendorCreditLineItem', required, **kwargs)

