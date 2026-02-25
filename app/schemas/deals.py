from pydantic import BaseModel
from typing import Optional


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