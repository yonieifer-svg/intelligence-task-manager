from pydantic import BaseModel, Field


class Agent(BaseModel):
    name: str = Field(max_length=50)
    specialty: str = Field(max_length=50)
    agent_rank: str = Field(max_length=50)


class Mission(BaseModel):
    title: str = Field(max_length=50)
    description: str
    location: str = Field(max_length=50)
    difficulty: int
    importance: int



