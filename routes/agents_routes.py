from fastapi import APIRouter, HTTPException
import logging
from database.db_connection import db
from database.agent_db import AgentDB
from models import Agent

agents = AgentDB(db, "agents")

router = APIRouter(prefix="/agents", tags=["agents"])

logger = logging.getLogger(__name__)


@router.post("", status_code=201)
def create_agent(data: Agent):
    logger.info("POST /agents called")

    if data.agent_rank not in ["Junior", "Senior", "Commander"]:
            logger.error("Incorrect rank")
            raise HTTPException(400, "rank must be Junior / Senior / Commander")
    
    logger.info("creating agent")
    new_id = agents.create_agent(data.model_dump())

    logger.info(f"Agent {new_id} Created")
    return {"message": f"Agent {new_id} Created"}

@router.get("")
def get_all_agents():
    logger.info("GET /agents called")
    logger.info("returns all agents")
    return agents.get_all_agents()

@router.get("/{id}")
def get_agent_by_id(id: int):
    logger.info(f"Looking for agent {id}")
    agent = agents.get_agent_by_id(id)
    
    if not agent:
        logger.error(f"id {id} not exists")
        raise HTTPException(404, f"id {id} not exists")
    
    logger.info(f"returns agent {id}")
    return agent

@router.put("/{id}")
def update_agent(id: int, data: Agent):
    logger.info(f"PUT /agents/{id} called")

    if data.agent_rank not in ["Junior", "Senior", "Commander"]:
            logger.error("Incorrect rank")
            raise HTTPException(400, "rank must be Junior / Senior / Commander")

    get_agent_by_id(id)
    logger.info("Updating agent")
    is_updated = agents.update_agent(id, data.model_dump())

    if is_updated:
        logger.info("Updated successfully")
        return {"message": "Updated successfully"}
    
@router.put("/{id}/deactivate")
def deactivate_agent(id: int):
    logger.info(f"PUT /agents/{id}/deactivate called")
    
    get_agent_by_id(id)
    logger.info("Updating agent")
    is_updated = agents.deactivate_agent(id)
    if is_updated:
        logger.info("Updated successfully")
        return {"message": "Updated successfully"}
    
@router.get("/{id}/performance")
def get_agent_performance(id: int):
    logger.info(f"GET /agents/{id}/performance called")

    get_agent_by_id(id)
    logger.info("returns performance")
    return agents.get_agent_performance(id)







