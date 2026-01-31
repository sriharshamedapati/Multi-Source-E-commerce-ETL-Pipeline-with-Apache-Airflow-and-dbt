from fastapi import FastAPI, Query
from typing import List

app = FastAPI()

# Sample data
orders_db = [
    {"order_id": i, "user_id": (i%10)+1, "product_id": (i%5)+1, "order_date": "2025-01-30", "amount": 100.0 + i}
    for i in range(1, 26) # 25 orders
]

@app.get("/health")
def health(): return {"status": "healthy"}

@app.get("/orders")
def get_orders(page: int = Query(1, gt=0)):
    limit = 10
    start = (page - 1) * limit
    end = start + limit
    return orders_db[start:end] # Returns [] if out of bounds