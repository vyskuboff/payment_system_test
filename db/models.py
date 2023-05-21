from datetime import datetime

from sqlalchemy import (BigInteger, Column, DateTime, Float, ForeignKey,
                        Integer, String)

from .base import Base


class PrimaryIdModel(Base):
    """Абстрактная модель с id primary key"""
    __abstract__ = True

    id = Column(Integer,
                primary_key=True,
                unique=True,
                nullable=False)

    created_on = Column(DateTime(), default=datetime.now)
    updated_on = Column(DateTime(), default=datetime.now, onupdate=datetime.now)


class User(Base):
    __tablename__ = 'users'

    user_id = Column(BigInteger, unique=True, nullable=False, primary_key=True)
    username = Column(String(255), unique=False, nullable=True)
    phone = Column(String(50), unique=False, nullable=True)
    balance = Column(Float)

    created_on = Column(DateTime(), default=datetime.now)
    updated_on = Column(DateTime(), default=datetime.now, onupdate=datetime.now)


class Transaction(PrimaryIdModel):
    __tablename__ = 'transactions'

    user_to = Column(BigInteger, ForeignKey('users.user_id'))
    user_from = Column(BigInteger, ForeignKey('users.user_id'))
    amount = Column(Float)



