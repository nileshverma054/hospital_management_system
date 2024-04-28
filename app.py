from flask_migrate import Migrate

from manage import validate_dependencies
from src.api import api, app, db
from src.models.models import *
from src.urls import config_api_urls

migrate = Migrate(app, db)

# intialize sqlalchemy
db.init_app(app)


def main():
    # Add api endpoints
    config_api_urls(api)

    # validate dependencies - database
    validate_dependencies()

    # run app
    app.run(
        debug=app.config.get("DEBUG", False),
        port=app.config.get("PORT"),
        host="0.0.0.0",
    )


if __name__ == "__main__":
    main()
