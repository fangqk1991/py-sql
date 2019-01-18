# 简介
MySQL 增删改查调用框架，Python 版。

### 依赖
* Python 3

### 安装
```
pip install git+https://github.com/fangqk1991/py-sql.git
```

### 使用
#### 测试表结构
```
CREATE TABLE IF NOT EXISTS stock_demo
(
  code CHAR(10)     NOT NULL PRIMARY KEY,
  name VARCHAR(255) NOT NULL DEFAULT ''
);
```

#### 常规使用
```
# instance
db = FCSQL()
db.init(Host, Account, Password, DBName)

# Adder
builder = SQLAdder(db)
builder.set_table('stock_demo')
builder.insert_kv('code', 'HK.00700')
builder.insert_kv('name', 'Tencent')
builder.execute()

# Modifier
builder = SQLModifier(db)
builder.set_table('stock_demo')
builder.update_kv('name', '腾讯控股')
builder.add_condition_kv('code', 'HK.00700')
builder.execute()

# Remover
builder = SQLRemover(db)
builder.set_table('stock_demo')
builder.add_condition_kv('code', 'HK.00700')
builder.execute()

# Searcher
builder = SQLSearcher(db)
builder.set_table('stock_demo')
builder.set_columns(['code', 'name'])
items = builder.query_list()
count = builder.query_count()
```
