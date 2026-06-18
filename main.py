from fastapi import FastAPI
import logging
from database.db_connection import db
from routes.agents_routes import router as agents_router
from routes.mission_routes import router as missions_router

logging.basicConfig(level=logging.INFO,
                    format = "%(asctime)s | %(levelname)s | %(message)s",
                    filename="logs/app.log")

app = FastAPI()

db.create_database()
db.create_tables()

app.include_router(agents_router)
app.include_router(missions_router)