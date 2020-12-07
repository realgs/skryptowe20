from flask import Flask, jsonify


app = Flask(__name__)


@app.route('/api')
def home():
  return jsonify(hello= "Hello",
                world="World")



if __name__ == '__main__':
  app.run(debug=True)
