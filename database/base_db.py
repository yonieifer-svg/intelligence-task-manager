from db_connection import DB_connection, db

class BaseDB:
    def __init__(self, db: DB_connection, table):
        self.db = db
        self.table = table

    def create(self, data: dict):
        columns = ", ".join(key for key in data.keys())
        holders = ", ".join(["%s"] * len(data))
        values = list(data.values())
        
        query = f"INSERT INTO {self.table} ({columns}) VALUES ({holders})"

        with self.db.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, values)
                conn.commit()
                id = cursor.lastrowid
                item = self.get_by_id(id)
                return item
    
    def get_all(self):
        with self.db.get_connection() as conn:
            with conn.cursor(dictionary=True) as cursor:
                cursor.execute(f"SELECT * FROM {self.table}")
                result = cursor.fetchall()
                return result
            
    def get_by_id(self, id):
        with self.db.get_connection() as conn:
            with conn.cursor(dictionary=True) as cursor:
                cursor.execute(f"SELECT * FROM {self.table} WHERE id = %s", [id])
                result = cursor.fetchone()
                return result
            
    def update(data: dict):


        query = "UPDATE customers SET address = 'Canyon 123' WHERE address = 'Valley 345'"

            



