import datetime


class Selector:
    def __init__(self, client):
        # https://fedorahosted.org/suds/wiki/TipsAndTricks#TypesNamesContaining
        client.factory.separator('/')
        self.client = client
        self.fields = []
        self.predicates = []
        self.date_range = None
        self.ordering = []
        self.paging = None

    def build(self):
        selector = self.client.factory.create('Selector')
        selector.fields = self.fields if self.fields else None
        selector.predicates = self.predicates if self.predicates else None
        selector.dateRange = self.date_range if self.date_range else None
        selector.ordering = self.ordering if self.ordering else None
        selector.paging = self.paging if self.paging else None

        return selector

    def select_fields(self, *args):
        self.fields = args
        return self

    # filter criteria
    def filter_by(self, field, values, operator='=='):
        predicate = self.client.factory.create('Predicate')
        predicate.field = field
        predicate.operator = Selector._create_predicate_operator(self,
                                                                 operator)
        predicate.values = values

        self.predicates.append(predicate)
        return self

    def order_by(self, field, desc=False):
        '''sortting a field by either 'ASCENDING' or 'DESCENDING' order.'''
        ordering = self.client.factory.create('OrderBy')
        ordering.field = field
        sort_order = self.client.factory.create('SortOrder')
        ordering.sortOrder = sort_order.DESCENDING if desc else sort_order.ASCENDING

        self.ordering.append(ordering)
        return self

    def from_date_range(self, min_date=None, max_date=None):
        '''Specify a start date and an end date in the format of YYYYMMDD, both date specified inclusive'''
        date_range = self.client.factory.create('DateRange')

        if min_date is None:
            min_date = datetime.date(1990, 1, 1)

        if max_date is None:
            max_date = datetime.date(2038, 1, 1)

        date_range.min = min_date.strftime('%Y%m%d')
        date_range.max = max_date.strftime('%Y%m%d')

        self.date_range = date_range

        return self

    def at_page(self, start_index=0, page_size=100):
        page = self.client.factory.create('Paging')
        page.startIndex = start_index
        page.numberResults = page_size

        self.paging = page

        return self

    def _create_predicate_operator(self, short_operator_name):
        predicate_operator = self.client.factory.create('Predicate.Operator')
        operatorr_map = {'!=': predicate_operator.NOT_EQUALS,
                         '<>': predicate_operator.NOT_EQUALS,
                         '==': predicate_operator.EQUALS,
                         '>': predicate_operator.GREATER_THAN,
                         '>=': predicate_operator.GREATER_THAN_EQUALS,
                         '<': predicate_operator.LESS_THAN,
                         '<=': predicate_operator.LESS_THAN_EQUALS,
                         '[]': predicate_operator.IN,
                         '][': predicate_operator.NOT_IN}

        match_operator = operatorr_map[
            short_operator_name] if operatorr_map.has_key(
                short_operator_name) else short_operator_name

        return predicate_operator[match_operator]
