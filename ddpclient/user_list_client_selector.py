from selector import Selector


class UserListClientSelector(Selector):
    def __init__(self, client):
        super(UserListClientSelector, self).__init__(client)

    def from_date_range(self, min_date=None, max_date=None):
        date_range = self.client.factory.create('DateRange')

        date_min_obj = self.client.factory.create('Date')
        date_max_obj = self.client.factory.create('Date')

        if min_date is None:
            min_date = datetime.date(1990, 1, 1)

        if max_date is None:
            max_date = datetime.date(2038, 1, 1)

        date_min_obj.year = min_date.year
        date_min_obj.month = min_date.month
        date_min_obj.day = min_date.day
        date_max_obj.year = max_date.year
        date_max_obj.month = max_date.month
        date_max_obj.day = max_date.day

        date_range.min = date_min_obj
        date_range.max = date_max_obj

        self.date_range = date_range

        return self
