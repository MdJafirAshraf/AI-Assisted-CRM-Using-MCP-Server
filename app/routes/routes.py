from fastapi import APIRouter
from .routers import auth, chat, dashboard, contacts, deals, leads, tasks

router = APIRouter()
router.include_router(auth.router, prefix="")
router.include_router(dashboard.router)
router.include_router(contacts.router)
router.include_router(leads.router)
router.include_router(deals.router)
router.include_router(tasks.router)
router.include_router(chat.router)