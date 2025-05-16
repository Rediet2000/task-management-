from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from .. import schemas, auth
from ..database import get_db
from .. import models
from ..models import UserRole

router = APIRouter()  # Remove the prefix since it's added in main.py

@router.post("/login", response_model=schemas.TokenResponse)
def login(
    credentials: schemas.LoginCredentials,
    db: Session = Depends(get_db)
):
    print(f"Login attempt for email: {credentials.email}")  # Debug log
    
    user = db.query(models.User).filter(models.User.email == credentials.email).first()
    if not user or not auth.verify_password(credentials.password, user.hashed_password):
        raise HTTPException(
            status_code=401,
            detail="Incorrect email or password"
        )
    
    # Create token with just the email
    access_token = auth.create_access_token(data={"sub": user.email})
    print(f"Login successful for user: {user.email} with role: {user.role}")  # Debug log
    
    # Ensure role is properly serialized
    user_role = user.role.value if isinstance(user.role, UserRole) else str(user.role)
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "email": user.email,
            "name": user.name,
            "role": user_role,
            "created_at": user.created_at
        }
    } 