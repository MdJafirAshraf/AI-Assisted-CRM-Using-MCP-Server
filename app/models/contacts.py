from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime

from app.database import Base


class Contact(Base):
    __tablename__ = "contacts"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    phone = Column(String(20), default="")
    company = Column(String(100), default="")
    position = Column(String(100), default="")
    status = Column(String(20), default="active")  # active, inactive
    notes = Column(Text, default="")
    created_at = Column(DateTime, default=datetime.utcnow)

    deals = relationship("Deal", back_populates="contact")

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "phone": self.phone,
            "company": self.company,
            "position": self.position,
            "status": self.status,
            "notes": self.notes,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
