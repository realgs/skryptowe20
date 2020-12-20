from flask import Blueprint

currency_controller = Blueprint("currency_controller", __name__)

@currency_controller.route('/', methods=['GET'])
def home():
    return "xD"