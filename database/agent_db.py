from db_connection import DB_connection, db
from base_db import BaseDB

class AgentDB(BaseDB):
    def __init__(self, db: DB_connection, table):
        super().__init__(db, table)

    def create_agent(self, data):
        return super().create(data)
    
    def get_all_agents(self):
        return super().get_all()
    
    def get_agent_by_id(self, id):
        return super().get_by_id(id)
    





agents = AgentDB(db, "agents")
# print(agents.create({"name": "yossi", "specialty": "aa", "agent_rank": "junior"}))
# print(agents.get_all())
# print(agents.get_by_id(1))