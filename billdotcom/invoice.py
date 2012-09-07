"""
.. module:: invoice
   :synopsis: A model for the invoice object.
"""

from xmldict import XMLDict

class Invoice(XMLDict):
    """This models the Invoice object.

    Required:
        ================ ========== ===============================================
        *Argument*                  *Description*
        --------------------------- -----------------------------------------------
        externalId       (str):     The developer-created ID from your system.
        invoiceNumber    (str):     The invoice number or identifier.
        customerId       (str):     The ID of the customer attached to the invoice.
        invoiceDate      (date):    The date that the invoice was billed on.
        dueDate          (date):    The date that the invoice must be paid by.
        ================ ========== ===============================================
        
        In addition to the above fields, you will need to add invoiceLineItems.

    Creation:
        Create a Invoice object and create it on the server side with
        with :func:`billdotcom.session.Session.create_invoice`. For example:

            >>> with Session() as s:
            >>>     a = Invoice(
            >>>         externalId = '123456',
            >>>         customerId= 'abc123',
            >>>         invoiceNumber = 'BC1234',
            >>>         invoiceDate = date(2012,10,1),
            >>>         dueDate = date(2012,11,1),
            >>>     )
            >>>     a['id'] = s.create_invoice(a)

    Retrieval:
        Download a list of Invoice objects from the server with the Session.
        For example:

            >>> with Session() as s:
            >>>     print [x['id'] for x in s.get_list('invoice')]
    """

    def __init__(self, ignore_required=False, **kwargs):
        required = (
            'customerId',
            'invoiceNumber',
            'invoiceDate',
            'dueDate',
            'externalId',
        )

        if ignore_required == True:
            required = ()

        super(Invoice, self).__init__('invoice', required, **kwargs)

        self.nested_map = {
            'invoiceLineItems': InvoiceLineItem
        }

    def add_line_item(self, line_item):
        self.nested_object.setdefault('invoiceLineItems', [])
        self.nested_object['invoiceLineItems'].append(line_item)


class InvoiceLineItem(XMLDict):
    """This models the InvoiceLineItem object. It allows you to further describe an Invoice,
    assigning amounts among individual line items.

    Required:
        ============= ========== =====================================================
        *Argument*               *Description*
        ------------------------ -----------------------------------------------------
        amount        (Decimal)  The amount of money that is billed on this line item.
        price         (Decimal)  Who knows?
        ratePercent   (Decimal)  The percentage of the rate
        ============= ========== =====================================================

    Creation:
        InvoiceLineItems are created along with an Invoice. For example

            >>> with Session() as s:
            >>>     a = Invoice(
            >>>         externalId = '123456',
            >>>         customerId = 'abc123',
            >>>         invoiceNumber = 'BC1234',
            >>>         invoiceDate = date(2012,10,1),
            >>>         dueDate = date(2012,11,1),
            >>>         amount = 5.0
            >>>     )
            >>>     a.add_line_item(InvoiceLineItem(amount=2, description="eggs"))
            >>>     a.add_line_item(InvoiceLineItem(amount=3, description="bacon"))
            >>>     a['id'] = s.create_invoice(a)

    Retrieval:
        See the :class:`billdotcom.bill.Invoice` class for how you can retrieve invoices.
    """

    def __init__(self, ignore_required=False, **kwargs):
        required = (
            'amount',
        )

        if ignore_required == True:
            required = ()

        super(InvoiceLineItem, self).__init__('invoiceLineItem', required, **kwargs)

