import random
from fc_sql import FCDatabase

HOST = '127.0.0.1'
ACCOUNT = 'SOME_ACCOUNT'
PASSWORD = 'SOME_PASSWORD'
DB_NAME = 'demo_db'
TABLE = 'demo_table'

database = FCDatabase()
database.init(HOST, ACCOUNT, PASSWORD, DB_NAME)


def show_records():
    searcher = database.fc_searcher()
    searcher.set_table(TABLE)
    searcher.set_columns(['uid', 'key1', 'key2'])
    # searcher.set_columns(['*'])
    items = searcher.query_list()
    count = searcher.query_count()
    print('{} records: {}'.format(count, items))
    return items


show_records()

for _ in range(5):
    adder = database.fc_adder()
    adder.set_table(TABLE)
    adder.insert_kv('key1', 'K1 - %04d' % random.randint(0, 9999))
    adder.insert_kv('key2', 'K2 - %04d' % random.randint(0, 9999))
    adder.execute()

show_records()

modifier = database.fc_modifier()
modifier.set_table(TABLE)
modifier.update_kv('key1', 'Odd')
modifier.update_kv('key2', 'Changed')
modifier.add_condition_kv('MOD(uid, 2)', 1)
modifier.execute()

show_records()

remover = database.fc_remover()
remover.set_table(TABLE)
remover.add_special_condition('uid > ?', 3)
remover.execute()

show_records()
