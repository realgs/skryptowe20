import flask
from currency_controller import currency_controller
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

app = flask.Flask(__name__)
app.config["DEBUG"] = True

limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["1000 per day", "300 per hour"]
)
limiter.limit("5/minute")(currency_controller)

app.register_blueprint(currency_controller)

@app.errorhandler(404)
def page_not_found(e):
    return ("Sorry but requested route was not found", 404)

if __name__ == "__main__":
    app.run()
