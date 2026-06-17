import mysql.connector

class DB_connection:
    def __init__(self):
        pass

    def get_connection(self):
        return mysql.connector.connect(
            host="localhost",
            port=3306,
            user="root",
            password="root",
            database="Intelligence_db"
            )

    def create_database(self):
        conn = mysql.connector.connect(
            host="localhost",
            port=3306,
            user="root",
            password="root"
            )
        with conn.cursor() as cursor:
            cursor.execute("CREATE DATABASE IF NOT EXISTS Intelligence_db")
        conn.close()

    def create_tables(self):
        with self.get_connection() as conn:
            with conn.cursor() as cursor:
                # cursor.execute("DROP TABLE agents")
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS agents (
                    id INT PRIMARY KEY AUTO_INCREMENT,
                    name VARCHAR(50),
                    specialty VARCHAR(50),
                    is_active BOOL DEFAULT TRUE,
                    completed_missions INT DEFAULT 0,
                    failed_missions INT DEFAULT 0,
                    agent_rank VARCHAR(50)
                    )
                    """)
                # cursor.execute("DROP TABLE missions")
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS missions (
                    id INT PRIMARY KEY AUTO_INCREMENT,
                    title VARCHAR(50),
                    description TEXT,
                    location VARCHAR(50),
                    difficulty INT,
                    importance INT,
                    status VARCHAR(50) DEFAULT 'NEW',
                    risk_level VARCHAR(50),
                    assigned_agent_id INT DEFAULT NULL
                    )
                """)

db = DB_connection()


db.create_database()


db.create_tables()

