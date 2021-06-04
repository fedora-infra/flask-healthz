import logging

from flask_healthz import Healthz


def test_ext(app):
    Healthz(app)
    app.config["HEALTHZ"] = {"live": lambda: None}
    with app.test_client() as client:
        response = client.get("/healthz/live")
        assert response.status_code == 200
        assert response.content_type == "text/plain; charset=utf-8"
        assert response.get_data(as_text=True) == "OK\n"


def test_ext_deferred_init(app):
    ext = Healthz()
    app.config["HEALTHZ"] = {"live": lambda: None}
    ext.init_app(app)
    with app.test_client() as client:
        response = client.get("/healthz/live")
        assert response.status_code == 200
        assert response.get_data(as_text=True) == "OK\n"


def test_ext_no_log(app, caplog):
    gunicorn_logger = logging.getLogger("gunicorn.access")
    caplog.set_level(logging.INFO)
    Healthz(app, no_log=True)
    # This URL is handled by flask_healthz
    gunicorn_logger.info("%(U)s", {"U": "/healthz/live"})
    assert len(caplog.records) == 0
    # This URL is *not* handled by flask_healthz
    gunicorn_logger.info("%(U)s", {"U": "/somewhere/else"})
    assert caplog.messages == ["/somewhere/else"]
