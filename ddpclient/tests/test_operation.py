from unittest import TestCase

from ddpclient import Client, Operation
from oauth2client.client import OAuth2Credentials
import datetime


class TestOperation(TestCase):
    def setUp(self):
        client = Client(OAuth2Credentials('token', 'clientid', 'secret',
                                          'rtoken', datetime.datetime(
                                              2038, 1, 1), 'uri', 'ua'))

        self.operation = Operation(client.user_list_service())

        self.user_list_props = {
            'id': 123,
            'name': 'TEST',
            'description': 'TEST Description',
            'status': 'CLOSED',
            'integrationCode': '123',
            'accountUserListStatus': 'INACTIVE',
            'membershipLifeSpan': 30
        }

    def test_add_user_list(self):
        operation = self.operation.add().user_list(
            **self.user_list_props).build()

        self.assertEqual('ADD', operation.operator)
        self.assertEqual('TEST', operation.operand.name)

    def test_set_user_list(self):
        operation = self.operation.set().user_list(
            **self.user_list_props).build()

        self.assertEqual('SET', operation.operator)
        self.assertEqual('TEST', operation.operand.name)
        self.assertEqual(123, operation.operand.id)

    def test_remove_user_list(self):
        operation = self.operation.remove().user_list(
            **self.user_list_props).build()

        self.assertEqual('REMOVE', operation.operator)
        self.assertEqual('TEST', operation.operand.name)
        self.assertEqual(123, operation.operand.id)
