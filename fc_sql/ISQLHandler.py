import abc
from abc import ABCMeta


class ISQLHandler(metaclass=ABCMeta):

    def __init__(self):
        pass

    @abc.abstractmethod
    def sql_instance(self):
        pass

    @abc.abstractmethod
    def sql_table(self):
        pass

    @abc.abstractmethod
    def sql_cols(self):
        pass

    def sql_insertable_cols(self):
        return self.sql_cols()

    def sql_modifiable_cols(self):
        return self.sql_insertable_cols()

    @abc.abstractmethod
    def sql_primary_key(self):
        pass
