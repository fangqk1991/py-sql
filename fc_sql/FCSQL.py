import decimal
import numbers
import re

import pymysql
from pymysql import OperationalError
from pymysql.cursors import DictCursor


class FCSQL:

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

    def query(self, query, params, retry=False):

        query = re.sub('\?', '%s', query)

        connection = self.connect()
        with connection.cursor(DictCursor) as cursor:

            try:
                cursor.execute(query, params)
            except OperationalError as e:
                if not retry:
                    self.query(query, params, True)
                else:
                    raise e

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
