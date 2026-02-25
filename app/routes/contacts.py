from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Contact
from app.schemas import ContactCreate, ContactUpdate

router = APIRouter(tags=["Contacts"])


#  HTML Page 
@router.get("/contacts", response_class=HTMLResponse, include_in_schema=False)
def contacts_page(request: Request):
    return request.app.state.templates.TemplateResponse("contacts.html", {"request": request})


#  API Endpoints 
@router.get("/api/contacts", summary="List all contacts")
def list_contacts(db: Session = Depends(get_db)):
    """Retrieve all contacts from the CRM database."""
    contacts = db.query(Contact).order_by(Contact.created_at.desc()).all()
    return [c.to_dict() for c in contacts]


@router.get("/api/contacts/{contact_id}", summary="Get a contact")
def get_contact(contact_id: int, db: Session = Depends(get_db)):
    """Retrieve a single contact by ID."""
    contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    return contact.to_dict()


@router.post("/api/contacts", summary="Create a contact")
def create_contact(
    data: ContactCreate,
    db: Session = Depends(get_db),
):
    """Create a new contact in the CRM."""
    contact = Contact(
        name=data.name,
        email=data.email,
        phone=data.phone,
        company=data.company,
        position=data.position,
        status=data.status,
        notes=data.notes,
    )
    db.add(contact)
    db.commit()
    db.refresh(contact)
    return contact.to_dict()


@router.put("/api/contacts/{contact_id}", summary="Update a contact", tags=["Contacts"])
def update_contact(
    contact_id: int,
    data: ContactUpdate,
    db: Session = Depends(get_db),
):
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


@router.delete("/api/contacts/{contact_id}", summary="Delete a contact", tags=["Contacts"])
def delete_contact(contact_id: int, db: Session = Depends(get_db)):
    """Delete a contact from the CRM by ID."""
    contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    db.delete(contact)
    db.commit()
    return {"detail": "Contact deleted", "id": contact_id}
