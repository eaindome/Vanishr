from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String)
    email = Column(String, unique=True)
    phone = Column(String, nullable=True)
    address = Column(String, nullable=True)

    requests = relationship("RequestLog", back_populates="user")

class Broker(Base):
    __tablename__ = "brokers"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    opt_out_method = Column(String)  # form, email, letter
    url = Column(String)
    notes = Column(String, nullable=True)

    requests = relationship("RequestLog", back_populates="broker")

class RequestLog(Base):
    __tablename__ = "requests"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    broker_id = Column(Integer, ForeignKey("brokers.id"))
    status = Column(String, default="Pending")  # Pending, Completed, Failed
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)

    user = relationship("User", back_populates="requests")
    broker = relationship("Broker", back_populates="requests")
