from fastapi import Depends, HTTPException, status, Header
from typing import Optional
from app.config import settings


async def verify_api_key(x_api_key: Optional[str] = Header(None)) -> str:
    """
    Dependency to verify API key from X-API-Key header.
    
    TODO: Replace with JWT authentication in production.
    This API key validation is suitable for development/testing only.
    Implement proper JWT token validation for production environments.
    
    Args:
        x_api_key: API key from X-API-Key header
        
    Returns:
        The valid API key
        
    Raises:
        HTTPException: 401 if key is missing or invalid
    """
    if not x_api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing X-API-Key header",
            headers={"WWW-Authenticate": "ApiKey"},
        )
    
    if x_api_key != settings.API_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key",
            headers={"WWW-Authenticate": "ApiKey"},
        )
    
    return x_api_key
