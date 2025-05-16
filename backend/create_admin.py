from sqlalchemy.orm import Session
from app.database import SessionLocal, engine
from app.models import User, UserRole, Base
from app.auth import get_password_hash

# Create tables if they don't exist
Base.metadata.create_all(bind=engine)

def create_admin_user(db: Session):
    # Check if admin user already exists
    admin = db.query(User).filter(User.email == "admin@example.com").first()
    if admin:
        print("Admin user already exists")
        return admin
    
    # Create admin user
    admin_user = User(
        name="Admin",
        email="admin@example.com",
        role=UserRole.admin,
        hashed_password=get_password_hash("admin123")  # Change this password in production
    )
    
    db.add(admin_user)
    db.commit()
    db.refresh(admin_user)
    print("Admin user created successfully!")
    print("Email: admin@example.com")
    print("Password: admin123")
    return admin_user

if __name__ == "__main__":
    db = SessionLocal()
    try:
        create_admin_user(db)
    finally:
        db.close() 