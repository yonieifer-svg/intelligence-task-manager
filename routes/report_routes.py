from fastapi import APIRouter, HTTPException
import logging
from routes.agents_routes import agents
from routes.mission_routes import missions


router = APIRouter(prefix="/reports", tags=["reports"])

logger = logging.getLogger(__name__)

@router.get("/summary")
def get_summary():
    return {
        "active_agents_count": agents.count_active_agents(),
        "total_missions": missions.count_all_missions(),
        "open_missions": missions.count_open_missions(),
        "completed_missions": missions.count_by_status("COMPLETE"),
        "failed_missions": missions.count_by_status("FAILED"),
        "critical_missions": missions.count_critical_missions()
        }

@router.get("/missions-by-status")
def get_missions_by_status():
    return {
        "open": missions.count_open_missions(),
        "in_progress": missions.count_by_status("IN_PROGRESS"),
        "completed": missions.count_by_status("COMPLETE"),
        "failed": missions.count_by_status("FAILED"),
        "critical": missions.count_critical_missions()
        }

@router.get("/top-agent")
def get_top_agent():
    agent = missions.get_top_agent()
    if not agent:
        raise HTTPException(404, "No top agent")
    return agent