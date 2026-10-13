from app.database.database import SessionLocal
from app.models import User, Environment, Flag

db = SessionLocal()
try:
    env = Environment(name="development", description="Development environment")
    user = User(
        name="Test User",
        email="test@example.com",
        password_hash="not_a_real_hash",
        role="admin",
    )
    db.add_all([env, user])
    db.commit()
    db.refresh(env)
    db.refresh(user)

    flag = Flag(
        environment_id=env.id,
        key="new_dashboard",
        type="boolean",
        default_value=False,
        enabled=True,
        description="Sample flag",
        owner_team="platform",
        created_by=user.id,
    )
    db.add(flag)
    db.commit()
    db.refresh(flag)

    print("Created:", env.name, "|", user.email, "|", flag.key)
    print("Flag ka environment (relationship se):", flag.environment.name)
finally:
    db.close()