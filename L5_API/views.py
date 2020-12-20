from flask import jsonify
from L5_API import db_app


def get_last_date(code):
    return jsonify(date=db_app.get_todays_date(code))
