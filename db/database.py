from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from core.config import settings

# sqlalchemy
# 教程
# https://docs.sqlalchemy.org.cn/en/20/tutorial/engine.html

engine = create_engine(settings.DATABASE, echo=True)

Base = declarative_base()

# autocommit=False表示手动提交事务，只有调用session.commit()时才会把对数据库的修改提交到数据库。
# autoflush=False 则是关闭自动刷新，也就是不会在每次执行查询或修改操作后，立即从数据库加载最新数据。
# bind=engine就是把前面创建的数据库引擎绑定到这个会话工厂上。
# 不用autocommit=True是因为手动控制事务提交有很多好处呀。
# （掰着手指一项一项数给你听）
# 比如可以把多个操作打包成一个事务，要么都成功，要么都失败，保证数据的一致性和完整性。
# 而且在一些复杂的业务逻辑中，可能需要先进行一些检查，然后再决定是否提交事务，手动提交就更灵活啦。

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_tables():
    Base.metadata.create_all(bind=engine)