from pydantic import BaseModel, EmailStr
from datetime import datetime, date
from typing import Optional, List
from .models import UserRole, TaskStatus, Priority

class UserBase(BaseModel):
    name: str
    email: EmailStr
    role: UserRole = UserRole.member

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    role: Optional[UserRole] = None

class PasswordUpdate(BaseModel):
    new_password: str

class User(BaseModel):
    id: int
    email: EmailStr
    name: str
    role: str  # Changed to str to match the serialized value
    created_at: datetime

    class Config:
        from_attributes = True
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    due_date: Optional[date] = None
    priority: Priority = Priority.medium

class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None
    status: TaskStatus = TaskStatus.pending
    priority: Priority = Priority.medium
    due_date: Optional[date] = None
    assigned_to: Optional[int] = None

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[TaskStatus] = None
    priority: Optional[Priority] = None
    due_date: Optional[date] = None
    assigned_to: Optional[int] = None

class Task(TaskBase):
    id: int
    assigned_to: int
    created_by: int
    status: TaskStatus
    created_at: datetime
    updated_at: datetime
    assignee: User
    creator: User

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

class NoteBase(BaseModel):
    content: str

class NoteCreate(NoteBase):
    task_id: int

class Note(NoteBase):
    id: int
    created_at: datetime
    updated_at: datetime
    task_id: int
    user_id: int

    class Config:
        from_attributes = True

class TaskResponse(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    status: TaskStatus
    priority: Priority
    due_date: Optional[date] = None
    created_by: Optional[int] = None
    assigned_to: Optional[int] = None
    created_at: datetime
    assignee: Optional[User] = None
    creator: Optional[User] = None

    class Config:
        from_attributes = True
        json_encoders = {
            datetime: lambda v: v.isoformat(),
            date: lambda v: v.isoformat()
        }

class LoginCredentials(BaseModel):
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    user: User

    class Config:
        from_attributes = True
        json_encoders = {
            datetime: lambda v: v.isoformat()
        } 