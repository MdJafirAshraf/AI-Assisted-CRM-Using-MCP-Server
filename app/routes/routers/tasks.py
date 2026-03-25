from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session

from app.db import get_db
from app.models.tasks import Task
from app.models.users import User
from app.schemas.tasks import TaskCreate, TaskUpdate
from app.dependencies.auth import get_current_user
from app.dependencies.permission import require_admin

router = APIRouter(tags=["Tasks"], dependencies=[Depends(get_current_user)])


#  HTML Page 
@router.get("/tasks", response_class=HTMLResponse, include_in_schema=False)
def tasks_page(request: Request, current_user: User = Depends(get_current_user)):
    return request.app.state.templates.TemplateResponse(
        "tasks.html", {"request": request, "current_user": current_user}
    )


#  API Endpoints 
@router.get("/api/tasks", summary="List all tasks", tags=["mcp"])
def list_tasks(db: Session = Depends(get_db)):
    """Retrieve all tasks from the CRM database."""
    tasks = db.query(Task).order_by(Task.created_at.desc()).all()
    return [t.to_dict() for t in tasks]


@router.get("/api/tasks/{task_id}", summary="Get a task")
def get_task(task_id: int, db: Session = Depends(get_db)):
    """Retrieve a single task by ID."""
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task.to_dict()


@router.post("/api/tasks", summary="Create a task", tags=["mcp"])
def create_task(data: TaskCreate, db: Session = Depends(get_db)):
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


@router.put("/api/tasks/{task_id}", summary="Update a task", tags=["mcp"])
def update_task(task_id: int, data: TaskUpdate, db: Session = Depends(get_db)):
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


@router.delete("/api/tasks/{task_id}", summary="Delete a task")
def delete_task(task_id: int, db: Session = Depends(get_db), current_user: User = Depends(require_admin)):
    """Delete a task from the CRM by ID. Admin only."""
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    db.delete(task)
    db.commit()
    return {"detail": "Task deleted", "id": task_id}
