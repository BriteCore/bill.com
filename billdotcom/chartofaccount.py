"""
.. module:: Chart of Account
   :synopsis: A model for the Chart of Account object.
"""

from xmldict import XMLDict

class ChartOfAccount(XMLDict):
    """This models the Chart of Account object. This is a mapping
    of the account type.

    Required:
        name (str): The name of the account (i.e. Checking)
        accountType (enum): Type of Account (This is not required in the API, but fails if not passed)
                            Unspecified = 0
                            Accounts Payable = 1
                            Accounts Receivable = 2
                            Bank = 3
                            Cost of Goods Sold = 4
                            Credit Card = 5
                            Equity = 6
                            Expenses = 7
                            Fixed Assed = 8
                            Income = 9
                            Long Term Liability = 10
                            Other Asset = 11
                            Other Current Asset = 12
                            Other Current Liability = 13
                            Other Expense = 14
                            Other Income = 15
                            Non-Posting = 16

    Optional:
        accountNumber (str): The account number
        description (str): Description of the accont
        parentChartOfAccountId (ChartOfAccountId): The parent chart of account
        integrationId (str): The ID of the record in an accounting system like QuickBooks.
        externalId (str): The external id of this account.
        createdTime (datetime): The create date.
        updatedTime (datetime): The last update date.
        lastSyncTime (SettableDateTime): The last time this object was synced.
        isActive (enum): Whether or not this chart of account is active.
                         1 = active
                         2 = inactive

    Creation:
        Create a Chart of Account object and create it on the server side with
        with :func:`billdotcom.session.Session.create_chartofaccount`. For example:

            >>> with Session() as s:
            >>>     a = ChartOfAccount(name="My Credit Card", 
                    >>>                accountType=5,
                    >>>                )
            >>>     a['id'] = s.create_chartofaccount(a)

    Retrieval:
        Download a list of Chart of Account objects from the server with the Session.
        For example:

            >>> with Session() as s:
            >>>     print [x['id'] for x in s.get_list('chartofaccount')]
    """

    def __init__(self, ignore_required=False, **kwargs):
        required = (
            'name',
            'accountType',
        )

        if ignore_required == True:
            required = ()

        super(ChartOfAccount, self).__init__('chartOfAccount', required, **kwargs)

