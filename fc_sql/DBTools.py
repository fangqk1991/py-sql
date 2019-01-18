from fc_sql import ISQLHandler, SQLAdder, SQLModifier, SQLRemover, SQLException, SQLSearcher


class DBTools:

    __handler: ISQLHandler = None

    def __init__(self, handler):
        self.__handler = handler

    def add(self, params):
        handler = self.__handler
        sql = handler.sql_instance()
        table = handler.sql_table()
        cols = handler.sql_insertable_cols()

        builder = SQLAdder(sql)
        builder.set_table(table)

        for key in cols:
            value = None
            if key in params:
                value = params[key]
            builder.insert_kv(key, value)

        builder.execute()

    def update(self, params):
        handler = self.__handler
        sql = handler.sql_instance()
        table = handler.sql_table()
        cols = handler.sql_modifiable_cols()

        builder = SQLModifier(sql)
        builder.set_table(table)

        p_key = handler.sql_primary_key()
        p_keys = p_key if isinstance(p_key, list) else [p_key]

        for key in p_keys:
            builder.check_primary_key(params, key)
            params.pop(key, None)

        for key in cols:
            if key in params:
                builder.update_kv(key, params[key])

        builder.execute()

    def delete(self, params):
        handler = self.__handler
        sql = handler.sql_instance()
        table = handler.sql_table()

        builder = SQLRemover(sql)
        builder.set_table(table)

        p_key = handler.sql_primary_key()
        p_keys = p_key if isinstance(p_key, list) else [p_key]

        for key in p_keys:
            builder.check_primary_key(params, key)

        builder.execute()

    def search_single(self, params, check_primary_key=True):
        if check_primary_key:
            handler = self.__handler
            p_key = handler.sql_primary_key()
            p_keys = p_key if isinstance(p_key, list) else [p_key]
            for key in p_keys:
                if key not in params:
                    raise SQLException('%s: primary key missing.' % __class__)

        items = self.fetch_list(params, 0, 1)
        if len(items) > 0:
            return items[0]
        return None

    def fetch_list(self, params, page, feeds_per_page):
        handler = self.__handler
        sql = handler.sql_instance()
        table = handler.sql_table()
        cols = handler.sql_cols()

        builder = SQLSearcher(sql)
        builder.set_table(table)
        builder.set_page_info(page, feeds_per_page)

        for key in cols:
            builder.add_column(key)

        for key, value in params.items():
            builder.add_condition_kv(key, value)

        return builder.query_list()

    def fetch_count(self, params):
        handler = self.__handler
        sql = handler.sql_instance()
        table = handler.sql_table()
        cols = handler.sql_cols()

        builder = SQLSearcher(sql)
        builder.set_table(table)

        for key in cols:
            builder.add_column(key)

        for key, value in params:
            builder.add_condition_kv(key, value)

        return builder.query_count()


