# Feature Flag Management System

Infosys Springboard project. Web-based feature flag system with
environments, targeting rules, user groups and audit logs.

## Tech stack
- Backend: Python, FastAPI, SQLAlchemy, PostgreSQL, Alembic
- Frontend: React, TypeScript, Vite (planned, Week 6)

## Run the backend
    cd backend
    venv\Scripts\activate
    uvicorn app.main:app --reload

API docs: http://127.0.0.1:8000/docs

## Setup
See docs/setup.md

## API Endpoints

### Authentication
| Method | Endpoint | Purpose |
|---|---|---|
| POST | /api/auth/register | Register a user |
| POST | /api/auth/login | Login and get a JWT token |
| GET | /api/auth/me | Current user (protected) |

### Feature Flags (JWT required)
| Method | Endpoint | Purpose |
|---|---|---|
| POST | /api/v1/flags | Create a flag |
| GET | /api/v1/flags | List all flags (optional `environment_id` filter) |
| GET | /api/v1/flags/{flag_id} | Get one flag |
| PUT | /api/v1/flags/{flag_id} | Update a flag |
| DELETE | /api/v1/flags/{flag_id} | Delete a flag |

Swagger UI: http://127.0.0.1:8000/docs