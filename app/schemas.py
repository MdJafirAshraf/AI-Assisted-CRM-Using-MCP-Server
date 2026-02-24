from pydantic import BaseModel
from typing import Optional


#  Contact Schemas 
class ContactCreate(BaseModel):
    name: str
    email: str
    phone: Optional[str] = ""
    company: Optional[str] = ""
    position: Optional[str] = ""
    status: Optional[str] = "active"
    notes: Optional[str] = ""


class ContactUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    company: Optional[str] = None
    position: Optional[str] = None
    status: Optional[str] = None
    notes: Optional[str] = None


#  Lead Schemas ─
class LeadCreate(BaseModel):
    name: str
    email: Optional[str] = ""
    company: Optional[str] = ""
    source: Optional[str] = "website"
    status: Optional[str] = "new"
    value: Optional[float] = 0.0
    notes: Optional[str] = ""


class LeadUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    company: Optional[str] = None
    source: Optional[str] = None
    status: Optional[str] = None
    value: Optional[float] = None
    notes: Optional[str] = None


#  Deal Schemas ─
class DealCreate(BaseModel):
    title: str
    contact_id: Optional[int] = None
    value: Optional[float] = 0.0
    stage: Optional[str] = "discovery"
    probability: Optional[int] = 10
    expected_close: Optional[str] = ""
    notes: Optional[str] = ""


class DealUpdate(BaseModel):
    title: Optional[str] = None
    contact_id: Optional[int] = None
    value: Optional[float] = None
    stage: Optional[str] = None
    probability: Optional[int] = None
    expected_close: Optional[str] = None
    notes: Optional[str] = None


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
