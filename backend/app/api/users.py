import uuid
from fastapi import Depends, APIRouter, Request, Query, APIRouter, Security, HTTPException
from sqlmodel import Session, select


from backend.app.core.deps import sessionDEP
from backend.app.core.config import settings
from typing import List

router = APIRouter(prefix="/users", tags=["users"])


