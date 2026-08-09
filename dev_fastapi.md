from pygments.lexer import default

# Fast api

# 创建 FastAPI 依赖项

我们一直在每个路径操作中，在一个 with 块中创建会话。

让我们重构这些会话以使用 FastAPI 依赖项。

一个 FastAPI 依赖项非常简单，它只是一个返回值的函数。

它可以使用 yield 而不是 return，在这种情况下，FastAPI 将确保在请求完成后，它会执行 yield 之后的所有代码。

```python
from fastapi import Depends, FastAPI, HTTPException, Query
from sqlmodel import Field, Session, SQLModel, create_engine, select

# Code here omitted 👈

def get_session():
    with Session(engine) as session:
        yield session

# Code here omitted 👈

@app.post("/heroes/", response_model=HeroPublic)
def create_hero(*, session: Session = Depends(get_session), hero: HeroCreate):
    db_hero = Hero.model_validate(hero)
    session.add(db_hero)
    session.commit()
    session.refresh(db_hero)
    return db_hero

```



# 查询参数和字符串验证

### 附加验证

```python
from typing import Annotated

from fastapi import FastAPI, Query

app = FastAPI()


@app.get("/items/")
async def read_items(q: Annotated[str | None, Query(max_length=50)] = None):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results
```

```python
async def read_items(q: Annotated[str | None, Query(max_length=50)] = None):
async def read_items(q: str | None = Query(default=None, max_length=50)):

q: Annotated[str, Query()] = "rick"
q: str = Query(default="rick")
```


Annotated 的优点¶
如果有一个必需的参数（没有默认值），Python 也会报错


# SQLModel 最强大的特性。💎

这些模型中的每一个都只是一个 数据模型，或者既是数据模型又是 表模型。

我们可以使用继承来避免这些模型中的重复信息。

```python
from fastapi import FastAPI
from sqlmodel import Field, Session, SQLModel, create_engine, select


class HeroBase(SQLModel):
    name: str = Field(index=True)
    secret_name: str
    age: int | None = Field(default=None, index=True)


class Hero(HeroBase, table=True):
    id: int | None = Field(default=None, primary_key=True)


class HeroCreate(HeroBase):
    pass


class HeroPublic(HeroBase):
    id: int

```

全部继承 HeroBase

请注意，Hero 现在不再继承自 SQLModel，而是继承自 HeroBase。

创建时不需要ID

所以，现在我们只直接声明一个字段 id，它在这里是 int | None，并且是 primary_key。


# 总结

- 只从数据模型继承，不要从 表模型 继承， 比如创建接口使用 HeroCreate， 而不是HeroBase

- 继承来 避免信息和代码重复，保持简单。



# 获取单个英雄

```python
@app.get("/heroes/{hero_id}", response_model=HeroPublic)
```

# 获取多个英雄

向查询参数添加限制和偏移量

让我们向查询参数添加 limit 和 offset。

默认情况下，我们将返回数据库中的第一个结果，所以 offset 将有一个默认值 0。

并且默认情况下，我们将最多返回 100 个英雄，所以 limit 将有一个默认值 100。


```python
from fastapi import FastAPI, HTTPException, Query
from sqlmodel import Field, Session, SQLModel, create_engine, select

# Code here omitted 👈

@app.get("/heroes/", response_model=list[HeroPublic])
def read_heroes(offset: int = 0, limit: int = Query(default=100, le=100)):
    with Session(engine) as session:
        heroes = session.exec(select(Hero).offset(offset).limit(limit)).all()
        return heroes

# Code below omitted 👇
```

# 更新数据


```python
# Code above omitted 👆

@app.patch("/heroes/{hero_id}", response_model=HeroPublic)
def update_hero(hero_id: int, hero: HeroUpdate):
    with Session(engine) as session:
        db_hero = session.get(Hero, hero_id)
        if not db_hero:
            raise HTTPException(status_code=404, detail="Hero not found")
        hero_data = hero.model_dump(exclude_unset=True)
        db_hero.sqlmodel_update(hero_data)
        session.add(db_hero)
        session.commit()
        session.refresh(db_hero)
        return db_hero
```

hero.model_dump
只得到用户变更的数据对象

sqlmodel_update
检查db_hero中，该字段是否在，更新它。

配合使用


# 带关系的模型

最佳实践：
- 基本模型不带关系，

- 表字段定义关系，

- 获取Hero时，定义新的模型，继承公共模型


```python

class HeroPublicWithTeam(HeroPublic):
    team: TeamPublic | None = None


class TeamPublicWithHeroes(TeamPublic):
    heroes: list[HeroPublic] = []

```


# 并发，并行

假如服务器是招商银行

并发，就是那个取号器

并行，就是柜台窗口

### 并发

程序只是一味的拿号，只做接客的事情，程序会有序处理。
async/await 协程


### 并行

并行是处理的柜台【线程】，每个线程处理一个请求。
【进程】，每个进程有多个线程。
