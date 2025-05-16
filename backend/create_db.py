import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

# Database connection parameters
host = "10.10.1.209"
user = "postgres"
password = "Hagbes@1234"
port = "5432"

# Connect to PostgreSQL server
conn = psycopg2.connect(
    host=host,
    user=user,
    password=password,
    port=port
)

conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
cursor = conn.cursor()

# Create database
try:
    cursor.execute("CREATE DATABASE taskmanagement")
    print("Database created successfully!")
except psycopg2.Error as e:
    print(f"Error creating database: {e}")
finally:
    cursor.close()
    conn.close() 