import os
from src.api import app, db


def setup_database():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ["TEST_DATABASE_URI"]
    db.init_app(app)
    app.app_context().push()
    db.create_all()


def teardown_database():
    db.session.remove()
    db.drop_all()
