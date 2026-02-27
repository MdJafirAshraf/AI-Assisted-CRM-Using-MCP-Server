from fastapi import APIRouter, Depends, HTTPException, Request, Response
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.users import User
from app.schemas.users import UserCreate, UserLogin
from app.security import (
    hash_password,
    verify_password,
    create_access_token,
    get_current_user,
    get_current_user_optional,
    require_admin,
)

router = APIRouter(tags=["Authentication"])


# ═══ HTML Pages ═══

@router.get("/", response_class=HTMLResponse, include_in_schema=False)
def login_page(request: Request):
    # If already logged in, redirect to dashboard
    user = None
    try:
        from app.database import SessionLocal
        db = SessionLocal()
        token = request.cookies.get("access_token")
        if token:
            from app.security import decode_access_token
            payload = decode_access_token(token)
            if payload and payload.get("sub"):
                user = db.query(User).filter(User.id == payload.get("sub")).first()
        db.close()
    except Exception:
        pass
    if user:
        return RedirectResponse(url="/", status_code=302)
    return request.app.state.templates.TemplateResponse("login.html", {"request": request})


@router.get("/register", response_class=HTMLResponse, include_in_schema=False)
def register_page(request: Request, current_user: User = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    return request.app.state.templates.TemplateResponse(
        "register.html", {"request": request, "current_user": current_user}
    )


@router.get("/users", response_class=HTMLResponse, include_in_schema=False)
def users_page(request: Request, current_user: User = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    return request.app.state.templates.TemplateResponse(
        "users.html", {"request": request, "current_user": current_user}
    )


# ═══ API Endpoints ═══

@router.post("/api/auth/login", summary="Login")
def api_login(data: UserLogin, response: Response, db: Session = Depends(get_db)):
    """Authenticate user and set JWT cookie."""
    user = db.query(User).filter(User.email == data.email).first()
    if not user or not verify_password(data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid email or password")
        
    if not user.is_active:
        raise HTTPException(status_code=403, detail="Account is deactivated")

    token = create_access_token(data={"sub": user.id, "role": user.role})
    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        samesite="lax",
        max_age=60 * 60 * 24,  # 24 hours
    )
    return {"detail": "Login successful", "user": user.to_dict()}


@router.post("/api/auth/register", summary="Register a new user (admin only)")
def api_register(
    data: UserCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    """Create a new user account. Only admins can register new users."""
    # Check for existing email or username
    if db.query(User).filter(User.email == data.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")
    if db.query(User).filter(User.username == data.username).first():
        raise HTTPException(status_code=400, detail="Username already taken")

    user = User(
        username=data.username,
        email=data.email,
        hashed_password=hash_password(data.password),
        role=data.role if data.role in ("admin", "user") else "user",
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return {"detail": "User created", "user": user.to_dict()}


@router.post("/api/auth/logout", summary="Logout")
def api_logout(response: Response):
    """Clear the JWT cookie."""
    response.delete_cookie(key="access_token")
    return {"detail": "Logged out successfully"}


@router.get("/api/auth/me", summary="Get current user")
def api_me(current_user: User = Depends(get_current_user)):
    """Return the currently authenticated user's info."""
    return current_user.to_dict()


@router.get("/api/auth/users", summary="List all users (admin only)")
def api_list_users(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    """List all user accounts. Admin only."""
    users = db.query(User).order_by(User.created_at.desc()).all()
    return [u.to_dict() for u in users]


@router.delete("/api/auth/users/{user_id}", summary="Delete a user (admin only)")
def api_delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    """Delete a user account. Admin only. Cannot delete yourself."""
    if user_id == current_user.id:
        raise HTTPException(status_code=400, detail="Cannot delete your own account")
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()
    return {"detail": "User deleted", "id": user_id}
