from kafka import KafkaProducer
import json
import time
import random
import uuid
from datetime import datetime

producer = KafkaProducer(
    bootstrap_servers='localhost:9092',  
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

products = [
    {"product_id": "P001", "product_name": "Laptop", "price": 1000},
    {"product_id": "P002", "product_name": "Phone", "price": 600},
    {"product_id": "P003", "product_name": "Headphones", "price": 150},
    {"product_id": "P004", "product_name": "Shoes", "price": 120}
]

regions = ["North", "South", "East", "West"]
statuses = ["placed", "shipped", "cancelled"]

while True:
    order = {
        "order_id": str(uuid.uuid4()),
        "customer_id": "C" + str(random.randint(100, 999)),
        "product_id": random.choice(products)["product_id"],
        "product_name": random.choice(products)["product_name"],
        "price": random.choice(products)["price"],
        "quantity": random.randint(1, 5),
        "region": random.choice(regions),
        "status": random.choice(statuses),
        "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }

    producer.send("ecommerce_orders", order)
    print("✅ Sent order:", order["order_id"])
    time.sleep(2)
