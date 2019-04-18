import pytest
from eventmanager import create_app, db

@pytest.fixture
def app():
    """Create and configure a new app instance for each test."""
    app = create_app()
    yield app

@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()


@pytest.fixture(scope="function", autouse=True)
def clean_up_db(client, app):
    with app.app_context():
        db.session.rollback() 
        db.drop_all()
        db.create_all()
        # db.session.commit()