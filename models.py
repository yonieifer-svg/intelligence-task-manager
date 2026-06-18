from pydantic import BaseModel, Field
from typing import Literal


class Agent(BaseModel):
    name: str = Field(max_length=50)
    specialty: str = Field(max_length=50)
    agent_rank: Literal["Junior", "Senior", "Commander"]


class Mission(BaseModel):
    title: str = Field(max_length=50)
    description: str
    location: str = Field(max_length=50)
    difficulty: int = Field(ge=1, le=10)
    importance: int = Field(ge=1, le=10)



