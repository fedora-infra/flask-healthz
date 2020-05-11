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

    try:
        check_function()
    except HealthError as e:
        return "{}\n".format(e), 503
    else:
        return "OK\n"
