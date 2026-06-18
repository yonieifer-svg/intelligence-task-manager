from database.db_connection import DB_connection, db

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
    
    def get_all(self, filter: dict=None):
        sql_filter = ""
        filter_values = []

        if filter:
            sql_filter = f" WHERE {' AND '.join(key + " = %s" for key in filter.keys())}"
            filter_values = list(filter.values())

        query = f"SELECT * FROM {self.table}" + sql_filter

        with self.db.get_connection() as conn:
            with conn.cursor(dictionary=True) as cursor:
                cursor.execute(query, filter_values)
                result = cursor.fetchall()
                return result
            
    def get_by_id(self, id):
        with self.db.get_connection() as conn:
            with conn.cursor(dictionary=True) as cursor:
                cursor.execute(f"SELECT * FROM {self.table} WHERE id = %s", [id])
                result = cursor.fetchone()
                return result
            
    def update(self, data: dict, filter:dict=None):
        set_items = ", ".join(key + " = %s" for key in data.keys())
        values = list(data.values())
        sql_filter = ""
        filter_values = []

        if filter:
            sql_filter = f" WHERE {' AND '.join(key + " = %s" for key in filter.keys())}"
            filter_values = list(filter.values())

        query = f"UPDATE {self.table} SET {set_items}" + sql_filter
        
        with self.db.get_connection() as conn:
            with conn.cursor(dictionary=True) as cursor:
                cursor.execute(query, values + filter_values)
                conn.commit()
                return cursor.rowcount > 0
            
    def count(self, filter: dict=None):
        sql_filter = ""
        filter_values = []

        if filter:
            sql_filter = f" WHERE {' AND '.join(key + " = %s" for key in filter.keys())}"
            filter_values = list(filter.values())

        query = f"SELECT COUNT(*) AS total FROM {self.table}" + sql_filter
        with self.db.get_connection() as conn:
            with conn.cursor(dictionary=True) as cursor:
                cursor.execute(query, filter_values)
                result = cursor.fetchone()
                return result






# bdb = BaseDB(db, "agent")
# bdb.update({"is_available": True}, {"id": 1})

            



