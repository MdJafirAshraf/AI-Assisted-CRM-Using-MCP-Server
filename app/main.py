import os, uuid
from sqlalchemy.orm import Session
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from fastmcp import FastMCP
import httpx
from fastmcp.server.dependencies import get_http_request
from app.models.users import User
from app.db import engine, Base, SessionLocal
from app.routes.routes import router
from app.dependencies.auth import get_current_user
from app.core.security import hash_password


def seed_admin(db: Session):
    """Create default admin account if no users exist."""
    if db.query(User).count() == 0:
        admin = User(
            user_id=uuid.uuid4().int >> 64, 
            username="Admin",
            email="admin@crm.com",
            hashed_password=hash_password("admin123"),
            role="admin",
            is_active=True,
        )
        db.add(admin)
        db.commit()
        print("✅  Default admin created (admin@crm.com / admin123)")


# Lifespan for FastAPI app
@asynccontextmanager
async def app_lifespan(app: FastAPI):
    # Startup: Create database tables
    Base.metadata.create_all(bind=engine)
    # Seed default admin
    db = SessionLocal()
    try:
        seed_admin(db)
    finally:
        db.close()
    yield
    # Shutdown: Nothing to clean up for now
    pass

# Combine FastAPI and MCP lifespans
@asynccontextmanager
async def combined_lifespan(fastapi_app: FastAPI):
    async with app_lifespan(fastapi_app):
        async with mcp_app.lifespan(fastapi_app):
            yield

#  FastAPI App 
app = FastAPI(
    title="CRM with MCP Server",
    description="A CRM application with MCP (Model Context Protocol) server integration",
    lifespan=combined_lifespan
)

# app middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)

#  Static & Templates 
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
app.mount("/static", StaticFiles(directory=os.path.join(BASE_DIR, "static")), name="static")

templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))
app.state.templates = templates

#  Include Routers
app.include_router(router, tags=["API Endpoints"])


# ═══ Auth Exception Handler ═══
# Redirect 401 errors on HTML page requests to the login page
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi.responses import JSONResponse

@app.exception_handler(StarletteHTTPException)
async def custom_http_exception_handler(request: Request, exc: StarletteHTTPException):
    if exc.status_code == 401:
        # If it's a page request (not API), redirect to login
        accept = request.headers.get("accept", "")
        if "text/html" in accept and not request.url.path.startswith("/api/"):
            return RedirectResponse(url="/", status_code=302)
    if exc.status_code == 403:
        accept = request.headers.get("accept", "")
        if "text/html" in accept and not request.url.path.startswith("/api/"):
            return RedirectResponse(url="/", status_code=302)
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )


class MCPForwardAuth(httpx.Auth):
    def auth_flow(self, request):
        try:
            req = get_http_request()
            auth = req.headers.get("Authorization")
            if auth:
                request.headers["Authorization"] = auth
        except Exception:
            pass
        yield request

# Convert to MCP server
mcp = FastMCP.from_fastapi(
    app=app,
    httpx_client_kwargs={"auth": MCPForwardAuth()}
) 
mcp_app = mcp.http_app(path='/mcp') # Create ASGI app from MCP server
# mount MCP app to FastAPI app
app.mount("/llm", mcp_app)

print("✅  MCP Server mounted at /mcp")
       
