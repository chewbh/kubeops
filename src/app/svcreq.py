
from fastapi import APIRouter, Depends, Request, HTTPException

router = APIRouter()


@router.get("/")
def get_requests():
    """
    Get all service requests.
    """
    return {"service": "requests"}
