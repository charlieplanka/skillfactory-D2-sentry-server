import os
from dotenv import load_dotenv

import sentry_sdk
from bottle import Bottle
from sentry_sdk.integrations.bottle import BottleIntegration

load_dotenv()
SENTRY_DSN = os.getenv("SENTRY_DSN")

sentry_sdk.init(
    dsn=SENTRY_DSN,
    integrations=[BottleIntegration()]
)

app = Bottle()


@app.route("/success")
def success():
    return "Everything is OK!"


@app.route("/fail")
def fail():
    raise RuntimeError("Something went wrong")


if os.environ.get("APP_LOCATION") == "heroku":
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 5000)),
        server="gunicorn",
        workers=3,
    )
else:
    app.run(host="localhost", port=8081, debug=True)
