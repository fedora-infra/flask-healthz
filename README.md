# Flask-Healthz

Define endpoints in your Flask application that Kubernetes can use as
[liveness and readiness probes](https://kubernetes.io/docs/tasks/configure-pod-container/configure-liveness-readiness-startup-probes/).


## Setting it up

### Blueprint

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
{"status": 200, "title": "OK"}
$ curl http://localhost/yourapp/healthz/ready
{"status": 200, "title": "OK"}
```

Now your can configure Kubernetes or OpenShift to check for those endpoints.

### Extension

You can also use the provided Flask extension to register the `healthz` blueprint:

```python
from flask import Flask
from flask_healthz import Healthz

app = Flask(__name__)
Healthz(app)
```

The rest of the configuration is identical.

The extension has an additional option, `no_log`, that can disable logging of the HTTP requests
handled by your healthz endpoints, to avoid cluttering your web log files with automated requests.
At the moment, only the [gunicorn](https://gunicorn.org/) web server is supported.

```python
Healthz(app, no_log=True)
```

## Examples

Here's an example of how you could use flask-healthz in OpenShift's `deploymentconfig`:

```yaml
kind: DeploymentConfig
spec:
  [...]
  template:
    [...]
    spec:
      containers:
      - name: yourapp
        [...]
        livenessProbe:
          httpGet:
            path: /healthz/live
            port: 8080
          initialDelaySeconds: 5
          timeoutSeconds: 1
        readinessProbe:
          httpGet:
            path: /healthz/ready
            port: 8080
          initialDelaySeconds: 5
          timeoutSeconds: 1
```

Some projects that have setup flask-healthz:

- Noggin: https://github.com/fedora-infra/noggin/pull/287
- FASJSON: https://github.com/fedora-infra/fasjson/pull/81


## License

Copyright 2020-2021 Red Hat

Flask-Healthz is licensed under the same license as Flask itself: BSD 3-clause.


[![codecov](https://codecov.io/gh/fedora-infra/flask-healthz/branch/dev/graph/badge.svg?token=lwlZLiSImq)](https://codecov.io/gh/fedora-infra/flask-healthz)
