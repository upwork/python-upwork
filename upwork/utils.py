# Python bindings to Upwork API
# python-upwork version 0.5
# (C) 2010-2015 Upwork

from datetime import date
from upwork.exceptions import ApiValueError


def assert_parameter(parameter_name, value, options_list):
    """Raise an exception if parameter's value not in options list."""
    if value not in options_list:
        raise ApiValueError(
            "Incorrect value for {0}: '{1}', "
            "valid values are {2}".format(
                parameter_name, value, options_list))


def decimal_default(obj):
    """JSON serialization of Decimal.

    *Usage:*
      ``json.dumps(data, default=decimal_default)``

    Converts decimal to string.

    """
    if obj.__class__.__name__ == 'Decimal':
        return str(obj)
    raise TypeError


class Q(object):
    """Simple GDS query constructor.

    Used to costruct :py:class:`upwork.utils.Query`.

    """

    def __init__(self, arg1, operator=None, arg2=None):
        self.arg1 = arg1
        self.operator = operator
        self.arg2 = arg2

    def __and__(self, other):
        return self.__class__(self, 'AND', other)

    def __or__(self, other):
        return self.__class__(self, 'OR', other)

    def __eq__(self, other):
        return self.__class__(self, '=', other)

    def __lt__(self, other):
        return self.__class__(self, '<', other)

    def __le__(self, other):
        return self.__class__(self, '<=', other)

    def __gt__(self, other):
        return self.__class__(self, '>', other)

    def __ge__(self, other):
        return self.__class__(self, '>=', other)

    def arg_to_string(self, arg):
        if isinstance(arg, self.__class__):
            if arg.operator:
                return '({0})'.format(arg)
            else:
                return arg
        elif isinstance(arg, str):
            return "'{0}'".format(arg)
        elif isinstance(arg, date):
            return "'{0}'".format(arg.isoformat())
        else:
            return str(arg)

    def __str__(self):
        if self.operator:
            str1 = self.arg_to_string(self.arg1)
            str2 = self.arg_to_string(self.arg2)
            return '{0} {1} {2}'.format(str1, self.operator, str2)
        else:
            return self.arg1


class Query(object):
    """Simple GDS query.

    *Example:*::

      client.timereport.get_provider_report('user1',
          upwork.utils.Query(select=upwork.utils.Query.DEFAULT_TIMEREPORT_FIELDS,
                            where=(upwork.utils.Q('worked_on') <= date.today()) &
                            (upwork.utils.Q('worked_on') > '2010-05-01')))

    """

    DEFAULT_TIMEREPORT_FIELDS = ['worked_on',
                                 'team_id',
                                 'team_name',
                                 'task',
                                 'memo',
                                 'hours']
    DEFAULT_FINREPORT_FIELDS = ['reference',
                                'date',
                                'buyer_company__id',
                                'buyer_company_name',
                                'buyer_team__id',
                                'buyer_team_name',
                                'provider_company__id',
                                'provider_company_name',
                                'provider_team__id',
                                'provider_team_name',
                                'provider__id',
                                'provider_name',
                                'type',
                                'subtype',
                                'amount']

    def __init__(self, select, where=None, order_by=None):
        self.select = select
        self.where = where
        self.order_by = order_by

    def __str__(self):
        select = self.select
        select_str = 'SELECT ' + ', '.join(select)
        where_str = ''
        if self.where:
            where_str = ' WHERE {0}'.format(self.where)
        order_by_str = ''
        if self.order_by:
            order_by_str = ' ORDER BY ' + ','.join(self.order_by)
        return ''.join([select_str, where_str, order_by_str])


class Table(object):

    """
    A helper class to access cryptic GDS response as a list of dictionaries.

    """

    def __init__(self, data):
        self._cols = data['cols']   # Original data
        self._rows = data['rows']
        self.cols = [col['label'] for col in data['cols']]
        self.rows = []
        if data['rows']:
            if data['rows'][0] != '':   # Empty response
                for row in [row['c'] for row in data['rows']]:
                    self.rows.append([cell['v'] for cell in row])

    def __getitem__(self, key):
        if not isinstance(key, (slice, int)):
            raise TypeError
        if isinstance(key, slice):
            return [dict(zip(self.cols, row)) for row in self.rows[key]]
        else:
            return dict(zip(self.cols, self.rows[key]))

    def __len__(self):
        return len(self.rows)
