from sqlalchemy import Column, DateTime, Integer, String, Text
from sqlalchemy.sql import func
from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(256), unique=True, index=True)
    password = Column(String(256))
    created_at = Column(DateTime, server_default=func.now())

class Expense(Base):
    __tablename__ = "expenses"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True)
    amount = Column(Integer)
    memo = Column(Text)
    created_at = Column(DateTime, server_default=func.now())