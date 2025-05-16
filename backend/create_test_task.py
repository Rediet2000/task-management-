from sqlalchemy.orm import Session
from app.database import SessionLocal, engine
from app.models import Task, User, TaskStatus, Base
from datetime import date

def create_test_task(db: Session):
    # Get the admin user
    admin = db.query(User).filter(User.email == "admin@example.com").first()
    if not admin:
        print("Admin user not found!")
        return
    
    # Create a test task
    test_task = Task(
        title="Welcome to Task Management System",
        description="This is a test task to verify that the system is working correctly.",
        assigned_to=admin.id,
        created_by=admin.id,
        status=TaskStatus.pending,
        due_date=date.today()
    )
    
    db.add(test_task)
    db.commit()
    db.refresh(test_task)
    print("Test task created successfully!")

if __name__ == "__main__":
    db = SessionLocal()
    try:
        create_test_task(db)
    finally:
        db.close() 