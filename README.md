# Flask-Healthz

Define endpoints in your Flask application that Kubernetes can use as
[liveness and readiness probes](https://kubernetes.io/docs/tasks/configure-pod-container/configure-liveness-readiness-startup-probes/).

## Setting it up

Register the blueprint on your Flask application:

```python
from flask import Flask
from flask_healthz import healthz

app = Flask(__name__)
app.register_blueprint(healthz, url_prefix="/healthz")
```

Define the functions you want to use to check health. To signal an error, raise `flask_healthz.HealthError`.

```python
from flask_healthz import HealthError

def liveness():
    pass

def readiness():
    try:
        connect_database()
    except Exception:
        raise HealthError("Can't connect to the database")
```

Now point to those functions in the Flask configuration:

```python
HEALTHZ = {
    "live": "yourapp.checks.liveness",
    "ready": "yourapp.checks.readiness",
}
```

It is possible to directly set callables in the configuration, so you could write something like:

```python
HEALTHZ = {
    "live": lambda: None,
}
```

Check that the endpoints actually work:

```
$ curl http://localhost/yourapp/healthz/live
OK
$ curl http://localhost/yourapp/healthz/ready
OK
```

Now your can configure Kubernetes to check for those endpoints.

## License

Copyright 2020 Red Hat

Flask-Healthz is licensed under the same license as Flask itself: BSD 3-clause.
