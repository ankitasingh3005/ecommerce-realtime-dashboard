# 📊 E-commerce Real-Time Analytics Dashboard

Welcome to the **E-commerce Real-Time Dashboard** project!  
This project simulates a live order processing system for an e-commerce platform using **Kafka** and **PostgreSQL**, and visualizes insights through a fully interactive **Streamlit** dashboard.

---

## 🚀 About the Project

This end-to-end pipeline replicates a simplified e-commerce system where:

- **Kafka** handles real-time order streaming  
- **PostgreSQL (AWS RDS)** stores all order data  
- **Streamlit** displays metrics, trends, and insights using professional visuals  
- **Docker** orchestrates Kafka and Zookeeper containers  

It’s built for **hands-on learning** and **portfolio-ready demonstration** of modern data engineering + analytics skills.

---

## 🧱 Tech Stack

- **Backend / Streaming**: Apache Kafka, Python  
- **Database**: PostgreSQL (hosted on AWS RDS)  
- **Dashboard**: Streamlit  
- **Containerization**: Docker & Docker Compose  
- **Data Processing**: pandas, psycopg2, seaborn, matplotlib  

---

## 📂 Project Structure

```bash
ecommerce_realtime_pipeline/
│
├── app.py                  # Streamlit dashboard
├── producer.py             # Kafka producer (sends order data)
├── consumer.py             # Kafka consumer (stores data into PostgreSQL)
├── create_table.py         # Creates 'orders' table in DB
├── test_db.py              # Verifies DB connectivity
├── docker-compose.yml      # Runs Kafka & Zookeeper containers
├── filtered_orders.csv     # Exported dashboard data (for testing/demo)
└── README.md               # Project overview
