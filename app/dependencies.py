from fastapi import Header, HTTPException, status
from .database import db

async def verify_api_key(
    api_key: str = Header(..., description="API key required for access"),
    user_agent: str = Header(..., description="User agent information")
):
    if api_key != "your-secret-key":  
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key"
        )
    print(f"Request from: {user_agent} with API key: {api_key}")
    return api_key

def get_db():
    return db 