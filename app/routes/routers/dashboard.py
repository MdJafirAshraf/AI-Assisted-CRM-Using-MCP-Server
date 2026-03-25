from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session

from app.db import get_db
from app.models.tasks import Task
from app.models.users import User
from app.models.contacts import Contact
from app.models.leads import Lead
from app.models.deals import Deal
from app.dependencies.auth import get_current_user

router = APIRouter(tags=["Tasks"])
    

#  Dashboard
@router.get("/dashboard", response_class=HTMLResponse, include_in_schema=False)
def dashboard(request: Request, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    try:
        stats = {
            "total_contacts": db.query(Contact).count(),
            "active_contacts": db.query(Contact).filter(Contact.status == "active").count(),
            "total_leads": db.query(Lead).count(),
            "new_leads": db.query(Lead).filter(Lead.status == "new").count(),
            "qualified_leads": db.query(Lead).filter(Lead.status == "qualified").count(),
            "total_deals": db.query(Deal).count(),
            "won_deals": db.query(Deal).filter(Deal.stage == "won").count(),
            "total_deal_value": db.query(Deal).with_entities(
                __import__('sqlalchemy').func.coalesce(__import__('sqlalchemy').func.sum(Deal.value), 0)
            ).scalar(),
            "total_tasks": db.query(Task).count(),
            "pending_tasks": db.query(Task).filter(Task.status != "done").count(),
            "recent_contacts": [c.to_dict() for c in db.query(Contact).order_by(Contact.created_at.desc()).limit(5).all()],
            "recent_leads": [l.to_dict() for l in db.query(Lead).order_by(Lead.created_at.desc()).limit(5).all()],
            "recent_deals": [d.to_dict() for d in db.query(Deal).order_by(Deal.created_at.desc()).limit(5).all()],
            "deals_by_stage": {
                "discovery": db.query(Deal).filter(Deal.stage == "discovery").count(),
                "proposal": db.query(Deal).filter(Deal.stage == "proposal").count(),
                "negotiation": db.query(Deal).filter(Deal.stage == "negotiation").count(),
                "won": db.query(Deal).filter(Deal.stage == "won").count(),
                "lost": db.query(Deal).filter(Deal.stage == "lost").count(),
            },
        }
    finally:
        db.close()
    return request.app.state.templates.TemplateResponse(
        "dashboard.html", {"request": request, "stats": stats, "current_user": current_user}
    )


#  Dashboard API
@router.get("/api/dashboard", summary="Get dashboard stats")
def dashboard_api(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Retrieve summary statistics for the CRM dashboard."""
    try:
        from sqlalchemy import func
        stats = {
            "total_contacts": db.query(Contact).count(),
            "active_contacts": db.query(Contact).filter(Contact.status == "active").count(),
            "total_leads": db.query(Lead).count(),
            "new_leads": db.query(Lead).filter(Lead.status == "new").count(),
            "total_deals": db.query(Deal).count(),
            "won_deals": db.query(Deal).filter(Deal.stage == "won").count(),
            "total_deal_value": db.query(func.coalesce(func.sum(Deal.value), 0)).scalar(),
            "total_tasks": db.query(Task).count(),
            "pending_tasks": db.query(Task).filter(Task.status != "done").count(),
        }
    finally:
        db.close()
    return stats

