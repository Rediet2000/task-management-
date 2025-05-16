# Task Management System for Network and System Administration

A web-based task management system designed for network and system administration teams to track and manage daily and weekly tasks.

## Features

- User authentication and authorization (Admin/Member roles)
- Task creation, assignment, and tracking
- Task status management (Pending, In Progress, Completed)
- Dashboard for task overview
- Team member task management
- Admin controls for user and task management

## Technology Stack

- Frontend: React.js
- Backend: FastAPI (Python)
- Database: PostgreSQL
- Authentication: JWT tokens

## Setup Instructions

### Prerequisites

- Python 3.8+
- Node.js 14+
- PostgreSQL 12+

### Backend Setup

1. Create a virtual environment and activate it:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Create PostgreSQL database:
   ```sql
   CREATE DATABASE taskmanagement;
   ```

4. Set up environment variables:
   - Copy `.env.example` to `.env`
   - Update the database URL and secret key

5. Run database migrations:
   ```bash
   alembic upgrade head
   ```

6. Start the backend server:
   ```bash
   uvicorn app.main:app --reload
   ```

### Frontend Setup

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start the development server:
   ```bash
   npm start
   ```

## API Documentation

Once the backend server is running, visit `http://localhost:8000/docs` for the interactive API documentation.

## Security Considerations

- Replace the default secret key in production
- Configure CORS settings for production
- Use HTTPS in production
- Implement rate limiting
- Regular security updates

## Development

1. Backend API endpoints are in `backend/app/main.py`
2. Database models are in `backend/app/models.py`
3. Frontend components are in `frontend/src/components`
4. API integration is in `frontend/src/api`

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

MIT License 