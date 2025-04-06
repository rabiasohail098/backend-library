import psycopg2
from psycopg2 import pool, OperationalError
import os
from dotenv import load_dotenv
import time
from typing import Optional

load_dotenv()

class Database:
    _connection_pool = None

    @classmethod
    def initialize(cls):
        """Initialize the connection pool"""
        max_retries = 3
        retry_delay = 2  # seconds
        
        for attempt in range(max_retries):
            try:
                cls._connection_pool = psycopg2.pool.ThreadedConnectionPool(
                    minconn=1,
                    maxconn=10,
                    dbname=os.getenv("DB_NAME"),
                    user=os.getenv("DB_USER"),
                    password=os.getenv("DB_PASSWORD"),
                    host=os.getenv("DB_HOST"),
                    port=os.getenv("DB_PORT")
                )
                print("✅ Database connection pool created")
                break
            except OperationalError as e:
                print(f"⚠️ Connection attempt {attempt + 1} failed: {e}")
                if attempt == max_retries - 1:
                    raise
                time.sleep(retry_delay)

    @classmethod
    def get_connection(cls):
        """Get a connection from the pool"""
        if cls._connection_pool is None:
            cls.initialize()
        
        try:
            return cls._connection_pool.getconn()
        except OperationalError as e:
            print(f"⚠️ Failed to get connection: {e}")
            raise

    @classmethod
    def return_connection(cls, connection):
        """Return a connection to the pool"""
        if cls._connection_pool is not None:
            cls._connection_pool.putconn(connection)

    @classmethod
    def close_all_connections(cls):
        """Close all connections in the pool"""
        if cls._connection_pool is not None:
            cls._connection_pool.closeall()
            print("🔌 All database connections closed")

# Initialize the pool when module is imported
try:
    Database.initialize()
except Exception as e:
    print(f"❌ Failed to initialize database: {e}")