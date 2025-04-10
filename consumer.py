import json
from kafka import KafkaConsumer
import psycopg2

# Connect to AWS RDS PostgreSQL
conn = psycopg2.connect(
    host="ecommerce-db.cf0ku0i007rf.us-east-2.rds.amazonaws.com",
    port=5432,
    dbname="postgres",  # change if your DB name is different
    user="admin123",       # your RDS username
    password="Admin123456admin"  # your RDS password
)
cur = conn.cursor()


# Connect to Kafka and subscribe to topic
consumer = KafkaConsumer(
    'ecommerce_orders',
    bootstrap_servers='localhost:9092',
    auto_offset_reset='latest',        # only get new messages
    value_deserializer=lambda m: json.loads(m.decode('utf-8'))
)

print("📦 Listening for new orders...\n")

# Process each incoming message
for message in consumer:
    order = message.value
    print(f"✅ Saving order: {order['order_id']}")

    try:
        cur.execute("""
            INSERT INTO orders (
                order_id, customer_id, product_id, product_name, price,
                quantity, region, status, timestamp
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (order_id) DO NOTHING;
        """, (
            order['order_id'],
            order['customer_id'],
            order['product_id'],
            order['product_name'],
            order['price'],
            order['quantity'],
            order['region'],
            order['status'],
            order['timestamp']
        ))

        conn.commit()

    except Exception as e:
        print("❌ Error inserting order:", e)

# Close everything (in real projects, use try/finally or context managers)
cur.close()
conn.close()