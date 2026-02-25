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