# Import your SQLAlchemy models
from sqlalchemy import create_engine, text

from src.api import app, db
from flask_migrate import Migrate
from src.models.models import *

db.init_app(app)
migrate = Migrate(app, db)


def create_database():
    """Create the database if it doesn't exist."""
    DATABASE_URI = app.config.get("DATABASE_URI", "")
    engine = create_engine(DATABASE_URI)
    database_name = app.config.get("DATABASE_NAME", "hospital_management")
    print(f"Creating database if not present: {database_name}")
    with engine.connect().execution_options(autocommit=True) as connection:
        connection.execute(text(f"CREATE DATABASE IF NOT EXISTS {database_name}"))


def main():
    create_database()


if __name__ == "__main__":
    main()
