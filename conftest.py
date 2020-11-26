from app import app as app1
import pytest

@pytest.fixture
def app():
    app = app1
    return app