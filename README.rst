DDP API python client
---------------------

This is a python client library for the OAuth2 DDP API. Currently the following services are supported:

* UserListService
* UserListClientService


Installation
------------

::

    pip install ddpclient


Test
----

::

    python setup.py test

Requirement
-----------

1. OAuth client ID and OAuth client secret

   DDP API uses OAuth 2.0 for authorization, to authorize the DDP API,
   you must first create a Client ID and a Client Secret. Visit the
   `Developer Console`_ to create a project and a OAuth client with
   credentials.

   You will use the client ID and secret to authorize DDP API.

2. AdWards Client `Customer ID`_

   A unique three-part number that’s assigned to each AdWords account,
   listed at the top of every page in your account.

   You must set it as environment variable `DDP_CLIENT_CUSTOMER_ID`

Commands
--------

When installed, the DDP API client provide two command for authorizing
your application access to a DDP account.

Generate Authorize URL
^^^^^^^^^^^^^^^^^^^^^^

The ``ddp_authorize_url`` command expect the OAuth client id and client
secret as parameter and generate a URL for getting a AuthCode

::

    $ ddp_authorize_url
    usage: ddp_authorize_url [client_id client_secret]

Authorizing
^^^^^^^^^^^

The ``ddp_authorize`` command expect the OAuth client id, secrete and
the AuthCode obtained by using the ``ddp_authorize_url`` URL

::

    $ ddp_authorize
    usage: ddp_authorize [client_id client_secret auth_code]

Once this is done, a file ``.ddp_credentials`` is created and store the
resulting redentials. The credentials from this file will be used from
then on.

Usage
-----

Get UserList example:
^^^^^^^^^^^^^^^^^^^^^^^^

::

    from ddpclient import Selector, Client

    api_service = Client().user_list_service()
    selector = Selector(api_service). \
        select_fields('Id', 'Size'). \
        filter_by('Status', 'CLOSED'). \
        order_by('Id', True). \
        at_page(1, 3). \
        build()
    response = api_service.service.get(selector)

    print response

    # (UserListPage){
    #    totalNumEntries = 108
    #    Page.Type = "UserListPage"
    #    entries[] =
    #       (BasicUserList){
    #          id = 978704062
    #          isReadOnly = False
    #          name = "Name one"
    #          size = 0
    #          sizeRange = "LESS_THAN_FIVE_HUNDRED"
    #          listType = "REMARKETING"
    #          UserList.Type = "BasicUserList"
    #       },
    #       (BasicUserList){
    #          id = 178703382
    #          isReadOnly = False
    #          name = "Name two"
    #          size = 0
    #          sizeRange = "LESS_THAN_FIVE_HUNDRED"
    #          listType = "REMARKETING"
    #          UserList.Type = "BasicUserList"
    #       },
    #       (BasicUserList){
    #          id = 138700763
    #          isReadOnly = False
    #          name = "Name three"
    #          size = 0
    #          sizeRange = "LESS_THAN_FIVE_HUNDRED"
    #          listType = "REMARKETING"
    #          UserList.Type = "BasicUserList"
    #       },
    #  }


Add UserList example:
^^^^^^^^^^^^^^^^^^^^^^^^

::

    from ddpclient import Selector, Client, Operation

    api_service = Client().user_list_service()

    api_operation = Operation(api_service).add().user_list(
        name='TEST',
        description='TEST Description',
        status='CLOSED',
        integrationCode='123',
        accountUserListStatus='INACTIVE',
        membershipLifeSpan=30).build()

    response = api_service.service.mutate([api_operation])

    print response

    # (UserListReturnValue){
    #    ListReturnValue.Type = "UserListReturnValue"
    #    value[] =
    #       (BasicUserList){
    #          id = 12345678
    #          isReadOnly = False
    #          name = "TEST"
    #          description = "TEST Description"
    #          status = "CLOSED"
    #          integrationCode = "123"
    #          accessReason = "OWNED"
    #          accountUserListStatus = "INACTIVE"
    #          membershipLifeSpan = 30
    #          listType = "REMARKETING"
    #          isEligibleForSearch = True
    #          isEligibleForDisplay = True
    #          UserList.Type = "BasicUserList"
    #       },
    #  }


Update UserList example:
^^^^^^^^^^^^^^^^^^^^^^^^

::

    from ddpclient import Auth, Selector, Client, Operation

    api_service = Client().user_list_service()

    api_operation = Operation(api_service).set().user_list(
        id=395677280, name='TEST Updated Name').build()

    response = api_service.service.mutate([api_operation])
    print response

    # (UserListReturnValue){
    #    ListReturnValue.Type = "UserListReturnValue"
    #    value[] =
    #       (BasicUserList){
    #          id = 12345678
    #          isReadOnly = False
    #          name = "TEST Updated Name"
    #          description = "TEST Description"
    #          status = "CLOSED"
    #          integrationCode = "123"
    #          accessReason = "OWNED"
    #          accountUserListStatus = "INACTIVE"
    #          membershipLifeSpan = 30
    #          listType = "REMARKETING"
    #          isEligibleForSearch = True
    #          isEligibleForDisplay = True
    #          UserList.Type = "BasicUserList"
    #       },
    #  }


Remove UserList example:
^^^^^^^^^^^^^^^^^^^^^^^^

::

    from ddpclient import Selector, Client, Operation

    api_service = Client().user_list_service()
    api_operation = Operation(api_service).remove().user_list(id=395677280).build()

    response = api_service.service.mutate([api_operation])
    print response

    # suds.WebFault: Server raised fault: '[OperatorError.OPERATOR_NOT_SUPPORTED @ operations[0]]'
    # Note: UserListService does not support deleting user list, this code servers as example of 'remove' operations


.. _Developer Console: http://
.. _Customer ID: https://support.google.com/adwords/answer/29198?hl=en-AU
