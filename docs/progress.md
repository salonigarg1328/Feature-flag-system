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

## Next: Week 2
Registration, login, JWT authentication