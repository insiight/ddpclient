from unittest import TestCase
from ddpclient import Client
from oauth2client.client import OAuth2Credentials


class TestClient(TestCase):
    def setUp(self):
        self.client = Client(OAuth2Credentials('token', 'clientid', 'secret',
                                               'rtoken', 'exp', 'uri', 'ua'))

    def test_create_user_list_service(self):
        service = self.client.user_list_service()
        self.assertEquals(
            'https://ddp.googleapis.com/api/ddp/provider/v201603/UserListService?wsdl',
            service.wsdl.url)

    def test_create_user_list_client_service(self):
        service = self.client.user_list_client_service()
        self.assertEquals(
            'https://ddp.googleapis.com/api/ddp/provider/v201605/UserListClientService?wsdl',
            service.wsdl.url)
