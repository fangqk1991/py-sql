from fc_sql import FCSQL, SQLException


class BuilderBase:

    _mysqlDB: FCSQL = None
    _table: str = None
    _conditionColumns: list = None
    _conditionValues: list = None

    def __init__(self, sql_db):
        self._mysqlDB = sql_db
        self._conditionColumns = []
        self._conditionValues = []

    def set_table(self, table):
        self._table = table

    def check_primary_key(self, params, key):
        if key not in params:
            raise SQLException('%s: primary key missing.' % __class__)
        self.add_condition_kv(key, params[key])

    def add_condition_kv(self, key, value):
        self._conditionColumns.append('(%s = ?)' % key)
        self._conditionValues.append(value)

    def add_special_condition(self, condition, *args):
        self._conditionColumns.append('(%s)' % condition)
        for value in args:
            self._conditionValues.append(value)

    def add_stmt_values(self, *args):
        for value in args:
            self._conditionValues.append(value)

    def _conditions(self):
        return self._conditionColumns

    def _check_table_valid(self):
        if self._table is None:
            raise SQLException('%s: table missing.' % __class__)

    def build_condition_str(self):
        return ' AND '.join(self._conditions())

    def _stmt_values(self):
        return self._conditionValues

