import logging

from .blueprint import healthz
from .log import PrefixFilter


class Healthz:
    def __init__(self, app=None, prefix="/healthz", no_log=False):
        self.prefix = prefix
        self.no_log = no_log
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        app.register_blueprint(healthz, url_prefix=self.prefix)
        if self.no_log:
            prefix_filter = PrefixFilter(self.prefix)
            loggers = logging.getLogger().manager.loggerDict  # Undocumented API
            # Gunicorn support
            if "gunicorn.access" in loggers:
                logger = logging.getLogger("gunicorn.access")
                logger.addFilter(prefix_filter)
