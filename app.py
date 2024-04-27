from manage import validate_connections
from src.api import api, app
from src.urls import config_api_urls

# Add api endpoints
config_api_urls(api)


def main():
    validate_connections()
    app.run(
        debug=app.config.get("DEBUG", False),
        port=app.config.get("PORT"),
        host="0.0.0.0",
    )


if __name__ == "__main__":
    main()
