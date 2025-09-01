from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    full_name: str
    email: str
    phone: Optional[str]
    address: Optional[str]

class UserCreate(UserBase):
    pass

class User(UserBase):
    id: int
    class Config:
        orm_mode = True

class BrokerBase(BaseModel):
    name: str
    opt_out_method: str
    url: str
    notes: Optional[str]

class BrokerCreate(BrokerBase):
    pass

class Broker(BrokerBase):
    id: int
    class Config:
        orm_mode = True

class RequestLogBase(BaseModel):
    user_id: int
    broker_id: int

class RequestLog(RequestLogBase):
    id: int
    status: str
    created_at: datetime
    completed_at: Optional[datetime]
    class Config:
        orm_mode = True
