from typing import Optional
from sqlalchemy.orm import Session
from fastapi.responses import HTMLResponse
from fastapi import APIRouter, Depends, HTTPException, Request, Query, Body

from app.db import get_db
from app.models.users import User
from app.models.contacts import Contact
from app.schemas.contacts import ContactCreate, ContactUpdate

from app.dependencies.auth import get_current_user
from app.dependencies.permission import require_admin
from app.core.cache_invalidator import invalidate_user_cache

router = APIRouter(tags=["Contacts"], dependencies=[Depends(get_current_user)])


#  HTML Page 
@router.get("/contacts", response_class=HTMLResponse, include_in_schema=False)
def contacts_page(request: Request, current_user: User = Depends(get_current_user)):
    return request.app.state.templates.TemplateResponse(
        "contacts.html", {"request": request, "current_user": current_user}
    )


# ============================================
# API ENdpoints
# ============================================

@router.get("/api/contacts/{contact_id}", summary="Get a contact")
def get_contact(contact_id: int, db: Session = Depends(get_db)):
    """Retrieve a single contact by ID."""
    contact = db.get(Contact, contact_id)
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    return contact.to_dict()

@router.get("/api/contacts", summary="Retrieve all contacts")
def list_contacts(db: Session = Depends(get_db)):
    contacts = db.query(Contact).order_by(Contact.created_at.desc()).all()

    return [
        {k: v for k, v in c.to_dict().items()}
        for c in contacts
    ]

@router.put("/api/contacts/{contact_id}", summary="Update a contact")
@invalidate_user_cache
def update_contact(contact_id: int, data: ContactUpdate, db: Session = Depends(get_db)):
    """Update an existing contact by ID."""
    contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    
    update_data = data.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(contact, key, value)
        
    db.commit()
    db.refresh(contact)
    return contact.to_dict()


@router.delete("/api/contacts/{contact_id}", summary="Delete a contact")
@invalidate_user_cache
def delete_contact(contact_id: int, db: Session = Depends(get_db), current_user: User = Depends(require_admin)):
    """Delete a contact from the CRM by ID. Admin only."""
    contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    db.delete(contact)
    db.commit()
    return {"detail": "Contact deleted", "id": contact_id}


# ============================================
# API ENdpoints & MCP Tools
# ============================================

@router.get("/api/list-contacts",
summary="Retrieve all list of contacts",
operation_id="list_contacts", tags=["mcp"])
def list_contacts(db: Session = Depends(get_db)):
    contacts = db.query(Contact).order_by(Contact.created_at.desc()).all()

    return [
        {k: v for k, v in c.to_dict().items() if k != "id" and v not in [None, ""]}
        for c in contacts
    ]

@router.get("/api/contacts/search",
summary="Search and retrieve contacts by name, phone, or email",
operation_id="search_contacts", tags=["mcp"])
def get_contact_by_criteria(
    name: Optional[str] = Query(None, description="Name of the contact"),
    phone: Optional[str] = Query(None, description="Phone number of the contact"),
    email: Optional[str] = Query(None, description="Email address of the contact"),
    db: Session = Depends(get_db)
):
    query = db.query(Contact)

    if name:
        query = query.filter(Contact.name.ilike(f"%{name}%"))
    if phone:
        query = query.filter(Contact.phone.ilike(f"%{phone}%"))
    if email:
        query = query.filter(Contact.email.ilike(f"%{email}%"))

    contacts = query.all()

    result = []
    for c in contacts:
        data = c.to_dict()
        data.pop("id", None)
        clean_data = {k: v for k, v in data.items() if v not in [None, ""]}
        result.append(clean_data)

    return result


@router.post("/api/contacts",
summary="Create a new contact",
operation_id="create_contact", tags=["mcp"])
@invalidate_user_cache
def create_contact(data: ContactCreate, db: Session = Depends(get_db)):
    contact = Contact(**data.dict())

    db.add(contact)
    db.commit()
    db.refresh(contact)

    return {
        k: v for k, v in contact.to_dict().items()
        if k != "id" and v not in [None, ""]
    }


@router.put("/api/contacts/by-email",
summary="Update a contact using email",
operation_id="update_contact_by_email", tags=["mcp"])
@invalidate_user_cache
def update_contact_by_email(
    email: str = Query(..., description="Email of the contact to update"),
    data: ContactUpdate = Body(...),
    db: Session = Depends(get_db)
):
    contact = db.query(Contact).filter(Contact.email == email).first()

    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")

    update_data = data.dict(exclude_unset=True)

    for key, value in update_data.items():
        setattr(contact, key, value)

    db.commit()
    db.refresh(contact)

    return {
        k: v for k, v in contact.to_dict().items()
        if k != "id" and v not in [None, ""]
    }