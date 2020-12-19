from flask import Flask
from flask_restful import Api, Resource

app = Flask(__name__)
api = Api(app)


class UsdRates(Resource):
    def get(self):
        return "Hello World"


api.add_resource(UsdRates, "/usd")


if __name__ == "__main__":
    app.run(debug=True)
