from flask import Flask
from flask_restful import Api
from L5_API import views


app = Flask(__name__)
api = Api(app)

app.add_url_rule('/date/<code>', view_func=views.get_last_date)


if __name__ == "__main__":
    app.run(debug=True)
