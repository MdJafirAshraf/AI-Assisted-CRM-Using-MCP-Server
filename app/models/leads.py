from sqlalchemy import Column, Integer, String, Float, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

from app.database import Base


class Lead(Base):
    __tablename__ = "leads"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), default="")
    company = Column(String(100), default="")
    source = Column(String(50), default="website")  # website, referral, social, email, other
    status = Column(String(20), default="new")  # new, contacted, qualified, lost
    value = Column(Float, default=0.0)
    notes = Column(Text, default="")
    created_at = Column(DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "company": self.company,
            "source": self.source,
            "status": self.status,
            "value": self.value,
            "notes": self.notes,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
