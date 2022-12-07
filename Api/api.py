#!/usr/bin/env python3
from flask_restx import Api
from flask import Flask, Blueprint

api_v1 = Blueprint("api", __name__, url_prefix="/api")
api = Api(api_v1, version="1.2.0", title="Joker",
          description="Life's a joke")
app = Flask(__name__)
app.register_blueprint(api_v1)


# Import API Resources
# The below conditions prevents IDE auto-formatting
# skipcq: PYL-W0125
if True:
    # Secret Engines
    from Api.resources.generate.topic_resource import Engine_KV  # noqa: F401