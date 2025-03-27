from typing import Optional
import uuid
from enum import Enum

from sqlmodel import SQLModel, Field
from datetime import datetime

class Status(Enum):
    PREPARING = 'preparing'
    PROCESSING = 'processing'
    COMPLETED = 'completed'

class ProjectBase(SQLModel):
    name: str
    created_at: datetime = Field(default_factory=datetime.now)
    status: Status = Field(default=Status.PREPARING)
    raw_dataset_path: str
    final_data_set_path: Optional[str] = None
    raw_dataset_size: int = Field(default=0)
    final_dataset_size: int = Field(default=0)

class ProjectCreate(ProjectBase):
    pass

class ProjectRead(ProjectBase):
    id: uuid.UUID

class ProjectReadAll(SQLModel):
    projects: list[ProjectRead] = []
    count: int

class Project(ProjectBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
