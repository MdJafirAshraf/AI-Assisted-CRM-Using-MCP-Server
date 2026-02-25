from sqlalchemy import Column, Integer, String, Float, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

from app.database import Base


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
