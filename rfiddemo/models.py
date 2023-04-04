from typing import Optional, List
from enum import unique
from datetime import datetime
from sqlmodel import SQLModel, Field,Column,DateTime, Relationship
from pydantic import EmailStr

class Transaction(SQLModel,table=True):

    id:Optional[int]= Field( primary_key=True, nullable=False)
    amount:int = Field( nullable=False, unique=False)
    recharge_request:bool = Field(nullable=False)
    user_id:Optional[int] = Field( foreign_key="user.id", nullable=False)
    merchant_id:Optional[int] = Field( foreign_key= "merchant.id", nullable=False)
    created_at:datetime =Field(default_factory=datetime.utcnow, nullable=False)

    user: Optional["User"] = Relationship(back_populates="transactions")

class Merchant(SQLModel,table=True):
    id :Optional[int] = Field( primary_key=True, nullable=False)
    name:str = Field( nullable=False, unique=False)
    email:EmailStr  = Field( nullable=False, unique=True)
    password:str = Field( nullable=False)
    amount:int = Field(nullable=False,unique= False)
    created_at:datetime = Field(default_factory=datetime.utcnow, nullable=False)

    users: List["User"] = Relationship(back_populates="merchants", link_model=Transaction)
    # user: Optional["User"] = Relationship(back_populates="merchants")

class User(SQLModel,table=True):

    id:Optional[int]= Field( primary_key=True, nullable=False)
    name:str = Field( nullable=False, unique=False)
    tag_data:str = Field( nullable=False, unique=True)  
    amount:int = Field( nullable=False, unique=False)
    created_at:datetime = Field(default_factory=datetime.utcnow, nullable=False)
    
    transactions:List["Transaction"] = Relationship(back_populates="user")

    merchants: List["Merchant"] = Relationship(back_populates="users", link_model=Transaction)


    
# SQLALCHEMY_DATABASE_URL = "postgresql://postgres:yankee005@localhost/RFID2"

# engine = create_engine(SQLALCHEMY_DATABASE_URL)

# def create_db_and_tables():
#     SQLModel.metadata.create_all(engine)

# if __name__ == "__main__":
#     create_db_and_tables()

    