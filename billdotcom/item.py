"""
.. module:: item 
   :synopsis: A model for the Item object.
"""

from .jsondict import JSONDict

class Item(JSONDict):
    """This models the Item object. 
    Apparently Items are needed for invoices. Who knew?

    Required:
        ==== ====== ==========================
        *Argument*  *Description*
        ----------- --------------------------
        type (enum) Service = 1
                    Product(Non-inventory) = 3
                    Discount = 5
                    Sales Tax = 6
        name (str)  The name of your item.
        ==== ====== ==========================

    Creation:
        Create an Item object and create it on the server side with
        with :func:`billdotcom.session.Session.create_item`. For example:

            >>> with Session() as s:
            >>>     a = Item(name="Test Item",
            >>>              type=1)
            >>>     a['id'] = s.create(a)

    Retrieval:
        Download a list of Vendor objects from the server with the Session.
        For example:

            >>> with Session() as s:
            >>>     print [x['id'] for x in s.list('item')]
    """

    def __init__(self, ignore_required=False, **kwargs):
        required = (
            'name',
            'type',
        )

        if ignore_required == True:
            required = ()

        super(Item, self).__init__('Item', required, **kwargs)

