from src.api import api, app, db
from src.urls import config_api_urls

# Add api endpoints
config_api_urls(api)

# configure database
db.init_app(app)


if __name__ == "__main__":
    app.run(
        debug=app.config.get("DEBUG", False),
        port=app.config.get("PORT"),
        host="0.0.0.0",
    )
