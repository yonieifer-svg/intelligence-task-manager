from database.db_connection import DB_connection, db
from database.base_db import BaseDB


class AgentDB(BaseDB):
    def __init__(self, db: DB_connection, table):
        super().__init__(db, table)

    def create_agent(self, data: dict):
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
        total = completed + failed
        if total == 0:
            return {"message": "no missions done"}
        return {
            "completed": completed,
            "failed": failed,
            "total": total,
            "success_rate": (completed // (completed + failed)) * 100
            }
    
    def count_active_agents(self):
        return super().count({"is_active": True})["total"]
    
    
    
    

    






