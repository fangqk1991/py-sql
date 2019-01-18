from .SQLException import SQLException
from .BuilderBase import BuilderBase


class SQLModifier(BuilderBase):

    __updateColumns: list = None
    __updateValues: list = None

    def __init__(self, sql_db):
        super().__init__(sql_db)
        self.__updateColumns = []
        self.__updateValues = []

    def update_kv(self, key, value):
        self.__updateColumns.append('%s = ?' % key)
        self.__updateValues.append(value)

    def execute(self):
        self._check_table_valid()
        if len(self.__updateColumns) <= 0:
            return

        if len(self._conditionColumns) <= 0:
            raise SQLException('%s: conditionColumns missing.' % __class__)

        query = 'UPDATE %s SET %s WHERE %s' % (self._table,
                                               ', '.join(self.__updateColumns),
                                               ' AND '.join(self._conditions()))
        self._mysqlDB.update(query, self._stmt_values())

    def _stmt_values(self):
        return self.__updateValues + self._conditionValues

