# Import your SQLAlchemy models
import sys
import time

from flask_migrate import Migrate
from sqlalchemy import text

from src.api import app, db
from src.models.models import *

db.init_app(app)
migrate = Migrate(app, db)


def create_database():
    """Create the database if it doesn't exist."""
    database_name = app.config.get("DATABASE_NAME", "hospital_management")
    print(f"Creating database if not present: {database_name}")
    with app.app_context():
        db.session.execute(text(f"CREATE DATABASE IF NOT EXISTS {database_name}"))


def check_database_connection():
    MAX_RETRY = 3
    retry_count = 0
    is_successful = False
    while retry_count < MAX_RETRY:
        retry_count += 1
        try:
            with app.app_context():
                db.session.execute(text("SELECT 1"))
                app.logger.info("Database connection successful")
                is_successful = True
                return True
        except Exception as e:
            app.logger.error(f"Error while connecting to database: {e}, retrying...")
            time.sleep(3)

    if not is_successful:
        app.logger.error("Exiting.. Since connection to database failed")
        sys.exit(1)


def validate_connections():
    check_database_connection()
    create_database()


if __name__ == "__main__":
    validate_connections()
