from sqlalchemy import Column, Integer, String, Float, Text, DateTime, ForeignKey
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


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    description = Column(Text, default="")
    related_to = Column(String(20), default="")  # contact, lead, deal
    related_id = Column(Integer, default=0)
    priority = Column(String(10), default="medium")  # low, medium, high
    status = Column(String(20), default="todo")  # todo, in_progress, done
    due_date = Column(String(20), default="")
    created_at = Column(DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "related_to": self.related_to,
            "related_id": self.related_id,
            "priority": self.priority,
            "status": self.status,
            "due_date": self.due_date,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
