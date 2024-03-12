from fastapi import FastAPI, HTTPException
from typing import List
from pydantic import BaseModel
import pyodbc


app = FastAPI()

# Establish a connection to the database
conn = pyodbc.connect(driver='{ODBC Driver 17 for SQL Server}',
                      server='server_num',
                      database='database_name',
                      uid='user_name', pwd='password')
cursor = conn.cursor()
# Define a model for the item
class Item(BaseModel):
    id: int
    description: str
    SellingPrice: float

# GET all items
@app.get('/items/', response_model=List[Item])
def read_items():
    try:
       # cursor = conn.cursor()
        cursor.execute('SELECT id, description, SellingPrice FROM Table_items')
        items = []
        for row in cursor.fetchall():
            items.append({'id': row.id, 'description': row.description, 'SellingPrice': row.SellingPrice})
        return items
    except pyodbc.Error as e:
        raise HTTPException(status_code=500, detail=str(e))

# GET by ID
@app.get('/items/{item_id}', response_model=Item)
def read_item(item_id: int):
    try:
        #cursor = conn.cursor()
        cursor.execute('SELECT id, description, SellingPrice FROM Table_items WHERE id = ?', (item_id,))
        row = cursor.fetchone()
        if row:
            return row
        else:
            raise HTTPException(status_code=404, detail="Item not found")
    except pyodbc.Error as e:
        raise HTTPException(status_code=500, detail=str(e)) 

# POST
@app.post('/items/', response_model=Item)
def create_item(item: Item):
    try:
        #cursor = conn.cursor()
        cursor.execute('INSERT INTO Table_items (id, description, SellingPrice) VALUES (?, ?, ?)',
                       (item.id, item.description, item.SellingPrice))
        conn.commit()
        return item
    except pyodbc.Error as e:
        raise HTTPException(status_code=500, detail=str(e))

# PUT
@app.put('/items/{item_id}', response_model=Item)
def update_item(item_id: int, item: Item):
    try:
        #cursor = conn.cursor()
        cursor.execute('UPDATE Table_items SET description = ?, SellingPrice = ? WHERE id = ?',
                       (item.description, item.SellingPrice, item_id))
        conn.commit()
        return item
    except pyodbc.Error as e:
        raise HTTPException(status_code=500, detail=str(e))

# DELETE
@app.delete('/items/{item_id}')
def delete_item(item_id: int):
    try:
        #cursor = conn.cursor()
        cursor.execute('DELETE FROM Table_items WHERE id = ?', (item_id,))
        conn.commit()
        return {'message': 'Item deleted successfully'}
    except pyodbc.Error as e:
        raise HTTPException(status_code=500, detail=str(e))