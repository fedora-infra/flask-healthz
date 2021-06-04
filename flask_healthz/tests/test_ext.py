from flask_healthz import Healthz


def test_ext(app):
    Healthz(app)
    app.config["HEALTHZ"] = {"live": lambda: None}
    with app.test_client() as client:
        response = client.get("/healthz/live")
        assert response.status_code == 200
        assert response.get_json() == {"status": 200, "title": "OK"}


def test_ext_deferred_init(app):
    ext = Healthz()
    app.config["HEALTHZ"] = {"live": lambda: None}
    ext.init_app(app)
    with app.test_client() as client:
        response = client.get("/healthz/live")
        assert response.status_code == 200
        assert response.get_json() == {"status": 200, "title": "OK"}
