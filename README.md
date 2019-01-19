# 简介
这是一个对 MySQL 进行简单增删改查的调用框架，Python 版。

### 其他版本
* [ObjC 版](https://github.com/fangqk1991/iOS-SQL)
* [PHP 版](https://github.com/fangqk1991/php-sql)

### 依赖
* Python 3
* [PyMySQL](https://github.com/PyMySQL/PyMySQL)

### 安装
```
pip install git+https://github.com/fangqk1991/py-sql.git
```

### 使用
#### FCDatabase
```
# 初始化
def init(self, host, account, password, db_name)

# 直接查询
def query(self, query, params)
def update(self, query, params)
```

#### BuilderBase (Adder/Modifier/Remover/Searcher 的基类)
```
# 初始化方法
def __init__(self, db: FCDatabase)
ms[key])

# 添加执行条件（简单匹配）
def add_condition_kv(self, key, value)

// 添加执行条件（自定义）
def add_special_condition(self, condition, *args)
```

### SQLAdder
```
def insert_kv(self, key, value)
def execute(self)
```

### SQLModifier
```
def update_kv(self, key, value)
def execute(self)
```

### SQLRemover
```
def execute(self)
```

### SQLSearcher
```
# 采用 DISTINCT
def mark_distinct(self)

# 设置列
def set_columns(self, columns)

# 添加列
def add_column(self, column)

# 添加排序规则
def add_order_rule(self, sort_key, direction)

# 设置页码信息
def set_page_info(self, page, feeds_per_page)

# 设置附加语句
def set_option_str(self, option_str)

# 查询
def query_list(self)
def query_count(self)
```

### 示例
[Demo](https://github.com/fangqk1991/py-sql/tree/master/demos/sql-demo.py)

```
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
```

![](https://image.fangqk.com/2019-01-19/py-sql-demo.jpg)
