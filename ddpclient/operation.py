class Operation:
    def __init__(self, client):
        # https://fedorahosted.org/suds/wiki/TipsAndTricks#TypesNamesContaining
        client.factory.separator('/')
        self.client = client
        self.operation_type = None
        self.operand = None
        self.operator = None

    def add(self):
        self.operator = self.client.factory.create('Operator').ADD
        return self

    def remove(self):
        self.operator = self.client.factory.create('Operator').REMOVE
        return self

    def set(self):
        self.operator = self.client.factory.create('Operator').SET
        return self

    def user_list(self, is_logical=False, **kwargs):
        self.operation_type = 'UserListOperation'

        user_list_type = 'LogicalUserList' if is_logical else 'BasicUserList'
        user_list = self.client.factory.create(user_list_type)

        for k, v in kwargs.iteritems():
            setattr(user_list, k, v)

        self.operation_type = 'UserListOperation'
        self.operand = user_list
        return self

    def user_client_list(self, **kwargs):

        user_client_list = self.client.factory.create('UserListClient')

        for k, v in kwargs:
            setattr(user_list, k, v)

        self.operation_type = 'UserListClientOperation'
        self.operand = user_client_list

        return self

    def build(self):
        operation = None

        if self.operation_type is not None:
            operation = self.client.factory.create(self.operation_type)
            operation.operator = self.operator
            operation.operand = self.operand

        return operation
