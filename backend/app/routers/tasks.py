from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from .. import schemas, models, auth
from ..database import get_db
from ..models import UserRole

router = APIRouter(
    tags=["tasks"],
    include_in_schema=True
)

@router.post("", response_model=schemas.TaskResponse)
def create_task(
    task: schemas.TaskCreate,
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(get_db)
):
    print(f"Creating task with data: {task.dict()}")  # Debug log
    db_task = models.Task(
        **task.dict(),
        created_by=current_user.id
    )
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    print(f"Created task: {db_task.__dict__}")  # Debug log
    return db_task

@router.get("", response_model=List[schemas.TaskResponse])
def read_tasks(
    skip: int = 0,
    limit: int = 100,
    member_id: int = None,  # Optional filter for admin to view specific member's tasks
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(get_db)
):
    try:
        print(f"Current user role: {current_user.role}")  # Debug log
        print(f"Current user id: {current_user.id}")  # Debug log
        
        # Start with base query
        query = db.query(models.Task)
        
        # Admin users can see all tasks or filter by member
        if current_user.role == UserRole.admin:
            print("User is admin, checking for member filter")  # Debug log
            if member_id is not None:
                # Verify the member exists
                member = db.query(models.User).filter(models.User.id == member_id).first()
                if not member:
                    raise HTTPException(status_code=404, detail="Member not found")
                print(f"Filtering tasks for member: {member.name}")  # Debug log
                query = query.filter(
                    (models.Task.created_by == member_id) |
                    (models.Task.assigned_to == member_id)
                )
            tasks = query.all()
            print(f"Found {len(tasks)} tasks")  # Debug log
            return tasks
        else:
            print("User is not admin, filtering tasks")  # Debug log
            # Regular users can only see tasks they created or are assigned to
            tasks = query.filter(
                (models.Task.created_by == current_user.id) |
                (models.Task.assigned_to == current_user.id)
            ).all()
            print(f"Found {len(tasks)} tasks for user")  # Debug log
            return tasks
    except Exception as e:
        print(f"Error in read_tasks: {str(e)}")  # Debug log
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )

@router.get("/{task_id}", response_model=schemas.TaskResponse)
def read_task(
    task_id: int,
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(get_db)
):
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    # Admin users can access any task
    if current_user.role != UserRole.admin and task.created_by != current_user.id and task.assigned_to != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to access this task")
    return task

@router.put("/{task_id}", response_model=schemas.TaskResponse)
def update_task(
    task_id: int,
    task_update: schemas.TaskUpdate,
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(get_db)
):
    db_task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    
    # Admin users can update any task
    if current_user.role != UserRole.admin and db_task.created_by != current_user.id and db_task.assigned_to != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to update this task")
    
    # Update task fields
    for key, value in task_update.dict(exclude_unset=True).items():
        setattr(db_task, key, value)
    
    db.commit()
    db.refresh(db_task)
    return db_task

@router.delete("/{task_id}")
def delete_task(
    task_id: int,
    current_user: models.User = Depends(auth.get_current_user),
    db: Session = Depends(get_db)
):
    db_task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    # Admin users can delete any task
    if current_user.role != UserRole.admin and db_task.created_by != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this task")
    
    db.delete(db_task)
    db.commit()
    return {"message": "Task deleted successfully"} 