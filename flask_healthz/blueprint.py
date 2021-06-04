from flask import Blueprint, abort, current_app
from werkzeug.utils import import_string


class HealthError(Exception):
    pass


healthz = Blueprint("healthz", __name__)


@healthz.route("/<name>")
def check(name):
    try:
        check_function = current_app.config["HEALTHZ"][name]
    except KeyError:
        abort(404, "The {} check endpoint is not setup".format(name))

    if not callable(check_function):
        try:
            check_function = import_string(check_function)
        except ImportError:
            abort(
                500, "The {} check function could not be imported".format(name),
            )

    mime_type = "text/plain"

    try:
        check_function()
    except HealthError as e:
        return current_app.response_class(
            "{}\n".format(e), status=503, mimetype=mime_type
        )
    else:
        return current_app.response_class("OK\n", mimetype=mime_type)


# Basic Talisman support: we don't want this view to redirect to HTTPS
check.talisman_view_options = {"force_https": False}
# (another way to get the same result would be to do this in your own code:
# talisman(force_https=False)(app.view_functions["healthz.check"])
# https://github.com/GoogleCloudPlatform/flask-talisman#per-view-options
