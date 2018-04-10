#!/usr/bin/env python

from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import Numeric
from sqlalchemy import String
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Todo(Base):
    __tablename__ = 'todos'

    id = Column(Integer, primary_key=True)
    task = Column(String(255))
    

class Account(Base):
    __tablename__ = 'account'

    account_id = Column(Integer, primary_key=True)
    account_name = Column(String(255))
    account_type = Column(String(255))
    account_status = Column(String(255))
    account_balance = Column(Integer)
    create_timestamp = Column(DateTime)
    
class Transaction(Base):
    __tablename__ = 'transaction'

    transaction_id = Column(Integer, primary_key=True)
    instrument_name = Column(String(255))
    transaction_type = Column(String(255))
    transaction_dt = Column(DateTime)
    net_transaction_amt = Column(Numeric)
    transaction_qty = Column(Numeric)
    account_id = Column(Integer, ForeignKey("account.account_id"))

class ServiceNow(Base):
    __tablename__ = 'service_now'

    ticket_id = Column(Integer, primary_key=True)
    ticket_category = Column(String(255))
    ticket_status = Column(String(255))
    ticket_description = Column(String(255))
    ticket_comment = Column(String(255))
    create_date = Column(DateTime)
    priotity = Column(String(25))
    assigned_to = Column(String(255))
    assignment_group = Column(String(255))
    requestor = Column(String(255))

if __name__ == "__main__":
    from sqlalchemy import create_engine
    from settings import DB_URI
    engine = create_engine(DB_URI)
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
