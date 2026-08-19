import sqlalchemy

# 版本检查
print("----# 版本检查-----------------------")
print(sqlalchemy.__version__)


# 建立连接 - 引擎
print("----# 建立连接 - 引擎-----------------------")
from sqlalchemy import create_engine
engine = create_engine("sqlite+pysqlite:///:memory:", echo=True)



## 使用事务和 DBAPI
print("----# 使用事务和 DBAPI-----------------------")
from sqlalchemy import text
with engine.connect() as conn:
    result = conn.execute(text("select 'hello world'"))
    print(result.all())


# 语句执行的基础知识
print("----# 语句执行的基础知识-----------------------")
with engine.connect() as conn:
    conn.execute(text("CREATE TABLE some_table (x int, y int)"))
    conn.execute(
        text("INSERT INTO some_table (x, y) VALUES (:x, :y)"),
        [{"x": 1, "y": 1}, {"x": 2, "y": 4}, {"x": 3, "y": 6}, {"x": 4, "y": 8}],
    )
    conn.commit()


# 获取行
print("----# 获取行-----------------------")
with engine.connect() as conn:
    result = conn.execute(text("SELECT x, y FROM some_table"))
    for row in result:
        print(f"x: {row.x}  y: {row.y}")


# 发送参数, {"y": 2}就是绑定参数 :y 的值为 2
print("----# 发送参数-----------------------")
with engine.connect() as conn:
    result = conn.execute(text("SELECT x, y FROM some_table WHERE y > :y"), {"y": 2})
    for row in result:
        print(f"x: {row.x}  y: {row.y}")


print("----# 发送多个参数-----------------------")
with engine.connect() as conn:
    conn.execute(
        text("INSERT INTO some_table (x, y) VALUES (:x, :y)"),
        [{"x": 11, "y": 12}, {"x": 13, "y": 14}],
    )
    conn.commit()
