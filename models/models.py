from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func

from db.database import Base

class UserModel(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    password = Column(String)
    email = Column(String)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    gender = Column(String)