from fastapi import APIRouter, HTTPException
from database.db_connection import db
from database.agent_db import AgentDB
from models import Agent

agents = AgentDB(db, "agents")

router = APIRouter(prefix="/agents", tags=["agents"])

@router.post("", status_code=201)
def create_agent(data: Agent):
    if data.agent_rank not in ["Junior", "Senior", "Commander"]:
            raise HTTPException(400, "rank must be Junior / Senior / Commander")
    agents.create_agent(data.model_dump())
    return {"message": "Agent Created"}

@router.get("")
def get_all_agents():
      return agents.get_all_agents()

@router.get("/{id}")
def get_agent_by_id(id: int):
    agent = agents.get_agent_by_id(id)
    if not agent:
        raise HTTPException(404, "id not exists")
    return agent

@router.put("/{id}")
def update_agent(id: int, data: Agent):
    agent = agents.get_agent_by_id(id)
    if not agent:
        raise HTTPException(404, "id not exists")
    is_updated = agents.update_agent(id, data.model_dump())
    if is_updated:
        return 





