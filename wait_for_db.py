from psycopg2 import OperationalError

import os
import psycopg2
import time

host = os.environ.get("POSTGRES_HOST", "db")
port = os.environ.get("POSTGRES_PORT", 5432)

while True:
    try:
        conn = psycopg2.connect(
            dbname=os.environ.get("POSTGRES_DB"),
            user=os.environ.get("POSTGRES_USER"),
            password=os.environ.get("POSTGRES_PASSWORD"),
            host=host,
            port=port,
        )
        conn.close()
        break
    except OperationalError:
        print("Waiting for database...")
        time.sleep(0.5)
