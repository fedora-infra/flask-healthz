import logging

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


def test_ext_no_log(app, caplog):
    gunicorn_logger = logging.getLogger("gunicorn.access")
    caplog.set_level(logging.INFO)
    Healthz(app, no_log=True)
    # This URL is handled by flask_healthz
    gunicorn_logger.info("%(U)s", {"U": "/healthz/live", "s": 200})
    assert len(caplog.records) == 0
    # This URL is *not* handled by flask_healthz
    gunicorn_logger.info("%(U)s", {"U": "/somewhere/else", "s": 200})
    assert caplog.messages == ["/somewhere/else"]


def test_ext_no_log_on_errors(app, caplog):
    gunicorn_logger = logging.getLogger("gunicorn.access")
    caplog.set_level(logging.INFO)
    Healthz(app, no_log=True)
    # Do log errors on heathlz requests
    gunicorn_logger.info("%(s)s %(U)s", {"U": "/healthz/live", "s": 500})
    assert caplog.messages == ["500 /healthz/live"]
