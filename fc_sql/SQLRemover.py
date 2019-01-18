from .SQLException import SQLException
from .BuilderBase import BuilderBase


class SQLRemover(BuilderBase):

    def execute(self):
        self._check_table_valid()

        if len(self._conditionColumns) <= 0:
            raise SQLException('%s: conditionColumns missing.' % __class__)

        query = 'DELETE FROM %s WHERE %s' % (
            self._table,
            ' AND '.join(self._conditions())
        )
        self._mysqlDB.update(query, self._stmt_values())

