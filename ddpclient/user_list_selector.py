from selector import Selector


class UserListSelector(Selector):
    def __init__(self, client):
        super(UserListSelector, self).__init__(client)

    def from_date_range(self, min_date=None, max_date=None):
        date_range = self.client.factory.create('DateRange')

        if min_date is None:
            min_date = datetime.date(1990, 1, 1)

        if max_date is None:
            max_date = datetime.date(2038, 1, 1)

        date_range.min = min_date.strftime('%Y%m%d')
        date_range.max = max_date.strftime('%Y%m%d')

        self.date_range = date_range

        return self
