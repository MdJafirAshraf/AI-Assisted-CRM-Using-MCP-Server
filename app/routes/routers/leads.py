from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.leads import Lead
from app.models.users import User
from app.schemas.leads import LeadCreate, LeadUpdate
from app.security import get_current_user, require_admin

router = APIRouter(tags=["Leads"])


#  HTML Page 
@router.get("/leads", response_class=HTMLResponse, include_in_schema=False)
def leads_page(request: Request, current_user: User = Depends(get_current_user)):
    return request.app.state.templates.TemplateResponse(
        "leads.html", {"request": request, "current_user": current_user}
    )


#  API Endpoints 
@router.get("/api/leads", summary="List all leads")
def list_leads(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Retrieve all leads from the CRM database."""
    leads = db.query(Lead).order_by(Lead.created_at.desc()).all()
    return [l.to_dict() for l in leads]


@router.get("/api/leads/{lead_id}", summary="Get a lead")
def get_lead(lead_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Retrieve a single lead by ID."""
    lead = db.query(Lead).filter(Lead.id == lead_id).first()
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")
    return lead.to_dict()


@router.post("/api/leads", summary="Create a lead")
def create_lead(
    data: LeadCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Create a new lead in the CRM."""
    lead = Lead(
        name=data.name,
        email=data.email,
        company=data.company,
        source=data.source,
        status=data.status,
        value=data.value,
        notes=data.notes,
    )
    db.add(lead)
    db.commit()
    db.refresh(lead)
    return lead.to_dict()


@router.put("/api/leads/{lead_id}", summary="Update a lead")
def update_lead(
    lead_id: int,
    data: LeadUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Update an existing lead by ID."""
    lead = db.query(Lead).filter(Lead.id == lead_id).first()
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")
    
    update_data = data.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(lead, key, value)

    db.commit()
    db.refresh(lead)
    return lead.to_dict()


@router.delete("/api/leads/{lead_id}", summary="Delete a lead")
def delete_lead(
    lead_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    """Delete a lead from the CRM by ID. Admin only."""
    lead = db.query(Lead).filter(Lead.id == lead_id).first()
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")
    db.delete(lead)
    db.commit()
    return {"detail": "Lead deleted", "id": lead_id}
