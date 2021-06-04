from flask import Blueprint, current_app
from flask.json import dumps
from werkzeug.utils import import_string


class HealthError(Exception):
    pass


healthz = Blueprint("healthz", __name__)


def _make_response(status, title):
    return current_app.response_class(
        dumps({"status": status, "title": title}),
        status=status,
        content_type="application/problem+json",
    )


@healthz.route("/<name>")
def check(name):
    try:
        check_function = current_app.config["HEALTHZ"][name]
    except KeyError:
        return _make_response(404, "The {} check endpoint is not setup".format(name))

    if not callable(check_function):
        try:
            check_function = import_string(check_function)
        except ImportError:
            return _make_response(
                500, "The {} check function could not be imported".format(name)
            )

    try:
        check_function()
    except HealthError as e:
        status = 503
        title = str(e)
    else:
        status = 200
        title = "OK"
    return _make_response(status, title)


# Basic Talisman support: we don't want this view to redirect to HTTPS
check.talisman_view_options = {"force_https": False}
# (another way to get the same result would be to do this in your own code:
# talisman(force_https=False)(app.view_functions["healthz.check"])
# https://github.com/GoogleCloudPlatform/flask-talisman#per-view-options
