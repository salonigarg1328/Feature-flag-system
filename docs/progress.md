# Progress

## Week 1: Setup and Database (DONE)
- FastAPI backend created and running
- PostgreSQL 18 installed (E drive), database `featureflags`
- SQLAlchemy configured (DATABASE_URL in backend/.env)
- 9 models created: users, environments, flags, flag_versions,
  user_groups, user_group_memberships, targeting_rules,
  audit_log, evaluation_stats
- Alembic migration created and applied
- 11 foreign keys verified
- Sample records inserted (insert_sample.py)

## Decisions
- Driver: postgresql+psycopg2 (SQLAlchemy 2.x defaults to psycopg3)
- Unique constraint on (environment_id, key) in flags

## Week 2: Authentication (DONE)
- Packages: bcrypt (password hash), PyJWT (tokens), email-validator
- SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES added to .env
- app/core/security.py: hash_password, verify_password,
  create_access_token, decode_access_token
- app/schemas/user.py: UserRegister, UserLogin, UserResponse, TokenResponse
- POST /api/auth/register: validates input, rejects duplicate email (409),
  stores hashed password
- POST /api/auth/login: returns JWT; same 401 message for wrong email or
  wrong password; inactive users get 403
- app/core/dependencies.py: get_current_user (reads Bearer token)
- GET /api/auth/me: protected test API

## Decisions (Week 2)
- bcrypt used directly (password max 72 chars, enforced in schema)
- JWT stores only user id (sub) and expiry (exp); tokens expire in 60 minutes
- Emails stored in lowercase

## Week 3 - Feature Flag Management APIs

Status: Done

What was built:
- Flag schemas (create, update, response) with validation in `app/schemas/flag.py`
- Service layer in `app/services/flag_service.py`
- Five JWT-protected CRUD endpoints in `app/routers/flags.py`

Endpoints:
- POST   /api/v1/flags
- GET    /api/v1/flags
- GET    /api/v1/flags/{flag_id}
- PUT    /api/v1/flags/{flag_id}
- DELETE /api/v1/flags/{flag_id}

Rules and error handling:
- Missing token: 401/403
- Unknown flag or environment: 404
- Duplicate key in the same environment: 409
- Invalid key, type or default value: 422

Testing: all endpoints tested in Swagger UI, records verified in PostgreSQL (pgAdmin).

## Week 4 - Environment Management APIs

Status: Done

What was built:
- Environment schemas with name validation in `app/schemas/environment.py`
- Service layer in `app/services/environment_service.py`
- Six JWT-protected endpoints in `app/routers/environments.py`
- Foreign key relationship: flags.environment_id references environments.id

Endpoints:
- POST   /api/v1/environments
- GET    /api/v1/environments
- GET    /api/v1/environments/{environment_id}
- PUT    /api/v1/environments/{environment_id}
- DELETE /api/v1/environments/{environment_id}
- GET    /api/v1/environments/{environment_id}/flags

Rules and error handling:
- Missing token: 401/403
- Unknown environment: 404
- Duplicate environment name (case-insensitive): 409
- Invalid name: 422
- Delete blocked with 409 while the environment still has flags

Testing: all endpoints tested in Swagger UI, relationship verified in PostgreSQL (pgAdmin).