import sys
import os
from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context

# Add app to PYTHONPATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.core.config import settings
from app.db.base import Base  # all models

# Load .ini config
config = context.config

# Set up logging
fileConfig(config.config_file_name)

# Don't call .set_main_option() — just use settings directly
target_metadata = Base.metadata

def run_migrations_online():
    connectable = engine_from_config(
        {
            "sqlalchemy.url": settings.DATABASE_URL  # <-- pass directly here
        },
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
        )
        with context.begin_transaction():
            context.run_migrations()

run_migrations_online()
