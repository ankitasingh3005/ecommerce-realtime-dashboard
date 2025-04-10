import psycopg2

try:
    conn = psycopg2.connect(
        host="ecommerce-db.cf0ku0i007rf.us-east-2.rds.amazonaws.com",
        database="postgres",
        user="admin123",
        password="Admin123456admin",
        port="5432"
    )
    print("✅ Connected successfully!")
    conn.close()
except Exception as e:
    print("❌ Connection failed:", e)
