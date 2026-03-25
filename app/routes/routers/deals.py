from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session

from app.db import get_db
from app.models.deals import Deal
from app.models.users import User
from app.schemas.deals import DealCreate, DealUpdate
from app.dependencies.auth import get_current_user
from app.dependencies.permission import require_admin

router = APIRouter(tags=["Deals"], dependencies=[Depends(get_current_user)])


#  HTML Page 
@router.get("/deals", response_class=HTMLResponse, include_in_schema=False)
def deals_page(request: Request, current_user: User = Depends(get_current_user)):
    return request.app.state.templates.TemplateResponse(
        "deals.html", {"request": request, "current_user": current_user}
    )


#  API Endpoints 
@router.get("/api/deals", summary="List all deals", tags=["mcp"])
def list_deals(db: Session = Depends(get_db)):
    """Retrieve all deals from the CRM database."""
    deals = db.query(Deal).order_by(Deal.created_at.desc()).all()
    return [d.to_dict() for d in deals]


@router.get("/api/deals/{deal_id}", summary="Get a deal")
def get_deal(deal_id: int, db: Session = Depends(get_db)):
    """Retrieve a single deal by ID."""
    deal = db.query(Deal).filter(Deal.id == deal_id).first()
    if not deal:
        raise HTTPException(status_code=404, detail="Deal not found")
    return deal.to_dict()


@router.post("/api/deals", summary="Create a deal", tags=["mcp"])
def create_deal(data: DealCreate, db: Session = Depends(get_db)):
    """Create a new deal in the CRM."""
    deal = Deal(
        title=data.title,
        contact_id=data.contact_id,
        value=data.value,
        stage=data.stage,
        probability=data.probability,
        expected_close=data.expected_close,
        notes=data.notes,
    )
    db.add(deal)
    db.commit()
    db.refresh(deal)
    return deal.to_dict()


@router.put("/api/deals/{deal_id}", summary="Update a deal")
def update_deal(deal_id: int, data: DealUpdate, db: Session = Depends(get_db)):
    """Update an existing deal by ID."""
    deal = db.query(Deal).filter(Deal.id == deal_id).first()
    if not deal:
        raise HTTPException(status_code=404, detail="Deal not found")
    
    update_data = data.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(deal, key, value)

    db.commit()
    db.refresh(deal)
    return deal.to_dict()


@router.delete("/api/deals/{deal_id}", summary="Delete a deal")
def delete_deal(deal_id: int, db: Session = Depends(get_db), current_user: User = Depends(require_admin)):
    """Delete a deal from the CRM by ID. Admin only."""
    deal = db.query(Deal).filter(Deal.id == deal_id).first()
    if not deal:
        raise HTTPException(status_code=404, detail="Deal not found")
    db.delete(deal)
    db.commit()
    return {"detail": "Deal deleted", "id": deal_id}
