from suds.client import Client as SudsClient
from auth import Auth
import os

CLIENT_CUSTOMER_ID = os.getenv('DDP_CLIENT_CUSTOMER_ID', '123-456-7890')
USER_AGENT = 'DDP API Call'
USER_LIST_SERVICE_WSDL_URL = 'https://ddp.googleapis.com/api/ddp/provider/v201603/UserListService?wsdl'
USER_LIST_CLIENT_SERVICE_WSDL_URL = 'https://ddp.googleapis.com/api/ddp/provider/v201605/UserListClientService?wsdl'


class Client:

    soap_clients = {}

    def __init__(self, credentials=None):
        self.credentials = credentials if credentials is not None else Auth(
        ).get_credentials()

    def user_list_service(self):
        return Client._create_soap_service(self, USER_LIST_SERVICE_WSDL_URL)

    def user_list_client_service(self):
        return Client._create_soap_service(self,
                                           USER_LIST_CLIENT_SERVICE_WSDL_URL)

    def _create_soap_service(self, wsdl_url):
        if not Client.soap_clients.has_key(wsdl_url):
            Client.soap_clients[wsdl_url] = Client._create_soap_client(
                self, wsdl_url)

        return Client.soap_clients[wsdl_url]

    def _create_soap_client(self, url):
        soap_client = SudsClient(url)

        # set http headers
        http_headers = {}
        headers = self.credentials.apply(http_headers)

        soap_client.set_options(headers=http_headers)

        # set soap headers
        soap_headers = {'clientCustomerId': CLIENT_CUSTOMER_ID,
                        'userAgent': USER_AGENT}
        soap_headers = soap_client.factory.create('SoapHeader')
        soap_headers.clientCustomerId = CLIENT_CUSTOMER_ID
        soap_headers.userAgent = USER_AGENT
        soap_client.set_options(soapheaders=soap_headers)

        return soap_client
