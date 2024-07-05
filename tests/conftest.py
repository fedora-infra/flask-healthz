# SPDX-FileCopyrightText: 2020-2024 Red Hat
#
# SPDX-License-Identifier: BSD-3-Clause

import pytest
from flask import Flask


@pytest.fixture
def app():
    app = Flask("test_app")
    app.config["TESTING"] = True
    return app
