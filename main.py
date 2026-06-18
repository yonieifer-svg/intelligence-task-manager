from fastapi import FastAPI
import logging
from database.db_connection import db
from routes.agents_routes import router as agents_router

# logging.basicConfig(level=logging.INFO,
#                     format = pass,
#                     handlers=pass)

app = FastAPI()

db.create_database()
db.create_tables()

app.include_router(agents_router)