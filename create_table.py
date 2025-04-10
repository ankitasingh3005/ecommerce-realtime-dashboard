import psycopg2

# Connect to your RDS PostgreSQL
conn = psycopg2.connect(
    host="ecommerce-db.cf0ku0i007rf.us-east-2.rds.amazonaws.com",
    port=5432,
    dbname="postgres",        # default DB name unless you changed it
    user="admin123",             # replace with your username
    password="Admin123456admin"  # replace with your password
)

cur = conn.cursor()

# Create table to store orders
cur.execute("""
    CREATE TABLE IF NOT EXISTS orders (
        order_id TEXT PRIMARY KEY,
        customer_id TEXT,
        product_id TEXT,
        product_name TEXT,
        price NUMERIC,
        quantity INTEGER,
        region TEXT,
        status TEXT,
        timestamp TEXT
    );
""")

conn.commit()
cur.close()
conn.close()

print("✅ Table created successfully!")
