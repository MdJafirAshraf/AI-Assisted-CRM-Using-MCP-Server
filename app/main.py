from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastmcp import FastMCP

from sqlalchemy.orm import Session
from contextlib import asynccontextmanager
import os

from app.database import engine, Base, SessionLocal
from app.models import Contact, Lead, Deal, Task
from app.routes import contacts, leads, deals, tasks
from app.routes import chat


@asynccontextmanager
async def app_lifespan(app: FastAPI):
    # Startup: Create database tables
    Base.metadata.create_all(bind=engine)
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

#  Static & Templates 
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
app.mount("/static", StaticFiles(directory=os.path.join(BASE_DIR, "static")), name="static")

templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))
app.state.templates = templates

#  Include Routers
app.include_router(contacts.router)
app.include_router(leads.router)
app.include_router(deals.router)
app.include_router(tasks.router)
app.include_router(chat.router)


#  Dashboard
@app.get("/", response_class=HTMLResponse, include_in_schema=False)
def dashboard(request: Request):
    db: Session = SessionLocal()
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
    return templates.TemplateResponse("dashboard.html", {"request": request, "stats": stats})


#  Dashboard API
@app.get("/api/dashboard", summary="Get dashboard stats", tags=["Dashboard"])
def dashboard_api():
    """Retrieve summary statistics for the CRM dashboard."""
    db: Session = SessionLocal()
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



# Convert to MCP server
mcp = FastMCP.from_fastapi(app=app)

# Create ASGI app from MCP server
mcp_app = mcp.http_app(path='/mcp')

# mount MCP app to FastAPI app
app.mount("/llm", mcp_app)

print("✅  MCP Server mounted at /mcp")
       
