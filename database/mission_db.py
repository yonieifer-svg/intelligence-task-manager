from db_connection import DB_connection, db
from agent_db import agents
from base_db import BaseDB


class MissionDB(BaseDB):
    def __init__(self, db: DB_connection, table):
        super().__init__(db, table)

    def create_mission(self, data: dict):

        risk_level = (data["difficulty"] * 2) + data["importance"]

        if 0 <= risk_level <= 9:
            data["risk_level"] = "LOW"

        elif 10 <= risk_level <= 17:
            data["risk_level"] = "MEDIUM"

        elif 18 <= risk_level <= 24:
            data["risk_level"] = "HIGH"

        elif 25 <= risk_level:
            data["risk_level"] = "CRITICAL"

        return super().create(data)
    
    def get_all_missions(self):
        return super().get_all()
    
    def get_mission_by_id(self, id):
        return super().get_by_id(id)
    
    def assign_mission(self, mission_id, agent_id):
        agent = agents.get_agent_by_id(agent_id)
        mission = self.get_mission_by_id(mission_id)
        if not agent["is_active"]:
            raise ValueError("non nactive agent")
        
        if len(self.get_open_missions_by_agent(agent_id)) >= 3:
            raise ValueError("3 missions are already open")
        
        if mission["risk_level"] == "CRITICAL" and agent["agent_rank"] != "Commander":
            raise ValueError("only Commander can take CRITICAL")

        if mission["status"] != "NEW":
            raise ValueError("not NEW mission")

        return super().update({"assigned_agent_id": agent_id, "status": "ASSIGNED"}, {"id": mission_id})
    
    def update_mission_status(self, id, status):

        mission = self.get_mission_by_id(id)

        if status == "IN_PROGRESS" and mission["status"] != "ASSIGNED":
            raise ValueError("only ASSIGNED can be IN_PROGRESS")
        
        if (status == "FAILED" or status == "COMPLETED") and mission["status"] != "IN_PROGRESS ":
            raise ValueError("can ens only IN_PROGRESS ")

        if status == "CANCELLED" and mission["status"] not in ["NEW", "ASSIGNED"] :
            raise ValueError("can not be CANCELLED")

        return super().update({"status": status}, {"id": id})
    
    def get_open_missions_by_agent(self, id):
        in_progress = super().get_all({"status": "IN_PROGRESS", "assigned_agent_id": id})
        assigned = super().get_all({"status": "ASSIGNED", "assigned_agent_id": id})
        return in_progress + assigned
    
    def count_all_missions(self):
        return super().count()["total"]
    
    def count_by_status(self, status):
        return super().count({"status": status})["total"]
    
    def count_open_missions(self):
        new = super().count({"status": "NEW"})["total"]
        assigned = super().count({"status": "ASSIGNED"})["total"]
        in_progress = super().count({"status": "IN_PROGRESS"})["total"]
        return new + assigned + in_progress
    
    def count_critical_missions(self):
        return super().count({"status": "CRITICAL"})["total"]
    
    def get_top_agent(self):
        all_agents = agents.get_all_agents()
        top_agent = max(all_agents, key=lambda x: x["completed_missions"])
        return top_agent








# mis = MissionDB(db, "missions")

# print(mis.create_mission({"title": "imp", "description": "wow", "location": "here", "difficulty": 5, "importance": 7, }))
# print(mis.get_all_missions())
# mis.assign_mission(1, 1)
# print(mis.get_mission_by_id(1))
# print(mis.get_all_missions())
# print(mis.get_open_missions_by_agent(1))

# print(mis.count_all_missions())
# print(mis.count_by_status("ASSIGNED"))
# print(mis.count_open_missions())


