from fastapi import APIRouter, HTTPException
import logging
from database.db_connection import db
from database.mission_db import MissionDB
from routes.agents_routes import agents, get_agent_by_id
from models import Mission


missions = MissionDB(db, "missions")

router = APIRouter(prefix="/missions", tags=["missions"])

logger = logging.getLogger(__name__)


@router.post("", status_code=201)
def create_mission(data: Mission):
    logger.info("POST /missions called")

    if not 1 <= data.difficulty <= 10:
        logger.error("difficulty between 1 and 10")
        raise HTTPException(400, "difficulty between 1 and 10")
    
    if not 1 <= data.importance <= 10:
        logger.error("importance between 1 and 10")
        raise HTTPException(400, "importance between 1 and 10")
    
    logger.info("creating mission")
    missions.create_mission(data.model_dump())
    logger.info("mission Created")
    return {"message": "Mission Created"}


@router.get("")
def get_all_missions():
    logger.info("GET /missions called")
    logger.info("returns all missions")
    return missions.get_all_missions()


@router.get("/{id}")
def get_mission_by_id(id: int):
    logger.info(f"Looking for agent {id}")
    mission = missions.get_mission_by_id(id)

    if not mission:
        logger.error("mission not exists")
        raise HTTPException(404, "mission not exists")
    
    logger.info(f"returns mission {id}")
    return mission


@router.put("/{id}/assign/{agent_id}")
def assign_mission(id: int, agent_id: int):
    logger.info(f"PUT /missions/{id}/assign/{agent_id} called")

    mission = get_mission_by_id(id)
    agent = get_agent_by_id(agent_id)

    if mission["status"] != "NEW":
        logger.error("not NEW mission")
        raise HTTPException(400, "not NEW mission")
    
    if not agent["is_active"]:
        logger.error("non nactive agent")
        raise HTTPException(400, "non nactive agent")
    
    if len(missions.get_open_missions_by_agent(agent_id)) >= 3:
        logger.error("3 missions are already open")
        raise HTTPException(400, "3 missions are already open")
    
    if mission["risk_level"] == "CRITICAL" and agent["agent_rank"] != "Commander":
        logger.error("only Commander can take CRITICAL")
        raise HTTPException(400, "only Commander can take CRITICAL")
    
    logger.info("Updating")
    is_updated = missions.assign_mission(id, agent_id)
    if is_updated:
        logger.info("Updated successfully")
        return {"message": "Updated successfully"}


@router.put("/{id}/start")
def start_mission(id: int):
    logger.info(f"PUT /missions/{id}/start called")
    mission = get_mission_by_id(id)

    if mission["status"] != "ASSIGNED":
            logger.error("only ASSIGNED can be IN_PROGRESS")
            raise HTTPException(400, "only ASSIGNED can be IN_PROGRESS")
    logger.info("Updating")
    is_updated = missions.update_mission_status(id, "IN_PROGRESS")
    if is_updated:
        logger.info("Updated successfully")
        return {"message": "Updated successfully"}
    

@router.put("/{id}/complete")
def complete_mission(id: int):
    logger.info(f"PUT /missions/{id}/complete called")
    mission = get_mission_by_id(id)

    if mission["status"] != "IN_PROGRESS":
            logger.error("can COMPLETED only IN_PROGRESS")
            raise HTTPException(400, "can COMPLETED only IN_PROGRESS")
    
    logger.info("Updating")
    is_updated = missions.update_mission_status(id, "COMPLETED")
    if is_updated:
        agents.increment_completed(mission["assigned_agent_id"])
        logger.info("Updated successfully")
        return {"message": "Updated successfully"}
    

@router.put("/{id}/fail")
def fail_mission(id: int):
    logger.info(f"PUT /missions/{id}/fail called")
    mission = get_mission_by_id(id)

    if mission["status"] != "IN_PROGRESS":
            logger.error("can FAILED only IN_PROGRESS")
            raise HTTPException(400, "can FAILED only IN_PROGRESS")
    
    logger.info("Updating")
    is_updated = missions.update_mission_status(id, "FAILED")
    if is_updated:
        agents.increment_failed(mission["assigned_agent_id"])
        logger.info("Updated successfully")
        return {"message": "Updated successfully"}


@router.put("/{id}/cancel")
def cancel_mission(id: int):
    logger.info(f"PUT /missions/{id}/cancel called")

    mission = get_mission_by_id(id)

    if mission["status"] not in ["NEW", "ASSIGNED"]:
        logger.error("can not be CANCELLED")
        raise HTTPException(400, "can not be CANCELLED")
    
    logger.info("Updating")
    is_updated = missions.update_mission_status(id, "CANCELLED")
    if is_updated:
        logger.info("Updated successfully")
        return {"message": "Updated successfully"}
    
    
    



     







