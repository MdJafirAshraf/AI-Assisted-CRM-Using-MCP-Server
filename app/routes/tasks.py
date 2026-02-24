from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Task
from app.schemas import TaskCreate, TaskUpdate

router = APIRouter()


# ── HTML Page ──────────────────────────────────────────────
@router.get("/tasks", response_class=HTMLResponse, include_in_schema=False)
def tasks_page(request: Request):
    return request.app.state.templates.TemplateResponse("tasks.html", {"request": request})


# ── API Endpoints ──────────────────────────────────────────
@router.get("/api/tasks", summary="List all tasks", tags=["Tasks"])
def list_tasks(db: Session = Depends(get_db)):
    """Retrieve all tasks from the CRM database."""
    tasks = db.query(Task).order_by(Task.created_at.desc()).all()
    return [t.to_dict() for t in tasks]


@router.get("/api/tasks/{task_id}", summary="Get a task", tags=["Tasks"])
def get_task(task_id: int, db: Session = Depends(get_db)):
    """Retrieve a single task by ID."""
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task.to_dict()


@router.post("/api/tasks", summary="Create a task", tags=["Tasks"])
def create_task(
    data: TaskCreate,
    db: Session = Depends(get_db),
):
    """Create a new task in the CRM."""
    task = Task(
        title=data.title,
        description=data.description,
        related_to=data.related_to,
        related_id=data.related_id,
        priority=data.priority,
        status=data.status,
        due_date=data.due_date,
    )
    db.add(task)
    db.commit()
    db.refresh(task)
    return task.to_dict()


@router.put("/api/tasks/{task_id}", summary="Update a task", tags=["Tasks"])
def update_task(
    task_id: int,
    data: TaskUpdate,
    db: Session = Depends(get_db),
):
    """Update an existing task by ID."""
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    update_data = data.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(task, key, value)
        
    db.commit()
    db.refresh(task)
    return task.to_dict()


@router.delete("/api/tasks/{task_id}", summary="Delete a task", tags=["Tasks"])
def delete_task(task_id: int, db: Session = Depends(get_db)):
    """Delete a task from the CRM by ID."""
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    db.delete(task)
    db.commit()
    return {"detail": "Task deleted", "id": task_id}
