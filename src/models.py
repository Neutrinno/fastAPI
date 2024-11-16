from sqlalchemy import Column, Integer, String, Numeric, func, Date
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True)
    date = Column(Date, server_default=func.current_date(), nullable=False)
    amount = Column(Numeric, nullable=False)
    category = Column(String, nullable=False)
    description = Column(String, nullable=True)

