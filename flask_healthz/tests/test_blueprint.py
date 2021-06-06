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
        assert response.content_type == "application/problem+json"
        assert response.get_json() == {"status": 200, "title": "OK"}


def test_bp_no_endpoint(blueprint, app):
    with app.test_client() as client:
        response = client.get("/nowhere")
        assert response.status_code == 404
        assert response.content_type == "application/problem+json"
        expected = {"status": 404, "title": "The nowhere check endpoint is not setup"}
        assert response.get_json() == expected


def test_bp_bad_endpoint(blueprint, app):
    app.config["HEALTHZ"] = {"live": "bad.import.path"}
    with app.test_client() as client:
        response = client.get("/live")
        assert response.status_code == 500
        assert response.content_type == "application/problem+json"
        expected = {
            "status": 500,
            "title": "The live check function could not be imported",
        }
        assert response.get_json() == expected


def test_bp_fail(blueprint, app):
    app.config["HEALTHZ"] = {"live": f"{__name__}.failing"}
    with app.test_client() as client:
        response = client.get("/live")
        assert response.status_code == 503
        assert response.content_type == "application/problem+json"
        expected = {"status": 503, "title": "This is failing."}
        assert response.get_json() == expected
