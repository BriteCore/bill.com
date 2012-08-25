"""
.. module:: bill
   :synopsis: A model for the Bill object.
"""

from xmldict import XMLDict

class Bill(XMLDict):
    """This models the Bill object.

    Required:
        externalId (str): The developer-created ID from your system.
        invoiceNumber (str): The invoice number or identifier.
        vendorId (str): The ID of the vendor that is creating the bill.
        invoiceDate (date): The date that the invoice was billed on.
        dueDate (date): The date that the invoice must be paid by.
        amount (Decimal): The amount of money that is billed.

    Creation:
        Create a Bill object and create it on the server side with
        with :func:`billdotcom.session.Session.create_bill`. For example:

            >>> with Session() as s:
            >>>     a = Bill(uuid, invoice, billDate, dueDate, amount)
            >>>     a['id'] = s.create_bill(a)
    """

    def __init__(self, externalId, invoiceNumber, vendorId, invoiceDate, dueDate, amount):
        payload = {
            'vendorId': vendorId,
            'invoiceNumber': invoiceNumber,
            'invoiceDate': invoiceDate,
            'dueDate': dueDate,
            'externalId': externalId,
            'amount': amount,
        }

        super(Bill, self).__init__('bill', **payload)

