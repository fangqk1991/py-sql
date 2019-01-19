import re

from .FCDatabase import FCDatabase
from .SQLException import SQLException
from .BuilderBase import BuilderBase


class SQLSearcher(BuilderBase):

    __queryColumns: list = None

    __distinct: bool = False
    __page: int = -1
    __feedsPerPage: int = 1

    __orderRules: list = None
    __optionStr: str = None

    def __init__(self, db: FCDatabase):
        super().__init__(db)
        self.__queryColumns = []
        self.__orderRules = []

    def mark_distinct(self):
        self.__distinct = True

    def set_columns(self, columns):
        self.__queryColumns = columns

    def add_column(self, column):
        self.__queryColumns.append(column)

    def add_order_rule(self, sort_key, direction):
        if not re.match('\w+', direction):
            return

        direction = direction.upper()
        if direction != 'DESC':
            direction = ''

        self.__orderRules.append({'sort_key': sort_key, 'sort_direction': direction})

    def set_page_info(self, page, feeds_per_page):
        self.__page = page
        self.__feedsPerPage = feeds_per_page

    def set_option_str(self, option_str):
        self.__optionStr = option_str

    def order_rules(self):
        return self.__orderRules

    def __check_columns_valid(self):
        if len(self.__queryColumns) <= 0:
            raise SQLException('%s: queryColumns missing.' % __class__)

    def export(self):
        self._check_table_valid()
        self.__check_columns_valid()

        query = 'SELECT %s %s FROM %s' % (
            'DISTINCT' if self.__distinct else '',
            ', '.join(self.__queryColumns),
            self._table)

        conditions = self._conditions()
        if len(conditions) > 0:
            query = '%s WHERE %s' % (query, self.build_condition_str())

        return query, self._stmt_values()

    def query_list(self):
        query, params = self.export()

        if self.__optionStr:
            query = '%s %s' % (query, self.__optionStr)

        if self.__orderRules:
            order_items = []
            for rule in self.__orderRules:
                order_items.append('%s %s' % (rule['sort_key'], rule['sort_direction']))
            query = '%s ORDER BY %s' % (query, ', '.join(order_items))

        if self.__page >= 0 and self.__feedsPerPage > 0:
            query = '%s LIMIT %d, %d' % (query, self.__page * self.__feedsPerPage, self.__feedsPerPage)

        return self._database.query(query, params)

    def query_single(self):
        items = self.query_list()
        if items:
            return items[0]
        return None

    def query_count(self):
        self._check_table_valid()

        if self.__distinct:
            query = 'SELECT COUNT(DISTINCT %s) AS count FROM %s' % (', '.join(self.__queryColumns), self._table)
        else:
            query = 'SELECT COUNT(*) AS count FROM %s' % self._table

        conditions = self._conditions()
        if len(conditions) > 0:
            query = '%s WHERE %s' % (query, self.build_condition_str())

        result = self._database.query(query, self._stmt_values())
        return result[0]['count']
