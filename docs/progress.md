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

## Next: Week 3
Environments and Feature Flags CRUD APIs