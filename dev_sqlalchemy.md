# SQLAlchemy 2.0+ 统一教材

***

# Quickstart

```shell

cd backend
uc sync

uv run ./sql/core.py

```

# 版本检查

查看版本号是不是 2.0

```python
import sqlalchemy
print(sqlalchemy.__version__)

```

# 建立连接 - 引擎

每个连接到数据库的 SQLAlchemy 应用程序都需要使用引擎。

在本教程中，我们将使用仅内存中的 SQLite 数据库。这是一种简单的测试方法，无需设置实际的预先存在的数据库。引擎是使用 create\_engine() 函数创建的：

```python
from sqlalchemy import create_engine
engine = create_engine("sqlite+pysqlite:///:memory:", echo=True)
```

create\_engine 的主要参数是一个字符串 URL，在上面作为字符串“sqlite+pysqlite:///:memory:”传递。该字符串向引擎指示三个重要事实：

- 数据库驱动程序：pysqlite
- 数据库类型：SQLite
- 数据库文件路径：:memory: 表示仅在内存中创建数据库，不写入磁盘

# 使用事务和 DBAPI

准备好引擎对象后，我们可以深入了解引擎及其主要端点（连接和结果）的基本操作。我们还将介绍这些对象的 ORM 外观，称为会话。

使用 ORM 时，引擎由会话管理。现代 SQLAlchemy 中的会话强调事务和 SQL 执行模式，该模式与下面讨论的连接的模式基本相同，因此虽然本小节以核心为中心，但这里的所有概念也与 ORM 使用相关，建议所有 ORM 学习者使用。本节末尾将把 Connection 使用的执行模式与 Session 进行比较。

```python
# core数据库操作

from sqlalchemy import text

with engine.connect() as conn:
    result = conn.execute(text("select 'hello world'"))
    print(result.all())
```

DBAPI 连接不会自动提交。如果我们想提交一些数据怎么办？我们可以更改上面的示例来创建一个表，插入一些数据，然后使用 Connection.commit() 方法在我们拥有 Connection 对象的块内提交事务：

```python
# core数据库操作

with engine.connect() as conn:
    conn.execute(text("CREATE TABLE some_table (x int, y int)"))
    conn.execute(
        text("INSERT INTO some_table (x, y) VALUES (:x, :y)"),
        [{"x": 1, "y": 1}, {"x": 2, "y": 4}],
    )
    conn.commit()
```

上面，我们执行两个 SQL 语句，一个“CREATE TABLE”语句和一个参数化的“INSERT”语句。为了提交我们在块中完成的工作，我们调用 Connection.commit() 方法来提交事务。 SQLAlchemy 将这种风格称为“随时提交”。

还有另一种提交数据的方式。我们可以预先将“连接”块声明为交易块。为此，我们使用 Engine.begin() 方法来获取连接，而不是 Engine.connect() 方法。此方法将管理连接的范围，并且还将事务内的所有内容包含在事务内，如果块成功，则在末尾使用 COMMIT；如果引发异常，则在末尾使用 ROLLBACK。这种风格称为开启一次：

```python
# core数据库操作

with engine.begin() as conn:
    conn.execute(
        text("INSERT INTO some_table (x, y) VALUES (:x, :y)"),
        [{"x": 6, "y": 8}, {"x": 9, "y": 10}],
    )
```

您应该更喜欢“开启一次”样式，因为它更短并且预先显示了整个块的意图。然而，在本教程中，我们将使用“随时提交”风格，因为它对于演示目的更加灵活。

# 语句执行的基础知识

数据库运行 SQL 语句的示例，使用名为 Connection.execute() 的方法，结合名为 text() 的对象，并返回名为 Result 的对象。在本节中，我们将更详细地说明这些组件的机制和交互。

本节中的大部分内容同样适用于使用 Session.execute() 方法时的现代 ORM 使用，该方法的工作方式与 Connection.execute() 非常相似，包括使用 Core 使用的相同 Result 接口传递 ORM 结果行。

### 获取行

我们首先将通过使用之前插入的行，在我们创建的表上运行文本 SELECT 语句来更仔细地说明 Result 对象：

```python
# core数据库操作

with engine.connect() as conn:
    result = conn.execute(text("SELECT x, y FROM some_table"))
    for row in result:
        print(f"x: {row.x}  y: {row.y}")
```

Row 对象本身的作用类似于 Python 命名元组。

下面我们举例说明访问行的多种方法:

1. 元组分配 - 这是最符合 Python 习惯的风格，即在收到变量时按位置将变量分配给每一行：

```python

result = conn.execute(text("select x, y from some_table"))

for x, y in result:
    print(x, y)
```

1. 整数索引 - 元组是 Python 序列，因此也可以使用常规整数访问：

```python
result = conn.execute(text("select x, y from some_table"))

for row in result:
    print(row[0], row[1])
```

1. 属性名称 - 由于这些是 Python 命名的元组，因此元组具有与每列名称匹配的动态属性名称。这些名称通常是 SQL 语句分配给每行中的列的名称。虽然它们通常是相当可预测的，并且也可以通过标签进行控制，但在定义较少的情况下，它们可能会受到特定于数据库的行为的影响：

```python
result = conn.execute(text("select x, y from some_table"))

for row in result:
    print(row.x, row.y)
```

1. 映射访问 - 要接收行作为 Python 映射对象（本质上是 Python 通用 dict 对象接口的只读版本），可以使用 Result.mappings() 修饰符将 Result 转换为 MappingResult 对象；这是一个结果对象，它生成类似字典的 RowMapping 对象而不是 Row 对象：

```python
result = conn.execute(text("select x, y from some_table"))

for row in result.mappings():
    x = row["x"]
    y = row["y"]
    print(x, y)
```

### 发送参数， {"y": 2}就是绑定参数 :y 的值为 2

```python
# core数据库操作

with engine.connect() as conn:
    result = conn.execute(text("SELECT x, y FROM some_table WHERE y > :y"), {"y": 2})
    for row in result:
        print(f"x: {row.x}  y: {row.y}")
```

### 发送多个参数

操作相当于为每个参数集运行一次给定的 INSERT 语句，
不同之处在于该操作将被优化以获得
**跨多行的更好性能**

```python
# core数据库操作
# 跨多行的更好性能

with engine.connect() as conn:
    conn.execute(
        text("INSERT INTO some_table (x, y) VALUES (:x, :y)"),
        [{"x": 11, "y": 12}, {"x": 13, "y": 14}],
    )
    conn.commit()
```

# 使用 ORM 会话执行

使用 ORM 时的基本事务/数据库交互对象称为会话。
在现代 SQLAlchemy 中，该对象的使用方式与 Connection 非常相似，
事实上，在使用 Session 时，它在内部引用一个 Connection，用于发出 SQL。

```python

from sqlalchemy.orm import Session

stmt = text("SELECT x, y FROM some_table WHERE y > :y ORDER BY x, y")
with Session(engine) as session:
    result = session.execute(stmt, {"y": 6})
    for row in result:
        print(f"x: {row.x}  y: {row.y}")
```

此外，与 Connection 一样，Session 具有使用 Session.commit() 方法的“随时提交”行为，如下所示，使用文本 UPDATE 语句来更改我们的一些数据：

```python

with Session(engine) as session:
    result = session.execute(
        text("UPDATE some_table SET y=:y WHERE x=:x"),
        [{"x": 9, "y": 11}, {"x": 13, "y": 15}],
    )
    session.commit()
```

# 使用数据库元数据

在使用ORM时，我们声明Table元数据的过程通常与声明映射类的过程结合在一起。

映射的类是我们想要创建的任何 Python 类，

该类将具有链接到数据库表中的列的属性。

```python
from sqlalchemy.orm import DeclarativeBase
class Base(DeclarativeBase):
    pass
```

# 声明映射类

```python

from typing import List
from typing import Optional
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "user_account"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    fullname: Mapped[Optional[str]]
    addresses: Mapped[List["Address"]] = relationship(back_populates="user")
    def __repr__(self) -> str:
        return f"User(id={self.id!r}, name={self.name!r}, fullname={self.fullname!r})"

class Address(Base):
    __tablename__ = "address"
    id: Mapped[int] = mapped_column(primary_key=True)
    email_address: Mapped[str]
    user_id = mapped_column(ForeignKey("user_account.id"))
    user: Mapped[User] = relationship(back_populates="addresses")
    def __repr__(self) -> str:
        return f"Address(id={self.id!r}, email_address={self.email_address!r})"

```

上面的两个类，User 和 Address，现在被称为 ORM 映射类，可用于 ORM 持久化和查询操作，这将在后面介绍。有关这些类的详细信息包括：

每个类都引用作为声明性映射过程的一部分生成的 Table 对象，该对象通过将字符串分配给 DeclarativeBase.__tablename__ 属性来命名。创建类后，可以从 DeclarativeBase.__table__ 属性获取生成的表。

为了指示表中的列，我们使用mapped\_column() 构造，并结合基于映射类型的键入注释。该对象将生成应用于表构造的 Column 对象。

显式类型注释的使用是完全可选的。根据每个mapped\_column()构造中的需要使用更显式的类型对象，例如Integer和String以及nullable=False。

# 从 ORM 映射向数据库发送 DDL

如果表不存在，创建表。

```python
Base.metadata.create_all(engine)
```

# 使用数据

## 插入数据

一个简单的 Insert 示例同时说明了目标表和 VALUES 子句：

```python

from sqlalchemy import insert
stmt = insert(user_table).values(name="spongebob", fullname="Spongebob Squarepants")

# 上面的 stmt 变量是 Insert 的一个实例。大多数 SQL 表达式都可以就地进行字符串化，作为查看所生成内容的一般形式的一种方法：

print(stmt)

# INSERT INTO user_account (name, fullname) VALUES (:name, :fullname)

# 字符串化形式是通过生成对象的编译形式来创建的，其中包括语句的特定于数据库的字符串 SQL 表示形式；我们可以使用 ClauseElement.compile() 方法直接获取这个对象：

compiled = stmt.compile()

compiled.params

# {'name': 'spongebob', 'fullname': 'Spongebob Squarepants'}

```

下面的示例一次执行,插入了两列的语句, 与orm逐行插入不同：

```python
with engine.connect() as conn:
    result = conn.execute(
        insert(user_table),
        [
            {"name": "sandy", "fullname": "Sandy Cheeks"},
            {"name": "patrick", "fullname": "Patrick Star"},
        ],
    )
    conn.commit()
```

## 插入...返回

```python

insert_stmt = insert(address_table).returning(
    address_table.c.id, address_table.c.email_address
)
print(insert_stmt)

# ⚠️注意：MySQL 不支持 RETURNING 语法；PostgreSQL 原生支持；SQLAlchemy 2.0 对它做了封装。
# 作用：插入数据之后，直接拿回数据库生成的字段，比如自增 id、create_time，不用再额外执行一次SELECT查询。

```

### 插入…从选择

从数据库的其他部分直接复制到一组新的行中，
而不实际从客户端获取并重新发送数据时，可以使用此构造。

```python
select_stmt = select(user_table.c.id, user_table.c.name + "@aol.com")
insert_stmt = insert(address_table).from_select(
    ["user_id", "email_address"], select_stmt
)
print(insert_stmt)

```

# Select 选取数据

```python
from sqlalchemy import select
stmt = select(user_table).where(user_table.c.name == "spongebob")
print(stmt)


print(select(User).where(User.name == "spongebob")）

print(select(user_table.c.name, user_table.c.fullname))

print(select(user_table.c["name", "fullname"]))

print(select(User))

row = session.execute(select(User)).first()
print(row)

user = session.scalars(select(User)).first()
print(user)

print(select(User.name, User.fullname))

row = session.execute(select(User.name, User.fullname)).first()
print(row)


# 设置 COLUMNS 和 FROM 子句

# Table.c 访问器

# Table.c 访问器

# Table.c 访问器

# 要使用核心方法从各个列中进行 SELECT，可以从 Table.c 访问器访问 Column 对象，并且可以直接发送； FROM 子句将被推断为由这些列表示的所有 Table 和其他 FromClause 对象的集合：

print(select(user_table.c.name, user_table.c.fullname))
# 等于
print(select(user_table.c["name", "fullname"]))

# 执行的都是
# SELECT user_table.name, user_table.fullname FROM user_table



# 选择 ORM 实体和列

row = session.execute(select(User)).first()

row[0]

print(row[0])

# 要注意，是row[0]，而不是row

# User(id=1, name='spongebob', fullname='Spongebob Squarepants')

# 强烈建议使用 session.scalars() 方法，而不是直接使用 row[0]，因为 row[0] 是一个 ORM 实体，而不是一个字典。

user = session.scalars(select(User)).first()
print(user)

# User(id=1, name='spongebob', fullname='Spongebob Squarepants')



row = session.execute(select(User.name, User.fullname)).first()
print(row)
# ('spongebob', 'Spongebob Squarepants')


```

这些方法也可以混合使用，如下所示，我们选择 User 实体的 name 属性作为行的第一个元素，并将其与第二个元素中的完整 Address 实体组合：

```python
session.execute(
    select(User.name, Address).where(User.id == Address.user_id).order_by(Address.id)
).all()

```

从带标签的 SQL 表达式中选择

```python

print(
    select(address_table.c.email_address)
    .where(user_table.c.name == "squidward")
    .where(address_table.c.user_id == user_table.c.id)
)

# 等于

print(
    select(address_table.c.email_address).where(
        user_table.c.name == "squidward",
        address_table.c.user_id == user_table.c.id,
    )
)

# SELECT address.email_address
# FROM address, user_account
# WHERE user_account.name = :name_1 AND address.user_id = user_account.id



# “AND”和“OR”连词都可以直接使用 and_() 和 or_() 函数使用，如下以 ORM 实体为例：

from sqlalchemy import and_, or_
print(
    select(Address.email_address).where(
        or_(
            User.name == "squidward",
            and_(Address.user_id == User.id, User.name == "sandy"),
        )
    )
)


# 对于针对单个实体的简单“相等”比较，还有一种称为 Select.filter_by() 的流行方法，它接受与列键或 ORM 属性名称匹配的关键字参数。它将根据最左边的 FROM 子句或最后加入的实体进行过滤：

print(select(User).filter_by(name="spongebob", fullname="Spongebob Squarepants"))



# 如果我们要放置两个表中的列，那么我们会得到一个以逗号分隔的 FROM 子句：
print(select(user_table.c.name, address_table.c.email_address))

# SELECT user_account.name, address.email_address FROM user_account, address


# 为了将这两个表连接在一起，我们通常在 Select 上使用两种方法之一。第一个是 Select.join_from() 方法，它允许我们显式指示 JOIN 的左侧和右侧：

print(
    select(user_table.c.name, address_table.c.email_address).join_from(
        user_table, address_table
    )
)

# SELECT user_account.name, address.email_address FROM user_account JOIN address ON user_account.id = address.user_id



# 另一个是 Select.join() 方法，它仅指示 JOIN 的右侧，推断左侧：

print(select(user_table.c.name, address_table.c.email_address).join(address_table))

# SELECT user_account.name, address.email_address FROM user_account JOIN address ON user_account.id = address.user_id


# 如果没有按照我们想要的方式从 columns 子句中推断出元素，我们还可以选择显式地将元素添加到 FROM 子句中。我们使用 Select.select_from() 方法来实现此目的，如下所示，我们将 user_table 建立为 FROM 子句中的第一个元素，并使用 Select.join() 建立 address_table 作为第二个元素：

print(select(address_table.c.email_address).select_from(user_table).join(address_table))

# SELECT address.email_address FROM user_account JOIN address ON user_account.id = address.user_id



# 我们可能想要使用 Select.select_from() 的另一个示例是，如果我们的 columns 子句没有足够的信息来为 FROM 子句提供信息。例如，要从常见 SQL 表达式 count(*) 中进行 SELECT，我们使用名为 sqlalchemy.sql.expression.func 的 SQLAlchemy 元素来生成 SQL count() 函数：

from sqlalchemy import func
print(select(func.count("*")).select_from(user_table))

# SELECT count(:count_2) AS count_1 FROM user_account



# 设置 ON 子句

print(
    select(address_table.c.email_address)
    .select_from(user_table)
    .join(address_table, user_table.c.id == address_table.c.user_id)
)

# SELECT address.email_address
# FROM user_account JOIN address 
# ON user_account.id = address.user_id


# 外部连接和完整连接

print(select(user_table).join(address_table, isouter=True))
print(select(user_table).join(address_table, full=True))


# ORDER BY, GROUP BY, HAVING

print(select(user_table).order_by(user_table.c.name))
print(select(User).order_by(User.fullname.desc()))


from sqlalchemy import func
count_fn = func.count(user_table.c.id)
print(count_fn)
# count(user_account.id)


with engine.connect() as conn:
    result = conn.execute(
        select(User.name, func.count(Address.id).label("count"))
        .join(Address)
        .group_by(User.name)
        .having(func.count(Address.id) > 1)
    )
    print(result.all())

```

```python

session.execute(
    select(User.name, Address).where(User.id == Address.user_id).order_by(Address.id)
).all()

```

# Update & Delete

```python

# 更新多个实体，用对象的方式

update_stmt = (
    update(user_table)
    .where(user_table.c.id == address_table.c.user_id)
    .where(address_table.c.email_address == "patrick@aol.com")
    .values(
        {
            user_table.c.fullname: "Pat",
            address_table.c.email_address: "pat@aol.com",
        }
    )
)
from sqlalchemy.dialects import mysql
print(update_stmt.compile(dialect=mysql.dialect()))



# 更新单个实体
from sqlalchemy import update
stmt = (
    update(user_table)
    .where(user_table.c.name == "patrick")
    .values(fullname="Patrick the Star")
)
print(stmt)


from sqlalchemy import delete
stmt = delete(user_table).where(user_table.c.name == "patrick")
print(stmt)



# DELETE Statements

from sqlalchemy import delete
stmt = delete(user_table).where(user_table.c.name == "patrick")
print(stmt)
# DELETE FROM user_account WHERE user_account.name = :name_1




```

<br />

