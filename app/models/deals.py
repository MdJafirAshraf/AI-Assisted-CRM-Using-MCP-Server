from sqlalchemy import Column, Integer, String, Float, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

from app.db import Base


class Deal(Base):
    __tablename__ = "deals"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    contact_id = Column(Integer, ForeignKey("contacts.id"), nullable=True)
    value = Column(Float, default=0.0)
    stage = Column(String(30), default="discovery")  # discovery, proposal, negotiation, won, lost
    probability = Column(Integer, default=10)  # 0-100
    expected_close = Column(String(20), default="")
    notes = Column(Text, default="")
    created_at = Column(DateTime, default=datetime.utcnow)

    contact = relationship("Contact", back_populates="deals")

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "contact_id": self.contact_id,
            "contact_name": self.contact.name if self.contact else None,
            "value": self.value,
            "stage": self.stage,
            "probability": self.probability,
            "expected_close": self.expected_close,
            "notes": self.notes,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }

