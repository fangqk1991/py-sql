from fc_sql import SQLException, BuilderBase


class SQLAdder(BuilderBase):

    __insertKeys: list = None
    __insertValues: list = None

    def __init__(self, sql_db):
        super().__init__(sql_db)
        self.__insertKeys = []
        self.__insertValues = []

    def insert_kv(self, key, value):
        self.__insertKeys.append(key)
        self.__insertValues.append(value)

    def execute(self):
        self._check_table_valid()
        if len(self.__insertKeys) <= 0:
            raise SQLException('%s: insertKeys missing.' % __class__)

        query = 'INSERT INTO %s(%s) VALUES(%s)' % (
            self._table,
            ', '.join(self.__insertKeys),
            self.__marks_of_insert_query())
        self._mysqlDB.update(query, self._stmt_values())

    def __marks_of_insert_query(self):
        marks = ['%s'] * len(self._stmt_values())
        return ', '.join(marks)

    def _stmt_values(self):
        return self.__insertValues

