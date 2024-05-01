# Import your SQLAlchemy models
import sys
import time

from sqlalchemy import create_engine, text

from src.api import app, db


def get_db_engine():
    DATABASE_URI = app.config.get("DATABASE_URI", "")
    return create_engine(DATABASE_URI)


def check_database_connection():
    MAX_RETRY = 10
    SLEEP_TIME = 3
    retry_count = 0
    error_message = None
    while retry_count < MAX_RETRY:
        retry_count += 1
        try:
            engine = get_db_engine()
            with engine.connect().execution_options(autocommit=True) as connection:
                connection.execute(text("SELECT 1"))
                app.logger.info("Database connection successful")
                error_message = None
                return True
        except Exception as e:
            error_message = str(e)
            if "Unknown database" in error_message:
                create_database()
            app.logger.error(f"Database is not running yet: {e}, waiting...")
            time.sleep(SLEEP_TIME)

    if error_message:
        app.logger.critical(
            f"Connection to database failed - {error_message}, Exiting.."
        )
        sys.exit(1)


def check_database_connection_sqlalchemy():
    MAX_RETRY = 10
    SLEEP_TIME = 3
    retry_count = 0
    error_message = None
    while retry_count < MAX_RETRY:
        retry_count += 1
        try:
            with app.app_context():
                db.session.execute(text("SELECT 1"))
                app.logger.info("Database connection successful")
                error_message = None
                return True
        except Exception as e:
            error_message = str(e)
            if "Unknown database" in error_message:
                create_database()
            app.logger.error(f"Database is not running yet: {e}, waiting...")
            time.sleep(SLEEP_TIME)

    if error_message:
        app.logger.critical(
            f"Connection to database failed - {error_message}, Exiting.."
        )
        sys.exit(1)


def create_database():
    """Create the database if it doesn't exist."""
    engine = get_db_engine()
    database_name = app.config.get("DATABASE_NAME", "hospital_management")
    app.logger.info(f"Creating database: {database_name} if not exists..")
    with engine.connect().execution_options(autocommit=True) as connection:
        connection.execute(text(f"CREATE DATABASE IF NOT EXISTS {database_name}"))


def setup_database():
    app.logger.info("Setting up database..")
    create_database()


def validate_dependencies():
    app.logger.info("Validating database connection..")
    check_database_connection_sqlalchemy()


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Database Setup Utility")
    parser.add_argument("-db", "--db_setup", help="setup database", default="False")

    args = parser.parse_args()
    if args.db_setup == "True":
        setup_database()

    check_database_connection()
