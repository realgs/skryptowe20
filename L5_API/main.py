from flask import Flask
from flask_restful import Api
from L5_API import views


app = Flask(__name__)
api = Api(app)

app.add_url_rule('/rates/<code>', view_func=views.get_last_rate)
app.add_url_rule('/rates/<code>/<date_from>/<date_to>', view_func=views.get_rates)
app.add_url_rule('/sales/<date_from>/<date_to>', view_func=views.get_sales)


if __name__ == "__main__":
    app.run(debug=True)
