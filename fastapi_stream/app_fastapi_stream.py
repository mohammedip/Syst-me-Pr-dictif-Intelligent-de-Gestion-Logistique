from fastapi import FastAPI, WebSocket
import random
import json
import asyncio
from faker import Faker

fake = Faker()
app = FastAPI()

def generate_fake_dataco():
    return {
        "Type": random.choice(["DEBIT", "CASH", "TRANSFER"]),
        "ProductCategoryId": random.randint(1, 100),
        "OrderItemQuantity": random.randint(1, 5),
        "CustomerCountry": fake.country(),
        "CustomerCity": fake.city(),
        "OrderCountry": fake.country(),
        "OrderCity": fake.city(),
        "ShippingMode": random.choice(["Standard Class", "Second Class", "First Class"]),
        "order_month": random.randint(1, 12)
    }


@app.websocket("/ws/data")
async def websocket_data(ws: WebSocket):
    await ws.accept()
    while True:
        record = generate_fake_dataco()
        await ws.send_text(json.dumps(record))
        await asyncio.sleep(1)
