from suds.client import Client as SudsClient
from . import UserListClientSelector, UserListSelector
import os
import httplib2

USER_AGENT = 'DDP API Call'
USER_LIST_SERVICE_WSDL_URL = 'https://ddp.googleapis.com/api/ddp/provider/v201603/UserListService?wsdl'
USER_LIST_CLIENT_SERVICE_WSDL_URL = 'https://ddp.googleapis.com/api/ddp/provider/v201605/UserListClientService?wsdl'


class Client(object):

    soap_clients = {}

    def __init__(self, credentials=None, client_customer_id=None):

        if credentials.access_token_expired:
            http = httplib2.Http()
            credentials.refresh(http)

        self.credentials = credentials
        self.client_customer_id = os.getenv('DDP_CLIENT_CUSTOMER_ID',
                                            client_customer_id)
        self.user_list_service_soap_client = self._create_soap_client(
            USER_LIST_SERVICE_WSDL_URL)

        self.user_list_client_service_soap_client = self._create_soap_client(
            USER_LIST_CLIENT_SERVICE_WSDL_URL)

    def _create_soap_client(self, url):
        soap_client = SudsClient(url)

        # set http headers
        http_headers = {}
        headers = self.credentials.apply(http_headers)

        soap_client.set_options(headers=http_headers)

        # set soap headers
        soap_headers = soap_client.factory.create('SoapHeader')
        soap_headers.clientCustomerId = self.client_customer_id
        soap_headers.userAgent = USER_AGENT
        soap_client.set_options(soapheaders=soap_headers)

        # https://fedorahosted.org/suds/wiki/TipsAndTricks#TypesNamesContaining
        soap_client.factory.separator('/')

        return soap_client

    def get(self, selector):
        soap_client = None

        if type(selector) is UserListSelector:
            soap_client = self.user_list_service_soap_client
        elif type(selector) is UserListClientSelector:
            soap_client = self.user_list_client_service_soap_client

        if soap_client is not None:
            return soap_client.service.get(selector.build(soap_client))

        return None

    def mutate(operation):
        pass
