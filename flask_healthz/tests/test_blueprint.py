import pytest
from flask_healthz import HealthError, healthz


@pytest.fixture
def blueprint(app):
    app.register_blueprint(healthz, prefix="/")
    return healthz


def failing():
    raise HealthError("This is failing.")


def test_bp(blueprint, app):
    app.config["HEALTHZ"] = {"live": lambda: None}
    with app.test_client() as client:
        response = client.get("/live")
        assert response.status_code == 200
        assert response.content_type == "text/plain; charset=utf-8"
        assert response.get_data(as_text=True) == "OK\n"


def test_bp_no_endpoint(blueprint, app):
    with app.test_client() as client:
        response = client.get("/nowhere")
        assert response.status_code == 404
        assert response.content_type == "text/html; charset=utf-8"
        expected = """<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 3.2 Final//EN">
<title>404 Not Found</title>
<h1>Not Found</h1>
<p>The nowhere check endpoint is not setup</p>
"""
        assert response.get_data(as_text=True) == expected


def test_bp_bad_endpoint(blueprint, app):
    app.config["HEALTHZ"] = {"live": "bad.import.path"}
    with app.test_client() as client:
        response = client.get("/live")
        assert response.status_code == 500
        assert response.content_type == "text/html; charset=utf-8"
        expected = """<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 3.2 Final//EN">
<title>500 Internal Server Error</title>
<h1>Internal Server Error</h1>
<p>The live check function could not be imported</p>
"""
        assert response.get_data(as_text=True) == expected


def test_bp_fail(blueprint, app):
    app.config["HEALTHZ"] = {"live": f"{__name__}.failing"}
    with app.test_client() as client:
        response = client.get("/live")
        assert response.status_code == 503
        assert response.content_type == "text/plain; charset=utf-8"
        expected = "This is failing.\n"
        assert response.get_data(as_text=True) == expected
