from fastapi import Header, HTTPException, status
from .database import db

async def verify_api_key(
    api_key: str = Header(...),
    user_agent: str = Header(...)
):
    if api_key != "your-secret-key":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key"
        )
    print(f"Request from: {user_agent} with API key: {api_key}")
    return api_key

async def verify_admin_role(
    role: str = Header(...),
):
    if role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    return role

def get_db():
    return db 