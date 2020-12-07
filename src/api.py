from flask import Flask, jsonify, request


app = Flask(__name__)
db = None


@app.route('/api/home/<name>')
def home(name):
  return jsonify(hello= "Hello",
              world=name)


# @app.route('/api/rates/<date>')
# def return_rate():
#   pass


if __name__ == '__main__':
  app.run('0.0.0.0',port= 8080,debug=True)
