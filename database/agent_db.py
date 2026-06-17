from db_connection import DB_connection, db
from base_db import BaseDB


class AgentDB(BaseDB):
    def __init__(self, db: DB_connection, table):
        super().__init__(db, table)

    def create_agent(self, data: dict):
        if data["agent_rank"] not in ["Junior", "Senior", "Commander"]:
            raise ValueError("rank must be Junior / Senior / Commander")
        return super().create(data)
    
    def get_all_agents(self):
        return super().get_all()
    
    def get_agent_by_id(self, id):
        return super().get_by_id(id)
    
    def update_agent(self, id, data):
        return super().update(data, {"id": id})
    
    def deactivate_agent(self, id):
        return super().update({"is_active": False}, {"id": id})
    
    def increment_completed(self, id):
        agent = self.get_agent_by_id(id)
        current = agent["completed_missions"]
        return super().update({"completed_missions": current + 1}, {"id": id})
    
    def get_agent_performance(self, id):
        agent = self.get_agent_by_id(id)
        completed = agent["completed_missions"]
        failed = agent["failed_missions"]
        return {
            "completed": completed,
            "failed": failed,
            "total": completed + failed,
            "success_rate": (completed // (completed + failed)) * 100
            }
    
    def count_active_agents(self):
        return super().count({"is_active": True})["total"]
    
    
    
    

    


agents = AgentDB(db, "agents")
# print(agents.create({"name": "yossi", "specialty": "aa", "agent_rank": "junior"}))
print(agents.get_all())
# print(agents.get_by_id(1))
# agents.update_agent(1, {"is_active": True})
# agents.increment_completed(1)
# print(agents.get_agent_performance(1))
# print(agents.get_all())
# # print(agents.count())
# print(agents.count_active_agents())
# agents.deactivate_agent(1)
# print(agents.count_active_agents())



