# Alembic 1.18.3

# config

# Step 1 : Creating an Environment

```python
$ cd /path/to/yourproject
$ uv add alembic # 安装alembic
$ source /path/to/yourproject/.venv/bin/activate   # assuming a local virtualenv
$ alembic init alembic # 初始化alembic
```

这将创建一个使用“通用”模板的环境：

生成了一个迁移目录，名为 ```alembic```


# Step 2 : 修改.ini文件

如果只用一个数据库和通用配置启动，只需设置 SQLAlchemy URL：

```python

sqlalchemy.url = postgresql://scott:tiger@localhost/test

sqlalchemy.url = sqlite:///./databse.db

```

# Step 3 : 修改项目中的 /alembic/env.py

```python
# 导入SQLModel
from sqlmodel import SQLModel
# 导入所有模型，确保 MetaData 包含所有表定义
from models.models import User, Roles
# 找到并修改这行
target_metadata = SQLModel.metadata
```

# Usage

生成变更集合, 生成变更的脚本
```shell

alembic revision --autogenerat -m "create account table"
```

执行变更

```shell
alembic upgrade head
```





---------- 下面是一些常用方法 --------

# 列出所有模版

```python
alembic list_templates
```

上述布局使用了一个名为 `generic` 的布局模板生成。
Alembic 还包含其他环境模板。 这些可以用 `alembic list_templates` 命令列出


```shell
$ alembic list_templates
Available templates:

generic - Generic single-database configuration.
pyproject - pep-621 compliant configuration that includes pyproject.toml
async - Generic single-database configuration with an async dbapi.
multidb - Rudimentary multi-database configuration.

Templates are used via the 'init' command, e.g.:

  alembic init --template generic ./scripts
```

# 通过初始化，可以应用不同的模版

```python

alembic init --template generic ./scripts

```




# 创建迁移脚本

```python
Create a Migration Script
```

有了环境，我们可以创建新的修订版

```python
$ alembic revision -m "create account table"
```
生成了一个新文件
1975ea83b712_create_account_table.py


# 进行我们的第一次迁移

```
$ alembic upgrade head
INFO  [alembic.context] Context class PostgresqlContext.
INFO  [alembic.context] Will assume transactional DDL.
INFO  [alembic.context] Running upgrade None -> 1975ea83b712
```

# 进行我们的第二次迁移

```python
$ alembic revision -m "Add a column"
Generating /path/to/yourapp/alembic/versions/ae1027a6acf_add_a_column.py...
done

$ alembic upgrade head
INFO  [alembic.context] Context class PostgresqlContext.
INFO  [alembic.context] Will assume transactional DDL.
INFO  [alembic.context] Running upgrade 1975ea83b712 -> ae1027a6acf

```

成功


# 升级

```python
$ alembic upgrade +2

```

# 降级

```python
$ alembic downgrade -1

```

# 查看当前版本

```
$ alembic current
```


# 历史记录

```
$ alembic history --verbose
```


