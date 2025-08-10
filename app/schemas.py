from typing import List, Optional
from pydantic import BaseModel


class PropertyBase(BaseModel):
    address: str
    price: float
    sold: bool = False


class PropertyCreate(PropertyBase):
    pass


class Property(PropertyBase):
    id: int
    client_id: Optional[int]

    class Config:
        orm_mode = True


class ClientBase(BaseModel):
    name: str
    email: str
    phone: Optional[str] = None


class ClientCreate(ClientBase):
    pass


class Client(ClientBase):
    id: int
    properties: List[Property] = []

    class Config:
        orm_mode = True
