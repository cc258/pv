
from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.app.core.security import get_password_hash, verify_password
from backend.app.core.config import settings
from backend.app.models.user import User


def get_user_by_name(*, session: Session, username: str):
    statement = select(User).where(User.username == username)
    db_user = session.execute(statement).scalars().first()
    return db_user


# create
def create_user(*, session: Session, username: str, password: str) -> User:
    user = User(
        username=username,
        hashed_password=get_password_hash(password),
    )
    session.add(user)
    session.commit()
    return user


# * 必须使用关键字参数，可读，安全
def authenticate(*, session: Session, username: str, password: str):
    db_user = get_user_by_name(session=session, username=username)
    if not db_user:
        verify_password(password, settings.DUMMY_HASH)
        return None
    verified, updated_password_hash = verify_password(password, db_user.hashed_password)
    if not verified:
        return None
    if updated_password_hash:
        db_user.hashed_password = updated_password_hash
        session.add(db_user)
        session.commit()
        session.refresh(db_user)
    return db_user
