from fastapi import FastAPI
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, Float, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from typing import List
from contextlib import contextmanager

app = FastAPI()
Base = declarative_base()

class Item(Base):
    __tablename__ = "new_items"
    id = Column(Integer, primary_key=True, index=True)
    description = Column(String, index=True)
    sellingprice = Column(Float)

database_url = "mssql+pyodbc://DBUser:CStore@db123@3.87.50.246/CStoreiQDB_dev?driver=ODBC+Driver+17+for+SQL+Server"
engine = create_engine(database_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class ItemModel(BaseModel):
    id: int
    description: str
    sellingprice: float

def to_pydantic(item):
    return ItemModel(id=item.id, description=item.description, sellingprice=item.sellingprice)

@contextmanager
def session_scope():
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()

@app.get('/get/items', response_model=List[ItemModel])
def get_item():
    with session_scope() as db:
        items = db.query(Item).all()
        if items is None:
            return []
        return [to_pydantic(item) for item in items]