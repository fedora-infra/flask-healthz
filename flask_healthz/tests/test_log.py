import logging

import pytest

from flask_healthz import Healthz


@pytest.fixture
def get_logger():
    loggers = []

    def _get_logger(name):
        logger = logging.getLogger(name)
        loggers.append(logger)
        return logger

    yield _get_logger

    # Remove all loggers and intermediary loggers along the path
    manager = logging.getLogger().manager  # Undocumented API
    for logger in loggers:
        logger_path = logger.name.split(".")
        while logger_path:
            del manager.loggerDict[".".join(logger_path)]
            logger_path.pop()


def test_no_log(app, caplog, get_logger):
    gunicorn_logger = get_logger("gunicorn.access")
    caplog.set_level(logging.INFO)
    Healthz(app, no_log=True)
    # This URL is handled by flask_healthz
    gunicorn_logger.info("%(U)s", {"U": "/healthz/live", "s": 200})
    assert len(caplog.records) == 0
    # This URL is *not* handled by flask_healthz
    gunicorn_logger.info("%(U)s", {"U": "/somewhere/else", "s": 200})
    assert caplog.messages == ["/somewhere/else"]


def test_no_log_on_errors(app, caplog, get_logger):
    gunicorn_logger = get_logger("gunicorn.access")
    caplog.set_level(logging.INFO)
    Healthz(app, no_log=True)
    # Do log errors on heathlz requests
    gunicorn_logger.info("%(s)s %(U)s", {"U": "/healthz/live", "s": 500})
    assert caplog.messages == ["500 /healthz/live"]


def test_no_log_no_logger(app, caplog, get_logger):
    logger = get_logger("something.else")
    caplog.set_level(logging.INFO)
    Healthz(app, no_log=True)
    # This should be logged as usual, because only gunicorn is supported yet.
    logger.info("%(U)s", {"U": "/healthz/live", "s": 200})
    assert caplog.messages == ["/healthz/live"]
