from pydantic import BaseModel
from typing import Optional


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