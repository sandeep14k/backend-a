from fastapi import Header, HTTPException, Depends, status
from sqlalchemy.orm import Session
from database import get_db
import models

# ==========================================
# Core Authentication Dependency
# ==========================================
def get_current_user(
    user_id: int = Header(..., description="Mock Auth: Pass your User ID here (e.g., 1 for Admin)"), 
    db: Session = Depends(get_db)
) -> models.User:
    """
    Validates the user via a mock Header ID. 
    In a real app, this would decode a JWT token from the Authorization header.
    """
    user = db.query(models.User).filter(models.User.id == user_id).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="User not found. Please provide a valid User-ID in the headers."
        )
        
    if user.status != "active":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="User account is inactive. Contact an administrator."
        )
        
    return user

# ==========================================
# Authorization Guards (Role Checks)
# ==========================================
def require_admin(current_user: models.User = Depends(get_current_user)) -> models.User:
    """Requires the user to have the 'admin' role."""
    if current_user.role != models.RoleEnum.admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="Insufficient permissions. Admin privileges required."
        )
    return current_user

def require_analyst_or_admin(current_user: models.User = Depends(get_current_user)) -> models.User:
    """Requires the user to be at least an 'analyst'."""
    if current_user.role not in [models.RoleEnum.analyst, models.RoleEnum.admin]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="Insufficient permissions. Analyst or Admin privileges required."
        )
    return current_user