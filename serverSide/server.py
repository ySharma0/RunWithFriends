from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/", methods = ["POST"])
def index():
    return "index"