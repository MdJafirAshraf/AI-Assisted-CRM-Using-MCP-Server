from pydantic import BaseModel
from typing import Optional


#  Task Schemas ─
class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = ""
    related_to: Optional[str] = ""
    related_id: Optional[int] = 0
    priority: Optional[str] = "medium"
    status: Optional[str] = "todo"
    due_date: Optional[str] = ""


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    related_to: Optional[str] = None
    related_id: Optional[int] = None
    priority: Optional[str] = None
    status: Optional[str] = None
    due_date: Optional[str] = None
