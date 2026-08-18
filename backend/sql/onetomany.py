import asyncio
from sqlalchemy import ForeignKey, String, Text, select
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

engine = create_async_engine("sqlite+aiosqlite:///:memory:", echo=True)

class Base(DeclarativeBase):
    pass

# 一对多 + 多对多

# 多对多关系, 中间表
class ArticleTag(Base):
    __tablename__ = "article_tag"
    article_id: Mapped[int] = mapped_column(ForeignKey("article.id"), primary_key=True)
    tag_id: Mapped[int] = mapped_column(ForeignKey("tag.id"), primary_key=True)

class User(Base):
    __tablename__ = "user"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    fullname: Mapped[str] = mapped_column(String(100))
    email: Mapped[str|None] = mapped_column(String(100))

    # 一对多关系
    articles: Mapped[list["Article"]] = relationship(back_populates="author")

class Article(Base):
    __tablename__ = "article"
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(100))
    content: Mapped[str] = mapped_column(Text)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))

    # 反向一对多
    author: Mapped[User] = relationship(back_populates="articles")
    # 多对多关系
    tags: Mapped[list["Tag"]] = relationship(secondary=ArticleTag.__table__, back_populates="articles")

class Tag(Base):
    __tablename__ = "tag"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    articles: Mapped[list[Article]] = relationship(secondary=ArticleTag.__table__,back_populates="tags")

async def main():
    # 创建数据库表
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    async with AsyncSession(engine) as session:
        # 新增数据
        u1 = User(name="张三", fullname="张大三", email="zhangsan@example.com")
        a1 = Article(title="Python入门", content="sqlalchemy练习", author=u1)
        a2 = Article(title="Python精通", content="sqlalchemy静姐", author=u1)
        t1 = Tag(name="技术")
        t2 = Tag(name="数据库")
        a1.tags.append(t1)
        a1.tags.append(t2)
        a2.tags.append(t2)
        
        session.add_all([u1, a1, a2, t2, t1])
        await session.commit()

        # 2.查询单条
        res = await session.execute(select(User).where(User.name == "张三"))
        user = res.scalar_one_or_none()
        print("查询用户:", user)
        
        res = await session.execute(select(User,Article).join(Article, isouter=True))
        for u,a in res.all():
            print(f"用户:{u.name},文章标题:{a.title}")
    


if __name__ == "__main__":
    asyncio.run(main())