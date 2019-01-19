import decimal
import numbers
import re

import pymysql
from pymysql import OperationalError
from pymysql.cursors import DictCursor


class FCDatabase:

    __host = None
    __account = None
    __password = None
    __db_name = None

    def init(self, host, account, password, db_name):
        self.__host = host
        self.__account = account
        self.__password = password
        self.__db_name = db_name
        return self

    def connect(self):
        return pymysql.connect(self.__host, self.__account, self.__password, self.__db_name)

    def query(self, query, params):

        query = re.sub('\?', '%s', query)

        connection = self.connect()
        with connection.cursor(DictCursor) as cursor:
            cursor.execute(query, params)
            records = []
            for row in cursor:
                for k, v in row.items():
                    if isinstance(v, numbers.Number):
                        pass
                    elif isinstance(v, decimal.Decimal):
                        row[k] = float(v)
                    elif v is not None:
                        row[k] = str(v)
                records.append(row)

            cursor.close()
            connection.close()
            return records

    def update(self, query, params):

        query = re.sub('\?', '%s', query)

        connection = self.connect()

        with connection.cursor() as cursor:
            cursor.execute(query, params)
            connection.commit()
            cursor.close()
            connection.close()

    def fc_adder(self):
        from .SQLAdder import SQLAdder
        return SQLAdder(self)

    def fc_modifier(self):
        from .SQLModifier import SQLModifier
        return SQLModifier(self)

    def fc_remover(self):
        from .SQLRemover import SQLRemover
        return SQLRemover(self)

    def fc_searcher(self):
        from .SQLSearcher import SQLSearcher
        return SQLSearcher(self)
