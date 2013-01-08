"""
.. module:: invoice
   :synopsis: A model for the invoice object.
"""

from .jsondict import JSONDict

class Invoice(JSONDict):
    """This models the Invoice object.

    Required:
        ================ ========== ===============================================
        *Argument*                  *Description*
        --------------------------- -----------------------------------------------
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
            >>>         customerId= 'abc123',
            >>>         invoiceNumber = 'BC1234',
            >>>         invoiceDate = date(2012,10,1),
            >>>         dueDate = date(2012,11,1),
            >>>     )
            >>>     a['id'] = s.create(a)

    Retrieval:
        Download a list of Invoice objects from the server with the Session.
        For example:

            >>> with Session() as s:
            >>>     print [x['id'] for x in s.list('invoice')]
    """

    def __init__(self, ignore_required=False, **kwargs):
        required = (
            'customerId',
            'invoiceNumber',
            'invoiceDate',
            'dueDate',
        )

        if ignore_required == True:
            required = ()

        super(Invoice, self).__init__('Invoice', required, **kwargs)

        self.nested_map = {
            'invoiceLineItems': InvoiceLineItem
        }
        self.convert_nested()

    def add_line_item(self, line_item):
        self.nested_object.setdefault('invoiceLineItems', [])
        self.nested_object['invoiceLineItems'].append(line_item)


class InvoiceLineItem(JSONDict):
    """This models the InvoiceLineItem object. It allows you to further describe an Invoice,
    assigning amounts among individual line items.

    Required:
        ============= ========== =====================================================
        *Argument*               *Description*
        ------------------------ -----------------------------------------------------
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
            >>>     a['id'] = s.create(a)

    Retrieval:
        See the :class:`billdotcom.bill.Invoice` class for how you can retrieve invoices.
    """

    def __init__(self, ignore_required=False, **kwargs):
        required = (
            'itemId',
            'quantity'
        )

        if ignore_required == True:
            required = ()

        super(InvoiceLineItem, self).__init__('InvoiceLineItem', required, **kwargs)

